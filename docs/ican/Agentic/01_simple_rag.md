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
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# Initialize OpenAI client
# Set your API key: export OPENAI_API_KEY="sk-..."
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("Libraries loaded successfully.")
```

    Libraries loaded successfully.



```python
# ── Setup check: verify the sample PDFs are in place ─────────────────────────
# If you have not yet generated the sample data, this cell runs the generator
# for you. Real-world workshops should swap these for actual annual reports.

import os, subprocess, sys
from pathlib import Path

DATA_DIR = Path("../data").resolve()
REQUIRED_PDFS = [
    DATA_DIR / "annual_reports" / "nmb_bank_annual_report_2023.pdf",
    DATA_DIR / "annual_reports" / "nmb_bank_annual_report_2022.pdf",
    DATA_DIR / "annual_reports" / "nepal_telecom_annual_report_2023.pdf",
    DATA_DIR / "financial_statements" / "nmb_bank_financials_2023.pdf",
    DATA_DIR / "financial_statements" / "nepal_telecom_financials_2023.pdf",
]

missing = [p for p in REQUIRED_PDFS if not p.exists()]
if missing:
    print(f"Missing {len(missing)} PDF(s). Running data generator...")
    gen = DATA_DIR / "generate_sample_data.py"
    subprocess.run([sys.executable, str(gen)], check=True, cwd=str(DATA_DIR))
    print()

print("Data ready:")
for p in REQUIRED_PDFS:
    size_kb = p.stat().st_size // 1024 if p.exists() else 0
    print(f"  {'OK' if p.exists() else 'MISSING':7s}  {p.name:50s}  {size_kb} KB")

if not os.environ.get("OPENAI_API_KEY"):
    print("\nWARNING: OPENAI_API_KEY is not set. Export it before running the rest of this notebook.")

