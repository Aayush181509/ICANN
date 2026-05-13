# Section 01: Simple RAG on Financial Documents

**Duration:** ~60 minutes  
**Goal:** Build a complete pipeline that reads a PDF annual report and answers financial questions about it.

---

## What is RAG?

**RAG** stands for **Retrieval-Augmented Generation**.

Think of it like an **open-book exam**:

> You give a brilliant student (GPT-4o-mini) a very specific textbook they have never read before (your annual report PDF). During the exam, they can look up relevant pages before answering.

Without RAG, the AI only knows what it learned during training — it has no idea what NMB Bank's FY2023 net profit was.  
With RAG, we **retrieve** the relevant pages from your document first, then **generate** an answer using those pages as context.

**Why not just paste the whole document into the AI?**  
Annual reports are 200–400 pages. LLMs have limits on how much text they can process at once. RAG solves this by retrieving only the relevant portions.

## The RAG Pipeline

Here is what we will build today:

```
PDF Document
     │
     ▼
 Text Extraction (pypdf)
     │
     ▼
 Fixed-Size Chunking (500 tokens, 50 overlap)
     │
     ▼
 Embedding (text-embedding-3-small)
     │
     ▼
 ChromaDB (Vector Store)
     │
     ▼
 User Query ──► Query Embedding ──► Similarity Search ──► Top-K Chunks
                                                               │
                                                               ▼
                                                   GPT-4o-mini (with context)
                                                               │
                                                               ▼
                                                          Final Answer
```

**Each step explained:**

| Step | What it does | Analogy |
|------|--------------|---------|
| Text Extraction | Convert PDF to raw text | Photocopying pages of the book |
| Chunking | Split text into manageable pieces | Tearing out individual pages |
| Embedding | Convert each chunk to a number vector | Giving each page a GPS coordinate based on its meaning |
| Vector Store | Index all the vectors | Building a map of the book |
| Similarity Search | Find chunks closest to the query | Navigating the map to find relevant pages |
| Generation | Feed retrieved chunks to GPT + get answer | The student reads the relevant pages and writes the answer |


```python
# Install required libraries (run once)
# !pip install openai chromadb pypdf tiktoken

import os
import re
import textwrap

import chromadb
import tiktoken
from openai import OpenAI
from pypdf import PdfReader

# Initialize OpenAI client
# Set your API key: export OPENAI_API_KEY="sk-..."
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Libraries loaded successfully.")
```


```python
# Load the PDF and extract raw text
PDF_PATH = "../data/annual_reports/nmb_bank_annual_report_2023.pdf"

reader = PdfReader(PDF_PATH)
pages = [page.extract_text() or "" for page in reader.pages]
full_text = "\n".join(pages)

print(f"Total pages extracted : {len(pages)}")
print(f"Total characters      : {len(full_text):,}")
print()
print("--- Preview of first 800 characters ---")
print(full_text[:800])
```

## Why Chunking?

The NMB Bank annual report has hundreds of pages. GPT-4o-mini can only read ~16,000 tokens at once — that is roughly 12,000 words, or about 25 pages.

Even if we could fit everything, it is expensive and slow. More importantly, the answer to *"What was the net profit?"* is usually in just 1–2 paragraphs. Sending all 300 pages is wasteful.

**Chunking** solves this by splitting the document into small, overlapping pieces. The overlap ensures we do not accidentally cut off a sentence that spans two chunks.

```
Full Document: [AAAAAAAAABBBBBBBBBCCCCCCCCC]

Chunks (500 tokens, 50 overlap):
  Chunk 1: [AAAAAAAAAB]
  Chunk 2:         [ABBBBBBBBC]       ← 50-token overlap
  Chunk 3:                 [BCCCCCCCCC]
```


```python
# Fixed-size chunking: 500 tokens per chunk, 50 token overlap
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
ENCODING = "cl100k_base"  # tokenizer used by text-embedding-3-small and GPT-4o

enc = tiktoken.get_encoding(ENCODING)

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    tokens = enc.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(enc.decode(chunk_tokens))
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(full_text)

print(f"Total chunks created  : {len(chunks)}")
print(f"Average chunk length  : {sum(len(c) for c in chunks) // len(chunks)} characters")
print()
print("--- Sample Chunk (first chunk) ---")
print(textwrap.fill(chunks[0], width=90))
print()
print("--- Sample Chunk (chunk 10) ---")
print(textwrap.fill(chunks[10], width=90))
```


