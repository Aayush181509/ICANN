# Section 02: Chunking Strategies for Financial Documents

**Duration:** ~60 minutes  
**Goal:** Understand that *how* you split a document is as important as the retrieval itself, and compare 4 strategies on the same annual report.

---

## Why Chunking Matters

Chunking is like **deciding how to index a book**.

Imagine you are indexing the NMB Bank Annual Report:
- **By sentences** → Very granular. *"Net profit was NPR 2.3 billion"* is one chunk. Good for precise lookups, but loses surrounding context.
- **By chapters** → Very broad. Each chunk is 20 pages. The answer is buried inside — retrieval is noisy.
- **By fixed size** → Predictable. Sometimes cuts mid-sentence or mid-table.
- **By meaning** → Best of both worlds. Chunks end where the topic naturally ends.

For financial documents — which have **tables, footnotes, ratio calculations, and narrative sections** — chunking strategy significantly changes answer quality.

## The 4 Strategies We Will Compare

```
Same PDF Document
       │
       ├──► Fixed-Size Chunking      ──► ChromaDB-1 ──┐
       │                                               │
       ├──► Sentence-Based Chunking  ──► ChromaDB-2 ──┤
       │                                               ├──► Same Query ──► Compare Answers
       ├──► Paragraph-Based Chunking ──► ChromaDB-3 ──┤
       │                                               │
       └──► Semantic Chunking        ──► ChromaDB-4 ──┘
```

| Strategy | Split Logic | Pros | Cons |
|----------|-------------|------|------|
| **Fixed-size** | Every N tokens | Predictable, fast | Cuts mid-sentence/mid-table |
| **Sentence-based** | `.`, `?`, `!` | Preserves sentence integrity | Loses multi-sentence context |
| **Paragraph-based** | `\n\n` | Preserves logical sections | Paragraphs vary wildly in length |
| **Semantic** | Cosine distance between sentences | Topic-aware splits | Slower, needs embeddings upfront |


```python
import os
import re
import textwrap
import numpy as np

import chromadb
import nltk
import tiktoken
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["figure.dpi"] = 120

from openai import OpenAI
from pypdf import PdfReader

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
EMBED_MODEL = "text-embedding-3-small"
enc = tiktoken.get_encoding("cl100k_base")

# Load the PDF
PDF_PATH = "../data/annual_reports/nmb_bank_annual_report_2023.pdf"
reader = PdfReader(PDF_PATH)
full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
print(f"Loaded {len(reader.pages)} pages, {len(full_text):,} characters.")
```


```python
# ── Strategy 1: Fixed-size chunking ──────────────────────────────────────────
def fixed_size_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(enc.decode(tokens[start:end]))
        start += chunk_size - overlap
    return chunks

chunks_fixed = fixed_size_chunks(full_text)

print(f"Fixed-size chunks : {len(chunks_fixed)}")
print(f"Avg length        : {int(np.mean([len(c) for c in chunks_fixed]))} chars")
print()
for i, c in enumerate(chunks_fixed[5:8], start=6):
    print(f"  Chunk {i}: {c[:180].strip()}...\n")
```


```python
# ── Strategy 2: Sentence-based chunking ──────────────────────────────────────
from nltk.tokenize import sent_tokenize

def sentence_chunks(text: str, sentences_per_chunk: int = 5, overlap: int = 1) -> list[str]:
    sentences = sent_tokenize(text)
    chunks = []
    start = 0
    while start < len(sentences):
        end = min(start + sentences_per_chunk, len(sentences))
        chunks.append(" ".join(sentences[start:end]))
        start += sentences_per_chunk - overlap
    return chunks

chunks_sentence = sentence_chunks(full_text)

print(f"Sentence-based chunks : {len(chunks_sentence)}")
print(f"Avg length            : {int(np.mean([len(c) for c in chunks_sentence]))} chars")
print()
for i, c in enumerate(chunks_sentence[5:8], start=6):
    print(f"  Chunk {i}: {c[:180].strip()}...\n")
```