```

    Data ready:
      OK       nmb_bank_annual_report_2023.pdf                     11 KB
      OK       nmb_bank_annual_report_2022.pdf                     6 KB
      OK       nepal_telecom_annual_report_2023.pdf                8 KB
      OK       nmb_bank_financials_2023.pdf                        7 KB
      OK       nepal_telecom_financials_2023.pdf                   8 KB



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

    Total pages extracted : 5
    Total characters      : 7,406
    
    --- Preview of first 800 characters ---
    NMB Bank Limited
    Annual Report — Fiscal Year 2022/23 (FY2023)
    Registered Office: Babarmahal, Kathmandu, Nepal  |  Company Registration No.: 25478/064/065  |  Listed on: Nepal
    Stock Exchange (NEPSE) — Symbol: NMB
    This is a synthetic document created for the ICAN GenAI training workshop. All figures, names, and events are
    fictional and used only for educational demonstration of RAG and Knowledge Graph techniques.
    Chairperson's Statement
    On behalf of the Board of Directors, I am pleased to present the Annual Report of NMB Bank Limited
    for the fiscal year 2022/23. Despite a challenging macroeconomic environment characterised by
    tightening liquidity and elevated interest rates, NMB Bank delivered another year of resilient
    performance. Net profit grew by 9.8 percent year-on-year, total deposits 


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
# Show a middle chunk (handles both small synthetic data and large real reports)
middle_idx = min(10, len(chunks) - 1) if len(chunks) > 1 else 0
print(f"--- Sample Chunk (chunk {middle_idx}) ---")
print(textwrap.fill(chunks[middle_idx], width=90))

```

    Total chunks created  : 5
    Average chunk length  : 1647 characters
    
    --- Sample Chunk (first chunk) ---
    NMB Bank Limited Annual Report — Fiscal Year 2022/23 (FY2023) Registered Office:
    Babarmahal, Kathmandu, Nepal  |  Company Registration No.: 25478/064/065  |  Listed on:
    Nepal Stock Exchange (NEPSE) — Symbol: NMB This is a synthetic document created for the
    ICAN GenAI training workshop. All figures, names, and events are fictional and used only
    for educational demonstration of RAG and Knowledge Graph techniques. Chairperson's
    Statement On behalf of the Board of Directors, I am pleased to present the Annual Report
    of NMB Bank Limited for the fiscal year 2022/23. Despite a challenging macroeconomic
    environment characterised by tightening liquidity and elevated interest rates, NMB Bank
    delivered another year of resilient performance. Net profit grew by 9.8 percent year-on-
    year, total deposits crossed NPR 250 billion, and our capital adequacy ratio remained well
    above the regulatory minimum at 13.2 percent. During the year, the Bank continued to
    expand its branch and digital footprint, opening 14 new branches across the Karnali and
    Sudurpaschim provinces. We also completed the acquisition of a majority stake in NMB
    Microfinance Bittiya Sanstha, taking our ownership to 70.0 percent, and re-affirmed our
    51.0 percent stake in NMB Capital Limited. — Ram Bahadur Khatri, Chairperson Board of
    Directors (As at Ashadh 31, 2080 / 15 July 2023) Name Designation Appointed Ram Bahadur
    Khatri Chairperson 2018 Sunita Sharma Director (Independent) 2020 Pradeep K. Joshi
    Director 2019 Anjali Pradhan Director (Independent) 2021 Bibek Rana Director 2022 Sushil
    Bhatta Chief Executive Officer 2017 Manish Timalsina Chief Financial Officer 2019
    Financial Highlights — FY2023 (NPR in Millions) Metric FY2023 FY2022 Change % Total Assets
    298,420 274,310 +8.79% Total Deposits 251,640 230,180 +9.32% Loans and Advances 212,890
    197,420
    
    --- Sample Chunk (chunk 4) ---
    ate enhanced whistleblower protections. Dividend and Capital Distribution The Board has
    recommended a cash dividend of 11.0 percent and a bonus share issue of 4.5 percent on
    paid-up capital, subject to approval at the Annual General Meeting. Total distribution
    equates to NPR 2,418 million, representing 57.8 percent of net profit for FY2023.



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

    Embedding chunks... (this may take 30–60 seconds for a large report)
      Embedded batch 1 (5 chunks)
    
    Embedding dimensions : 1536
    First 10 values of embedding[0]: [0.01540374755859375, 0.0177001953125, 0.07757568359375, -0.015350341796875, -0.0249176025390625, 0.0269317626953125, -0.0006256103515625, 0.058135986328125, -0.0193939208984375, -0.00856781005859375]



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

    Stored 5 chunks in ChromaDB.


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

    Query: What was NMB Bank's net profit in FY2023?
    ======================================================================
    Retrieved Chunks:
      [1] NMB Bank Limited
    Annual Report — Fiscal Year 2022/23 (FY2023)
    Registered Office: Babarmahal, Kathmandu, Nepal  |  Company Registration No.: 25478/064/065  |  Listed on: Nepal
    Stock Exchange (NEPSE) —...
      [2] guidelines and the proposed
    Banks and Financial Institutions Act (BAFIA) amendments may affect lending margins in FY2024.
    Independent Auditor's Report
    To the Shareholders of NMB Bank Limited:
    We have...
      [3] 2
    Change %
    Total Assets
    298,420
    274,310
    +8.79%
    Total Deposits
    251,640
    230,180
    +9.32%
    Loans and Advances
    212,890
    197,420
    +7.84%
    Total Equity
    32,150
    29,640
    +8.47%
    Net Interest Income
    11,820
    10,440
    +13.2...
      [4] 2.41 percent from 2.18 percent the previous year,
    primarily attributable to stress in the tourism and trading portfolios in the first half of the fiscal year.
    Provision coverage was strengthened to 1...
      [5] ate enhanced whistleblower protections.
    Dividend and Capital Distribution
    The Board has recommended a cash dividend of 11.0 percent and a bonus share issue of 4.5 percent
    on paid-up capital, subject t...
    ======================================================================
    Answer:
    NMB Bank's net profit in FY2023 was NPR 4,184 million.
    





    "NMB Bank's net profit in FY2023 was NPR 4,184 million."




