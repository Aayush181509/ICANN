# Gen AI in Financial Analysis — ICAN Workshop Plan
**Audience:** CA Professionals (no coding background)
**Format:** Jupyter Notebooks — instructor runs, audience follows along
**Duration:** Full-day workshop (6–8 hours)
**LLM:** OpenAI GPT-4o / GPT-4o-mini
**Dataset:** Nepal bank annual reports (PDF) + financial statements (PDF)

---

## Curriculum Overview

| # | Section | Notebook | Core Concept | Duration |
|---|---------|----------|--------------|----------|
| 1 | Simple RAG | `01_simple_rag.ipynb` | Retrieve and answer from financial PDFs | ~60 min |
| 2 | Chunking Strategies | `02_chunking_strategies.ipynb` | How text splitting affects answer quality | ~60 min |
| 3 | Knowledge Graph Basics | `03_knowledge_graph_intro.ipynb` | Entities and relationships in Neo4j | ~75 min |
| 4 | Multi-Document Knowledge Graph | `04_multi_doc_knowledge_graph.ipynb` | Linking documents via shared entities | ~60 min |
| 5 | GraphRAG Pipeline | `05_graphrag_pipeline.ipynb` | Combining vector search + graph traversal | ~75 min |
| 6 | Agentic RAG with LangGraph | `06_agentic_rag_langgraph.ipynb` | AI agent that chooses tools to answer | ~90 min |

---

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| PDF Parsing | `pypdf` | Extract text from annual report PDFs |
| Embeddings | `openai` (`text-embedding-3-small`) | Convert text chunks to vectors |
| Vector Store | `chromadb` | Store and search embeddings (in-memory, no setup) |
| LLM | `openai` (`gpt-4o-mini`, `gpt-4o`) | Answer generation and entity extraction |
| Graph DB | `neo4j` (Desktop) + `py2neo` | Store and query knowledge graphs |
| Agent Framework | `langgraph` | Build multi-tool financial analysis agent |
| Visualization | `pyvis`, `matplotlib`, `IPython.display` | Flow diagrams, graph renders, comparison tables |
| Notebook | `jupyter` | Delivery format |

---

## Dataset

### Documents to prepare before the workshop
```
RAG/Finance/data/
├── annual_reports/
│   ├── nmb_bank_annual_report_2023.pdf
│   ├── nmb_bank_annual_report_2022.pdf
│   └── nepal_telecom_annual_report_2023.pdf
└── financial_statements/
    ├── nmb_bank_financials_2023.pdf
    └── nepal_telecom_financials_2023.pdf
```

Use publicly available annual reports from:
- NMB Bank: https://www.nmb.com.np/investor-relations
- Nepal Telecom: https://www.ntc.net.np/investors

---

## Section 01 — Simple RAG on Financial Documents
**Notebook:** `01_simple_rag.ipynb`
**Duration:** ~60 minutes