```python
# ── Strategy 3: Paragraph-based chunking ─────────────────────────────────────
def paragraph_chunks(text: str, min_length: int = 100, max_length: int = 2000) -> list[str]:
    raw = re.split(r"\n{2,}", text)
    chunks = []
    buffer = ""
    for para in raw:
        para = para.strip()
        if not para:
            continue
        if len(buffer) + len(para) < max_length:
            buffer = (buffer + "\n\n" + para).strip()
        else:
            if len(buffer) >= min_length:
                chunks.append(buffer)
            buffer = para
    if len(buffer) >= min_length:
        chunks.append(buffer)
    return chunks

chunks_para = paragraph_chunks(full_text)

print(f"Paragraph-based chunks : {len(chunks_para)}")
print(f"Avg length             : {int(np.mean([len(c) for c in chunks_para]))} chars")
print()
for i, c in enumerate(chunks_para[5:8], start=6):
    print(f"  Chunk {i}: {c[:180].strip()}...\n")
```


```python
# ── Strategy 4: Semantic chunking ────────────────────────────────────────────
# Split sentences, embed them, then split where cosine distance between
# consecutive sentences drops sharply (topic shift)

from nltk.tokenize import sent_tokenize

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

def semantic_chunks(
    text: str,
    threshold: float = 0.75,
    window: int = 3,
    max_sentences_per_chunk: int = 15
) -> list[str]:
    sentences = sent_tokenize(text)
    if len(sentences) < 2:
        return sentences

    # Embed all sentences
    print(f"  Embedding {len(sentences)} sentences for semantic chunking...")
    resp = client.embeddings.create(model=EMBED_MODEL, input=sentences)
    embeds = [item.embedding for item in resp.data]

    # Compute similarity between consecutive windows
    split_indices = [0]
    for i in range(window, len(sentences) - window):
        left  = np.mean(embeds[max(0, i-window):i], axis=0)
        right = np.mean(embeds[i:min(len(embeds), i+window)], axis=0)
        sim = cosine_sim(left, right)
        chunk_size_so_far = i - split_indices[-1]
        if sim < threshold or chunk_size_so_far >= max_sentences_per_chunk:
            split_indices.append(i)

    split_indices.append(len(sentences))

    chunks = []
    for i in range(len(split_indices) - 1):
        chunk = " ".join(sentences[split_indices[i]:split_indices[i + 1]])
        if chunk.strip():
            chunks.append(chunk.strip())
    return chunks

print("Running semantic chunking (slowest — embeds every sentence)...")
chunks_semantic = semantic_chunks(full_text)

print(f"Semantic chunks        : {len(chunks_semantic)}")
print(f"Avg length             : {int(np.mean([len(c) for c in chunks_semantic]))} chars")
print()
for i, c in enumerate(chunks_semantic[5:8], start=6):
    print(f"  Chunk {i}: {c[:180].strip()}...\n")
```


```python
# Build 4 ChromaDB collections, one per strategy
chroma_client = chromadb.Client()

def build_collection(name: str, chunks: list[str]) -> chromadb.Collection:
    col = chroma_client.create_collection(name=name, metadata={"hnsw:space": "cosine"})
    # Embed in batches
    embeddings = []
    for i in range(0, len(chunks), 100):
        batch = chunks[i:i+100]
        resp = client.embeddings.create(model=EMBED_MODEL, input=batch)
        embeddings.extend([item.embedding for item in resp.data])
    col.add(documents=chunks, embeddings=embeddings, ids=[f"{name}_{i}" for i in range(len(chunks))])
    print(f"  Collection '{name}': {col.count()} chunks stored.")
    return col

print("Building ChromaDB collections...")
col_fixed    = build_collection("fixed",    chunks_fixed)
col_sentence = build_collection("sentence", chunks_sentence)
col_para     = build_collection("para",     chunks_para)
col_semantic = build_collection("semantic", chunks_semantic)
print("Done.")
```