```python
# Query 2: What are the key risk factors mentioned in the annual report?
rag_answer("What are the key risk factors mentioned in the annual report?")
```

    Query: What are the key risk factors mentioned in the annual report?
    ======================================================================
    Retrieved Chunks:
      [1] 2.41 percent from 2.18 percent the previous year,
    primarily attributable to stress in the tourism and trading portfolios in the first half of the fiscal year.
    Provision coverage was strengthened to 1...
      [2] guidelines and the proposed
    Banks and Financial Institutions Act (BAFIA) amendments may affect lending margins in FY2024.
    Independent Auditor's Report
    To the Shareholders of NMB Bank Limited:
    We have...
      [3] NMB Bank Limited
    Annual Report — Fiscal Year 2022/23 (FY2023)
    Registered Office: Babarmahal, Kathmandu, Nepal  |  Company Registration No.: 25478/064/065  |  Listed on: Nepal
    Stock Exchange (NEPSE) —...
      [4] 2
    Change %
    Total Assets
    298,420
    274,310
    +8.79%
    Total Deposits
    251,640
    230,180
    +9.32%
    Loans and Advances
    212,890
    197,420
    +7.84%
    Total Equity
    32,150
    29,640
    +8.47%
    Net Interest Income
    11,820
    10,440
    +13.2...
      [5] ate enhanced whistleblower protections.
    Dividend and Capital Distribution
    The Board has recommended a cash dividend of 11.0 percent and a bonus share issue of 4.5 percent
    on paid-up capital, subject t...
    ======================================================================
    Answer:
    The key risk factors mentioned in the annual report are:
    
    1. Credit Risk: Concentration in the hydropower and real estate sectors.
    2. Liquidity Risk: Tightness in interbank markets causing short-term funding costs to spike.
    3. Foreign Exchange Risk: Dependence on imports and remittance inflows.
    4. Cyber and Operational Risk: Investment in cybersecurity and core banking upgrades.
    5. Regulatory Risk: Anticipated changes to working capital lending guidelines and proposed BAFIA amendments.
    





    'The key risk factors mentioned in the annual report are:\n\n1. Credit Risk: Concentration in the hydropower and real estate sectors.\n2. Liquidity Risk: Tightness in interbank markets causing short-term funding costs to spike.\n3. Foreign Exchange Risk: Dependence on imports and remittance inflows.\n4. Cyber and Operational Risk: Investment in cybersecurity and core banking upgrades.\n5. Regulatory Risk: Anticipated changes to working capital lending guidelines and proposed BAFIA amendments.'




```python
# Query 3: Who are the members of the board of directors?
rag_answer("Who are the members of the board of directors?")
```

    Query: Who are the members of the board of directors?
    ======================================================================
    Retrieved Chunks:
      [1] guidelines and the proposed
    Banks and Financial Institutions Act (BAFIA) amendments may affect lending margins in FY2024.
    Independent Auditor's Report
    To the Shareholders of NMB Bank Limited:
    We have...
      [2] ate enhanced whistleblower protections.
    Dividend and Capital Distribution
    The Board has recommended a cash dividend of 11.0 percent and a bonus share issue of 4.5 percent
    on paid-up capital, subject t...
      [3] NMB Bank Limited
    Annual Report — Fiscal Year 2022/23 (FY2023)
    Registered Office: Babarmahal, Kathmandu, Nepal  |  Company Registration No.: 25478/064/065  |  Listed on: Nepal
    Stock Exchange (NEPSE) —...
      [4] 2.41 percent from 2.18 percent the previous year,
    primarily attributable to stress in the tourism and trading portfolios in the first half of the fiscal year.
    Provision coverage was strengthened to 1...
      [5] 2
    Change %
    Total Assets
    298,420
    274,310
    +8.79%
    Total Deposits
    251,640
    230,180
    +9.32%
    Loans and Advances
    212,890
    197,420
    +7.84%
    Total Equity
    32,150
    29,640
    +8.47%
    Net Interest Income
    11,820
    10,440
    +13.2...
    ======================================================================
    Answer:
    The members of the Board of Directors of NMB Bank Limited are:
    
    1. Ram Bahadur Khatri - Chairperson
    2. Sunita Sharma - Director (Independent)
    3. Pradeep K. Joshi - Director
    4. Anjali Pradhan - Director (Independent)
    5. Bibek Rana - Director
    6. Sushil Bhatta - Chief Executive Officer
    7. Manish Timalsina - Chief Financial Officer
    





    'The members of the Board of Directors of NMB Bank Limited are:\n\n1. Ram Bahadur Khatri - Chairperson\n2. Sunita Sharma - Director (Independent)\n3. Pradeep K. Joshi - Director\n4. Anjali Pradhan - Director (Independent)\n5. Bibek Rana - Director\n6. Sushil Bhatta - Chief Executive Officer\n7. Manish Timalsina - Chief Financial Officer'



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