### Learning Objectives
- Understand what RAG is and why it exists (LLMs don't know your private documents)
- See a complete pipeline from PDF → answer in ~50 lines of code
- Understand the role of embeddings and vector search

### Opening Flow Diagram (rendered in notebook)
```
PDF Document
     │
     ▼
 Text Extraction (pypdf)
     │
     ▼
 Fixed-Size Chunking
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

### Notebook Structure
| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | **What is RAG?** — Plain-language analogy: *"Like giving an open-book exam to a brilliant student who has never read your specific textbook"* |
| 2 | Markdown | Flow diagram (ASCII art + explanation of each step) |
| 3 | Code | Install + import libraries |
| 4 | Code | Load PDF with `pypdf`, preview raw extracted text |
| 5 | Markdown | **Why chunking?** — LLMs have context limits, analogous to reading one page at a time |
| 6 | Code | Fixed-size chunking (500 tokens, 50 overlap), print sample chunks |
| 7 | Code | Embed chunks using OpenAI, show what an embedding vector looks like (first 10 values) |
| 8 | Code | Store in ChromaDB |
| 9 | Markdown | **How similarity search works** — cosine distance analogy |
| 10 | Code | Query 1: *"What was NMB Bank's net profit in FY2023?"* — show retrieved chunks + final answer |
| 11 | Code | Query 2: *"What are the key risk factors mentioned in the annual report?"* |
| 12 | Code | Query 3: *"Who are the members of the board of directors?"* |
| 13 | Markdown | **What RAG can and cannot do** — limitations recap |

### Key Libraries
```
openai
chromadb
pypdf
tiktoken
```

---

## Section 02 — Chunking Strategies
**Notebook:** `02_chunking_strategies.ipynb`
**Duration:** ~60 minutes

### Learning Objectives
- Understand that chunking is not trivial — it directly affects answer quality
- Compare 4 strategies on the same financial document
- See empirically which strategy works best for different question types

### Opening Flow Diagram
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

### Notebook Structure
| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | **Why chunking matters** — analogy: indexing a book by sentences vs. chapters |
| 2 | Markdown | Overview table of 4 strategies with pros/cons for financial documents |
| 3 | Code | **Strategy 1: Fixed-size** — 500 chars, 50 overlap. Show 3 sample chunks |
| 4 | Code | **Strategy 2: Sentence-based** — split on `.`, `?`, `!`. Show 3 sample chunks |
| 5 | Code | **Strategy 3: Paragraph-based** — split on `\n\n`. Show 3 sample chunks |
| 6 | Code | **Strategy 4: Semantic chunking** — embed sentences, split where cosine distance drops. Show 3 sample chunks |
| 7 | Code | Build 4 ChromaDB collections, one per strategy |
| 8 | Code | Run same query across all 4: *"What is the capital adequacy ratio of NMB Bank?"* |
| 9 | Code | Display retrieved chunks side-by-side for each strategy (styled DataFrame) |
| 10 | Code | Display final answers side-by-side |
| 11 | Code | Bar chart: chunk count vs. avg chunk length vs. answer relevance score per strategy |
| 12 | Markdown | **When to use which strategy** — financial document recommendations |
| 13 | Code | Run a second query: *"Summarize the auditor's observations"* — show how paragraph-based wins here |

### Key Libraries
```
openai
chromadb
pypdf
nltk (sentence tokenizer)
pandas
matplotlib
```

---

## Section 03 — Knowledge Graph Basics in Neo4j
**Notebook:** `03_knowledge_graph_intro.ipynb`
**Duration:** ~75 minutes

### Learning Objectives
- Understand what a knowledge graph is (nodes, edges, properties)
- Extract financial entities from an annual report using GPT-4o-mini
- Build and visualize a graph in Neo4j
- Write basic Cypher queries

### Prerequisites (setup before session)
- Neo4j Desktop installed and running locally
- Create a new database named `ican-finance`
- Default password set to `icandemo123`

### Opening Concept Diagram
```
Traditional Database (Table):
┌──────────────┬───────────┬──────────────┐
│ Company      │ Metric    │ Value        │
├──────────────┼───────────┼──────────────┤
│ NMB Bank     │ Net Profit│ NPR 2.3B     │
└──────────────┴───────────┴──────────────┘

Knowledge Graph (Connected):
(NMB Bank) ──[REPORTED]──► (Net Profit: NPR 2.3B)
     │
     └──[SUBSIDIARY_OF]──► (NMB Microfinance)
     │
     └──[AUDITED_BY]──► (Deloitte Haskins & Sells)
     │
     └──[CHAIRED_BY]──► (Person: Ram Bahadur Khatri)
```

### Notebook Structure
| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | **What is a Knowledge Graph?** — Plain-language explanation, newspaper analogy |
| 2 | Markdown | Graph vs. table — when graph wins (relationship queries) |
| 3 | Code | Connect to Neo4j via `py2neo` |
| 4 | Markdown | **Entity types we will extract**: Company, Person, FinancialMetric, Subsidiary, AuditFirm, Year |
| 5 | Code | GPT-4o-mini prompt to extract entities from 2–3 pages of annual report (structured JSON output) |
| 6 | Code | Print extracted entities — show the JSON |
| 7 | Code | Create nodes in Neo4j for each entity type |
| 8 | Code | Create relationships (REPORTED_IN, SUBSIDIARY_OF, AUDITED_BY, CHAIRED_BY, FILED_FOR) |
| 9 | Code | `pyvis` HTML visualization of the graph — rendered inline in notebook |
| 10 | Code | Cypher Query 1: *"Find all subsidiaries of NMB Bank"* |
| 11 | Code | Cypher Query 2: *"Who audited this company and in which year?"* |
| 12 | Code | Cypher Query 3: *"Show all financial metrics reported for FY2023"* |
| 13 | Markdown | **What Cypher reads like** — SQL analogy for CA professionals |
| 14 | Code | Show Neo4j Browser screenshot (pre-captured or live) |

### Entity Schema
```
Nodes:
  (:Company {name, type, registration_no})
  (:Person {name, designation})
  (:FinancialMetric {name, value, unit, period})
  (:Subsidiary {name, ownership_pct})
  (:AuditFirm {name})
  (:Year {value})

Relationships:
  (Company)-[:REPORTED]->(FinancialMetric)
  (Company)-[:SUBSIDIARY_OF]->(Subsidiary)
  (Company)-[:AUDITED_BY]->(AuditFirm)
  (Company)-[:CHAIRED_BY]->(Person)
  (Company)-[:FILED_FOR]->(Year)
```

### Key Libraries
```
openai
py2neo
pyvis
```

---

## Section 04 — Linking Financial Documents via Knowledge Graphs
**Notebook:** `04_multi_doc_knowledge_graph.ipynb`
**Duration:** ~60 minutes

### Learning Objectives
- Scale the graph from 1 document to 3 documents
- Understand entity resolution (same entity across multiple documents)
- See cross-document relationships and multi-year trends in the graph

### Opening Flow Diagram
```
NMB Bank AR 2022 ──► Entity Extraction ──┐
                                          │
NMB Bank AR 2023 ──► Entity Extraction ──┼──► Entity Resolution ──► Unified Graph
                                          │         (merge same entities)
Nepal Telecom AR 2023 ► Entity Extraction ──┘

Cross-document edges:
(NMB Bank FY2022) ──[YEAR_OVER_YEAR]──► (NMB Bank FY2023)
(Net Profit 2022) ──[PRIOR_YEAR_OF]──► (Net Profit 2023)
```

### Notebook Structure
| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | **The multi-document problem** — why connecting documents matters for CA work (trend analysis, cross-entity comparison) |
| 2 | Code | Load all 3 PDFs, run entity extraction on each, store results |
| 3 | Markdown | **Entity resolution** — why "NMB Bank" in doc 1 and "NMB Bank Ltd." in doc 2 are the same node |
| 4 | Code | GPT-4o-mini prompt for entity normalization (canonical name resolution) |
| 5 | Code | Merge entities across documents — `MERGE` in Cypher (create if not exists, update if exists) |
| 6 | Code | Add `SOURCE_DOC` property to each node (which document it came from) |
| 7 | Code | Add cross-document relationships: `YEAR_OVER_YEAR`, `PRIOR_YEAR_OF`, `REPORTED_IN` |
| 8 | Code | `pyvis` visualization — nodes color-coded by source document |
| 9 | Code | Cypher traversal: *"Show all financial metrics for NMB Bank across both years"* |
| 10 | Code | Cypher comparison: *"Which company has higher total assets in FY2023 — NMB Bank or Nepal Telecom?"* |
| 11 | Code | Show the connected subgraph for the cross-year NMB Bank query as a rendered visualization |
| 12 | Markdown | **What this enables** — audit trail, year-over-year analysis, inter-company comparison |

### Key Libraries
```
openai
py2neo
pyvis
pandas
```

---

## Section 05 — GraphRAG Pipeline
**Notebook:** `05_graphrag_pipeline.ipynb`
**Duration:** ~75 minutes

### Learning Objectives
- Understand why RAG alone fails for multi-hop relational questions
- Combine vector search (ChromaDB) and graph traversal (Neo4j) into one pipeline
- See empirically when GraphRAG outperforms plain RAG

### Opening Flow Diagram
```
User Query
     │
     ├──────────────────────┬──────────────────────┐
     ▼                      ▼                      │
Query Embedding      Entity Detection           (parallel)
     │               (GPT-4o-mini)                 │
     ▼                      │                      │
ChromaDB Search      Neo4j Cypher Query            │
(semantic similarity) (graph traversal)            │
     │                      │                      │
     └──────────┬───────────┘                      │
                ▼                                  │
        Context Merging                            │
        (deduplicate, rank)                        │
                │                                  │
                ▼                                  │
          GPT-4o (final answer)                    │
                │                                  │
                ▼                                  │
           Final Answer ◄─────────────────────────┘
```

### Notebook Structure
| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | **The limitation of RAG** — multi-hop questions it cannot answer alone |
| 2 | Markdown | **What GraphRAG adds** — structured relationship context from the graph |
| 3 | Code | Load ChromaDB from Section 02 (best chunking strategy) and Neo4j from Section 04 |
| 4 | Code | Build `rag_retrieve(query)` function — returns top-5 chunks |
| 5 | Code | Build `graph_retrieve(query)` function — extracts entities from query, runs Cypher, returns structured context |
| 6 | Code | Build `graphrag_answer(query)` function — merges both, sends to GPT-4o |
| 7 | Code | **Demo Query 1:** *"What was NMB Bank's net profit in FY2023?"* — RAG-only vs GraphRAG side-by-side |
| 8 | Code | **Demo Query 2:** *"Compare NMB Bank's asset growth from FY2022 to FY2023 and identify its auditor"* — multi-hop, graph wins |
| 9 | Code | **Demo Query 3:** *"Which subsidiaries of NMB Bank were mentioned across both annual reports?"* |
| 10 | Code | Comparison table: Question × Method × Answer Quality (manually annotated) |
| 11 | Code | Visualization: bar chart of context tokens contributed by RAG vs Graph for each query |
| 12 | Markdown | **When to use GraphRAG** — guidance for CA professionals building financial analysis tools |

### Key Libraries
```
openai
chromadb
py2neo
pandas
matplotlib
```

---

## Section 06 — Agentic RAG with LangGraph
**Notebook:** `06_agentic_rag_langgraph.ipynb`
**Duration:** ~90 minutes

### Learning Objectives
- Understand what an AI agent is (LLM + tools + decision loop)
- See how a financial analysis agent decides which tool to use for which question
- Visualize the agent's state graph and observe step-by-step execution traces

### Opening Concept Diagram
```
                    ┌─────────────────────┐
                    │   Financial Agent   │
                    │   (LangGraph)       │
                    └─────────┬───────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼               ▼
        rag_search      graph_query    ratio_calculator  doc_summarizer
     (ChromaDB vector  (Neo4j Cypher  (compute liquidity/ (summarize a
      similarity)       traversal)    profitability ratios) full section)
```

### Agent State Graph (LangGraph nodes)
```
[START]
   │
   ▼
[Planner] — reads the user question, breaks into sub-tasks
   │
   ▼
[Tool Selector] — decides which tool(s) to call
   │
   ├──► [RAG Search Tool]
   ├──► [Graph Query Tool]
   ├──► [Ratio Calculator Tool]
   └──► [Doc Summarizer Tool]
              │
              ▼
        [Synthesizer] — combines tool outputs into coherent answer
              │
              ▼
           [Output]
              │
         (loop back if incomplete)
```

### Notebook Structure
| Cell | Type | Content |
|------|------|---------|
| 1 | Markdown | **What is an AI Agent?** — analogy: a CA using multiple reference books, calculators, and colleagues to answer one question |
| 2 | Markdown | **LangGraph explained** — nodes = steps, edges = decisions, state = working memory |
| 3 | Code | LangGraph state graph diagram rendered via `IPython.display` (Mermaid) |
| 4 | Code | Define agent state schema (`TypedDict`) |
| 5 | Code | Define Tool 1: `rag_search` — wraps Section 02 ChromaDB retrieval |
| 6 | Code | Define Tool 2: `graph_query` — wraps Section 04 Neo4j Cypher retrieval |
| 7 | Code | Define Tool 3: `ratio_calculator` — parses numbers from context, computes current ratio / ROE / debt-equity |
| 8 | Code | Define Tool 4: `doc_summarizer` — retrieves and summarizes a named section (e.g. "MD&A") |
| 9 | Code | Build LangGraph: add nodes, add conditional edges (tool selector logic) |
| 10 | Markdown | **Workflow 1: Financial Health Analysis** |
| 11 | Code | Run: *"Analyze the financial health of NMB Bank for FY2023"* — print step-by-step agent trace |
| 12 | Code | Visualize agent execution path as highlighted state graph |
| 13 | Markdown | **Workflow 2: Cross-Company Ratio Comparison** |
| 14 | Code | Run: *"Compare the current ratio of Nepal Telecom vs NMB Bank for FY2023"* — print trace |
| 15 | Code | Visualize execution path |
| 16 | Markdown | **Workflow 3: Audit-Focused Query** |
| 17 | Code | Run: *"Summarize the auditor's key observations for NMB Bank and flag any going-concern issues"* |
| 18 | Markdown | **Where Agentic RAG goes next** — multi-agent systems, automated financial reporting |

### Key Libraries
```
openai
langgraph
langchain-openai
chromadb
py2neo
```

---

## Folder Structure (Final)

```
RAG/Finance/
├── PLAN.md                              ← this file
├── README.md                            ← setup instructions for the workshop
├── requirements.txt                     ← all Python dependencies
├── data/
│   ├── annual_reports/
│   │   ├── nmb_bank_annual_report_2023.pdf
│   │   ├── nmb_bank_annual_report_2022.pdf
│   │   └── nepal_telecom_annual_report_2023.pdf
│   └── financial_statements/
│       ├── nmb_bank_financials_2023.pdf
│       └── nepal_telecom_financials_2023.pdf
├── notebooks/
│   ├── 01_simple_rag.ipynb
│   ├── 02_chunking_strategies.ipynb
│   ├── 03_knowledge_graph_intro.ipynb
│   ├── 04_multi_doc_knowledge_graph.ipynb
│   ├── 05_graphrag_pipeline.ipynb
│   └── 06_agentic_rag_langgraph.ipynb
└── utils/
    └── neo4j_setup.cypher               ← Cypher commands to reset DB between demos
```

---

## Setup Checklist (Run Before Workshop)

- [ ] Python 3.11+ installed
- [ ] `pip install -r requirements.txt` completed
- [ ] OpenAI API key set as `OPENAI_API_KEY` environment variable
- [ ] Neo4j Desktop installed, database `ican-finance` created, password `icandemo123`
- [ ] All 5 PDFs downloaded and placed in `data/` as shown above
- [ ] Run cells 1–8 of `03_knowledge_graph_intro.ipynb` to pre-populate Neo4j (avoid live delays during session)
- [ ] Test all 6 notebooks top-to-bottom with `Kernel → Restart & Run All`

---

## requirements.txt (Draft)

```
openai>=1.30.0
chromadb>=0.5.0
pypdf>=4.0.0
tiktoken>=0.7.0
nltk>=3.8.0
py2neo>=2021.2.3
pyvis>=0.3.2
langgraph>=0.1.0
langchain-openai>=0.1.0
pandas>=2.0.0
matplotlib>=3.8.0
jupyter>=1.0.0
ipykernel>=6.0.0
```

---

## Pedagogical Notes

### For the instructor
- Each notebook opens with a **plain-language analogy** before any code — never start with code cold
- Every pipeline diagram uses ASCII art (no external image files, always renders in Jupyter)
- After each major code block, a markdown cell explains **what just happened** in non-technical terms
- Demo questions are chosen specifically because CAs will recognize them as real work they do
- Section 03 (Neo4j) requires the most setup time — do a dry run the day before

### Conceptual progression for the audience
```
Section 01: "AI can read and answer questions from our documents"
Section 02: "How we prepare the documents matters"
Section 03: "We can map relationships, not just text"
Section 04: "We can connect multiple documents into one map"
Section 05: "Combining text search + map gives better answers"
Section 06: "AI can plan and use multiple tools like a CA analyst"
```