```python
# Run the same query across all 4 strategies and compare retrieved chunks
QUERY = "What is the capital adequacy ratio of NMB Bank?"

def query_collection(col: chromadb.Collection, query: str, n: int = 3) -> list[str]:
    q_embed = client.embeddings.create(model=EMBED_MODEL, input=[query]).data[0].embedding
    results = col.query(query_embeddings=[q_embed], n_results=n)
    return results["documents"][0]

strategies = {
    "Fixed-size"   : col_fixed,
    "Sentence"     : col_sentence,
    "Paragraph"    : col_para,
    "Semantic"     : col_semantic,
}

print(f"Query: {QUERY}")
print("=" * 70)

retrieved = {}
for name, col in strategies.items():
    chunks_retrieved = query_collection(col, QUERY)
    retrieved[name] = chunks_retrieved
    print(f"\n── {name} ──")
    for i, c in enumerate(chunks_retrieved, 1):
        print(f"  [{i}] {c[:200].strip()}...")
```


```python
# Generate final answers for each strategy and display side-by-side
SYSTEM_PROMPT = (
    "You are a financial analyst assistant. Answer the question based on the provided context. "
    "Be concise — 2–3 sentences max. If unsure, say so."
)

def generate_answer(context_chunks: list[str], query: str) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ],
        temperature=0
    )
    return resp.choices[0].message.content

print(f"Query: {QUERY}\n")
answers = {}
for name, chunks_ret in retrieved.items():
    answers[name] = generate_answer(chunks_ret, QUERY)
    print(f"── {name} Strategy ──")
    print(textwrap.fill(answers[name], width=80))
    print()
```


```python
# Visualize: chunk count vs avg length vs answer length per strategy
all_chunks = {
    "Fixed-size" : chunks_fixed,
    "Sentence"   : chunks_sentence,
    "Paragraph"  : chunks_para,
    "Semantic"   : chunks_semantic,
}

names      = list(all_chunks.keys())
counts     = [len(v) for v in all_chunks.values()]
avg_lens   = [int(np.mean([len(c) for c in v])) for v in all_chunks.values()]
ans_lens   = [len(answers[n]) for n in names]

x = np.arange(len(names))
width = 0.28

fig, ax = plt.subplots(figsize=(10, 5))
bars1 = ax.bar(x - width, counts,   width, label="Chunk count",          color="steelblue")
bars2 = ax.bar(x,         avg_lens, width, label="Avg chunk length (chars)", color="darkorange")
bars3 = ax.bar(x + width, ans_lens, width, label="Answer length (chars)",    color="seagreen")

ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=11)
ax.set_ylabel("Value")
ax.set_title(f"Chunking Strategy Comparison\nQuery: {QUERY[:60]}...")
ax.legend()
ax.bar_label(bars1, padding=3, fontsize=9)
ax.bar_label(bars2, padding=3, fontsize=9)
ax.bar_label(bars3, padding=3, fontsize=9)
plt.tight_layout()
plt.show()
```

## When to Use Which Strategy for Financial Documents

| Question Type | Best Strategy | Reason |
|---------------|---------------|---------|
| Precise number lookup (*"What is the CAR?"*) | **Paragraph** or **Semantic** | Numbers appear in well-formed paragraphs or tables |
| Section summaries (*"Summarize MD&A"*) | **Paragraph** | Keeps narrative sections intact |
| Definition queries (*"What is Tier 1 capital?"*) | **Sentence** | Definitions often appear as standalone sentences |
| Long-form analysis | **Semantic** | Topic boundaries are respected |

**Rule of thumb for CA professionals:**  
> Use **paragraph-based** chunking as your default for narrative sections.  
> Use **fixed-size** when you need speed and predictability.  
> Use **semantic** when answer quality is critical and you can afford the extra embedding cost upfront.


```python
# Second query: Summarize the auditor's observations
# Paragraph-based chunking tends to win here because audit opinions are full paragraphs

QUERY2 = "Summarize the auditor's observations"

print(f"Query: {QUERY2}\n")
for name, col in strategies.items():
    chunks_ret = query_collection(col, QUERY2)
    answer = generate_answer(chunks_ret, QUERY2)
    print(f"── {name} Strategy ──")
    print(textwrap.fill(answer, width=80))
    print()
```
