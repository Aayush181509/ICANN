"""Chunking, embeddings, vector store and the RAG answering loop.

Designed for teaching, not for production:
    * Single embedding backend abstraction (local sentence-transformers or OpenAI).
    * In-memory NumPy vector store (no DB), with optional Chroma persistence.
    * Simple prompt template that injects retrieved chunks and asks for citations.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import numpy as np
from dotenv import load_dotenv

from .llm_client import ask_llm

load_dotenv()


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    """Split text into ~`chunk_size` character chunks with `overlap` characters
    of overlap between consecutive chunks.

    Uses paragraph boundaries where possible to avoid cutting sentences.
    """
    if not text or not text.strip():
        return []
    # Normalise whitespace
    text = re.sub(r"\s+\n", "\n", text).strip()
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks: list[str] = []
    buf = ""
    for para in paragraphs:
        if len(buf) + len(para) + 1 <= chunk_size:
            buf = (buf + "\n" + para).strip()
        else:
            if buf:
                chunks.append(buf)
            if len(para) <= chunk_size:
                buf = para
            else:
                # Hard wrap a long paragraph
                for i in range(0, len(para), chunk_size - overlap):
                    chunks.append(para[i:i + chunk_size])
                buf = ""
    if buf:
        chunks.append(buf)
    # Add overlap by prepending the tail of the previous chunk
    if overlap > 0 and len(chunks) > 1:
        out = [chunks[0]]
        for prev, cur in zip(chunks, chunks[1:]):
            tail = prev[-overlap:]
            out.append((tail + " " + cur).strip())
        return out
    return chunks


def chunk_documents(docs: list[dict], chunk_size: int = 800, overlap: int = 120) -> list[dict]:
    """Apply chunk_text to each document while propagating metadata.

    Each output chunk has ``metadata.chunk_index``.
    """
    out: list[dict] = []
    for doc in docs:
        parts = chunk_text(doc["text"], chunk_size=chunk_size, overlap=overlap)
        for idx, part in enumerate(parts):
            meta = dict(doc.get("metadata", {}))
            meta["chunk_index"] = idx
            out.append({"text": part, "metadata": meta})
    return out


# ---------------------------------------------------------------------------
# Embedding backends
# ---------------------------------------------------------------------------
class _LocalEmbedder:
    _model = None

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name

    def _load(self):
        if _LocalEmbedder._model is None:
            from sentence_transformers import SentenceTransformer
            _LocalEmbedder._model = SentenceTransformer(self.model_name)
        return _LocalEmbedder._model

    def encode(self, texts: list[str]) -> np.ndarray:
        m = self._load()
        return np.asarray(m.encode(texts, show_progress_bar=False, normalize_embeddings=True))


class _OpenAIEmbedder:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or os.getenv(
            "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
        )

    def encode(self, texts: list[str]) -> np.ndarray:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        resp = client.embeddings.create(model=self.model_name, input=texts)
        arr = np.asarray([d.embedding for d in resp.data], dtype=np.float32)
        # L2-normalise so cosine == dot product
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms[norms == 0] = 1
        return arr / norms


def get_embedder():
    provider = os.getenv("EMBEDDING_PROVIDER", "local").strip().lower()
    if provider == "openai" and os.getenv("OPENAI_API_KEY", "").startswith("sk-"):
        return _OpenAIEmbedder()
    return _LocalEmbedder()


# ---------------------------------------------------------------------------
# Tiny in-memory vector store
# ---------------------------------------------------------------------------
@dataclass
class VectorStore:
    """A minimal cosine-similarity vector store.

    Built on NumPy so it works offline with no dependencies beyond what is
    already in requirements.txt. Suitable for thousands of chunks. For larger
    corpora switch to Chroma (see ``ChromaStore`` below).
    """
    texts: list[str] = field(default_factory=list)
    metadatas: list[dict] = field(default_factory=list)
    embeddings: np.ndarray | None = None
    embedder: object = field(default_factory=get_embedder)

    def add(self, chunks: list[dict]):
        if not chunks:
            return
        new_texts = [c["text"] for c in chunks]
        new_meta = [c.get("metadata", {}) for c in chunks]
        new_emb = self.embedder.encode(new_texts)
        self.texts.extend(new_texts)
        self.metadatas.extend(new_meta)
        if self.embeddings is None:
            self.embeddings = new_emb
        else:
            self.embeddings = np.vstack([self.embeddings, new_emb])

    def search(self, query: str, k: int = 4, where: dict | None = None) -> list[dict]:
        if self.embeddings is None or len(self.texts) == 0:
            return []
        q = self.embedder.encode([query])[0]
        sims = self.embeddings @ q
        # metadata filter
        if where:
            mask = np.array([
                all(m.get(k_) == v for k_, v in where.items())
                for m in self.metadatas
            ])
            sims = np.where(mask, sims, -np.inf)
        idx = np.argsort(-sims)[:k]
        out = []
        for i in idx:
            if not np.isfinite(sims[i]):
                continue
            out.append({
                "text": self.texts[i],
                "metadata": self.metadatas[i],
                "score": float(sims[i]),
            })
        return out

    def __len__(self):
        return len(self.texts)


# ---------------------------------------------------------------------------
# Optional Chroma-backed store (persistent)
# ---------------------------------------------------------------------------
class ChromaStore:
    """Same interface as VectorStore but persists to disk via ChromaDB."""

    def __init__(self, persist_dir: str | Path, collection_name: str = "ican_ca"):
        import chromadb
        self.persist_dir = str(persist_dir)
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.embedder = get_embedder()

    def add(self, chunks: list[dict]):
        if not chunks:
            return
        texts = [c["text"] for c in chunks]
        metas = [_flatten_meta(c.get("metadata", {})) for c in chunks]
        embs = self.embedder.encode(texts).tolist()
        # Make IDs deterministic and unique
        existing = self.collection.count()
        ids = [f"chunk-{existing + i}" for i in range(len(chunks))]
        self.collection.add(ids=ids, documents=texts, metadatas=metas, embeddings=embs)

    def search(self, query: str, k: int = 4, where: dict | None = None) -> list[dict]:
        emb = self.embedder.encode([query]).tolist()
        kw = {"query_embeddings": emb, "n_results": k}
        if where:
            kw["where"] = where
        res = self.collection.query(**kw)
        out = []
        if not res["documents"]:
            return out
        for text, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            out.append({
                "text": text,
                "metadata": meta,
                "score": 1.0 - float(dist),
            })
        return out

    def __len__(self):
        return self.collection.count()


def _flatten_meta(meta: dict) -> dict:
    """Chroma requires scalar metadata values."""
    out = {}
    for k, v in meta.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            out[k] = v
        else:
            out[k] = json.dumps(v, default=str)
    return out


# ---------------------------------------------------------------------------
# RAG prompt and answer loop
# ---------------------------------------------------------------------------
DEFAULT_SYSTEM = (
    "You are an experienced Nepali Chartered Accountant assistant. "
    "Answer ONLY using the provided context. If the context does not contain "
    "the answer, say exactly: \"I could not find this in the provided "
    "documents.\" Always cite sources by filename and page (if available) "
    "in square brackets at the end of each fact, e.g. "
    "[source: 02_audit_planning_memo.pdf, p.1]."
)


def _format_context(hits: list[dict]) -> str:
    blocks = []
    for i, h in enumerate(hits, start=1):
        m = h["metadata"]
        cite_bits = [f"source: {m.get('source', 'unknown')}"]
        if "page" in m: cite_bits.append(f"p.{m['page']}")
        if "sheet" in m: cite_bits.append(f"sheet:{m['sheet']}")
        cite = ", ".join(cite_bits)
        blocks.append(f"[chunk {i} — {cite}]\n{h['text']}")
    return "\n\n---\n\n".join(blocks)


def rag_answer(
    query: str,
    store,
    k: int = 4,
    where: dict | None = None,
    system: str | None = None,
    model: str | None = None,
    return_hits: bool = False,
):
    """Retrieve top-k chunks and ask the LLM to answer with citations.

    Returns the answer string, or a (answer, hits) tuple if return_hits=True.
    """
    hits = store.search(query, k=k, where=where)
    if not hits:
        msg = "I could not find this in the provided documents."
        return (msg, []) if return_hits else msg
    context = _format_context(hits)
    prompt = (
        f"Question: {query}\n\n"
        f"Context:\n{context}\n\n"
        "Answer the question using only the context above. "
        "Cite each fact with [source: ..., p. ...] at the end of the sentence."
    )
    answer = ask_llm(prompt, system=system or DEFAULT_SYSTEM, model=model, temperature=0.1)
    return (answer, hits) if return_hits else answer


# ---------------------------------------------------------------------------
# Build a store from a folder in one call (used in notebooks)
# ---------------------------------------------------------------------------
def build_store_from_folder(
    folder: str | Path,
    chunk_size: int = 800,
    overlap: int = 120,
    persist_dir: str | Path | None = None,
):
    from .document_loaders import load_folder
    docs = load_folder(folder)
    chunks = chunk_documents(docs, chunk_size=chunk_size, overlap=overlap)
    if persist_dir:
        try:
            store = ChromaStore(persist_dir=persist_dir)
            store.add(chunks)
            return store
        except Exception as e:  # noqa: BLE001
            print(f"[warn] ChromaStore failed ({e}); using in-memory VectorStore.")
    store = VectorStore()
    store.add(chunks)
    return store