```python
# Embed chunks using OpenAI text-embedding-3-small
# This converts each chunk into a 1536-dimensional vector

EMBED_MODEL = "text-embedding-3-small"

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts in batches of 100."""
    all_embeddings = []
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        response = client.embeddings.create(model=EMBED_MODEL, input=batch)
        all_embeddings.extend([item.embedding for item in response.data])
        print(f"  Embedded batch {i // batch_size + 1} ({len(batch)} chunks)")
    return all_embeddings

print("Embedding chunks... (this may take 30–60 seconds for a large report)")
embeddings = embed_texts(chunks)

print(f"\nEmbedding dimensions : {len(embeddings[0])}")
print(f"First 10 values of embedding[0]: {embeddings[0][:10]}")
```


```python
# Store chunks and embeddings in ChromaDB (in-memory vector store)
# ChromaDB lets us search for the most semantically similar chunks to a query

chroma_client = chromadb.Client()  # in-memory — no disk setup needed

# Create a collection (like a table in a database)
collection = chroma_client.create_collection(
    name="nmb_annual_report_2023",
    metadata={"hnsw:space": "cosine"}  # use cosine similarity
)

# Add all chunks with their embeddings
collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print(f"Stored {collection.count()} chunks in ChromaDB.")
```

## How Similarity Search Works

When you ask a question, we convert it to an embedding vector (same process as the chunks). Then we find the chunks whose vectors are *closest* to the question vector.

**Cosine similarity** measures the angle between two vectors. Vectors pointing in the same direction (same topic) have a cosine similarity close to **1.0**. Vectors pointing in opposite directions (very different topics) have similarity close to **0.0** or negative.

```
Query: "What was net profit?"
   Vector: [0.12, -0.34, 0.78, ...]   ← 1536 numbers

Chunk A: "Net profit for FY2023 was NPR 2.3 billion..."
   Vector: [0.11, -0.33, 0.76, ...]   ← very similar direction → high score

Chunk B: "The board approved 3 new branch openings..."
   Vector: [0.45, 0.12, -0.23, ...]   ← different direction → low score
```

ChromaDB returns the top-K chunks by cosine similarity — no manual keyword matching needed.


```python
# Query 1: What was NMB Bank's net profit in FY2023?

def rag_answer(query: str, n_results: int = 5) -> str:
    # Step 1: Embed the query
    query_embedding = client.embeddings.create(
        model=EMBED_MODEL, input=[query]
    ).data[0].embedding

    # Step 2: Retrieve top-K most similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    retrieved_chunks = results["documents"][0]

    # Step 3: Build context and send to GPT-4o-mini
    context = "\n\n---\n\n".join(retrieved_chunks)
    system_prompt = (
        "You are a financial analyst assistant. Answer the question based strictly on the "
        "provided context from NMB Bank's annual report. If the answer is not in the context, "
        "say so clearly. Be concise and precise."
    )
    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        temperature=0
    )
    answer = response.choices[0].message.content

    # Display retrieved chunks
    print(f"Query: {query}")
    print("=" * 70)
    print("Retrieved Chunks:")
    for i, chunk in enumerate(retrieved_chunks, 1):
        print(f"  [{i}] {chunk[:200].strip()}...")
    print("=" * 70)
    print(f"Answer:\n{answer}")
    print()
    return answer

rag_answer("What was NMB Bank's net profit in FY2023?")
```


```python
# Query 2: What are the key risk factors mentioned in the annual report?
rag_answer("What are the key risk factors mentioned in the annual report?")
```


```python
# Query 3: Who are the members of the board of directors?
rag_answer("Who are the members of the board of directors?")
```

## What RAG Can and Cannot Do

### RAG excels at:
- **Fact lookup** from a specific document ("What was the net profit?")
- **Summarizing** a specific section ("Summarize the MD&A")
- **Simple comparisons** within one document

### RAG struggles with:
- **Multi-hop questions** — *"Compare NMB Bank's profit growth to Nepal Telecom's across 2022 and 2023"*  
  → Requires connecting information across 3 documents and multiple relationships
- **Counting** — *"How many branches were opened?"*  
  → If the answer is spread across 5 different chunks, RAG may miss some
- **Relationship queries** — *"Which subsidiaries did NMB Bank acquire after FY2022?"*  
  → Requires structured relationship knowledge, not just text similarity

### What we will build next:
| Section | Addresses Which Limitation |
|---------|---------------------------|
| 02: Chunking Strategies | Improves retrieval quality |
| 03–04: Knowledge Graphs | Handles relationships and multi-document connections |
| 05: GraphRAG | Combines both — answers multi-hop questions |
| 06: Agentic RAG | Adds reasoning and tool selection |

---

> **Key takeaway:** RAG is powerful for document Q&A, but the quality of your answers depends heavily on how you prepare and retrieve the document chunks. We explore this next.
