# Gen AI in Financial Analysis — ICAN Workshop

A full-day workshop for CA professionals covering RAG, Knowledge Graphs, GraphRAG, and Agentic AI applied to Nepali financial documents.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Neo4j Desktop | 5.x |
| OpenAI API Key | — |

---

## Setup Instructions

### 1. Clone and install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your OpenAI API key
```bash
export OPENAI_API_KEY="sk-..."
```
On Windows:
```cmd
set OPENAI_API_KEY=sk-...
```

### 3. Set up Neo4j (required for Sections 03–06)
- Download Neo4j Desktop: https://neo4j.com/download/
- Create a new project and add a local DBMS
- Name the database: `ican-finance`
- Set the password to: `icandemo123`
- Start the database before running notebooks 03–06

### 4. Prepare the PDF datasets

The notebooks reference 5 PDFs under `data/`. You have two options:

**Option A — Use the included synthetic data (fastest, recommended for class)**

```bash
cd data && python generate_sample_data.py
```

This produces realistic but **fictional** Nepali financial PDFs covering
NMB Bank (FY2022 & FY2023) and Nepal Telecom (FY2023), wired so that all six
notebooks (chunking, entity extraction, year-over-year comparison, agent
ratio computation) demonstrate cleanly end-to-end. The first cell of each
notebook will also run this generator automatically if the PDFs are missing.

**Option B — Use real annual reports**

Replace the generated files with downloads from the issuers' investor relations
pages. The notebooks key off the exact filenames below, so keep them the same:

```
data/
├── annual_reports/
│   ├── nmb_bank_annual_report_2023.pdf       ← NMB Bank AR FY2023
│   ├── nmb_bank_annual_report_2022.pdf       ← NMB Bank AR FY2022
│   └── nepal_telecom_annual_report_2023.pdf  ← Nepal Telecom AR FY2023
└── financial_statements/
    ├── nmb_bank_financials_2023.pdf          ← NMB Bank financial statements FY2023
    └── nepal_telecom_financials_2023.pdf     ← Nepal Telecom financial statements FY2023
```

Sources (real data):
- NMB Bank: https://www.nmb.com.np/investor-relations
- Nepal Telecom: https://www.ntc.net.np/investors

> Real reports are 200–400 pages each; embedding + Neo4j extraction will be
> slower and noisier than the synthetic set during a live classroom demo.

### 5. Pre-populate Neo4j (run the day before)
To avoid live delays during the workshop, pre-run cells 1–8 of `03_knowledge_graph_intro.ipynb`.

### 6. Verify all notebooks run end-to-end
```
Kernel → Restart & Run All
```
on each of the 6 notebooks.

---

## Workshop Curriculum

| # | Notebook | Topic | Duration |
|---|----------|-------|----------|
| 1 | `01_simple_rag.ipynb` | Simple RAG on Financial Documents | ~60 min |
| 2 | `02_chunking_strategies.ipynb` | Chunking Strategies Comparison | ~60 min |
| 3 | `03_knowledge_graph_intro.ipynb` | Knowledge Graph Basics in Neo4j | ~75 min |
| 4 | `04_multi_doc_knowledge_graph.ipynb` | Linking Financial Documents via KG | ~60 min |
| 5 | `05_graphrag_pipeline.ipynb` | GraphRAG Pipeline | ~75 min |
| 6 | `06_agentic_rag_langgraph.ipynb` | Agentic RAG with LangGraph | ~90 min |

**Total:** ~7 hours (with breaks)

---

## Pre-Workshop Checklist

- [ ] Python 3.11+ installed
- [ ] `pip install -r requirements.txt` completed successfully
- [ ] `OPENAI_API_KEY` environment variable set
- [ ] Neo4j Desktop installed, database `ican-finance` created, password `icandemo123`
- [ ] All 5 PDFs present under `data/` — either run `python data/generate_sample_data.py` or drop in real reports
- [ ] Run cells 1–8 of `03_knowledge_graph_intro.ipynb` to pre-populate Neo4j
- [ ] Run `Kernel → Restart & Run All` on each notebook — all should complete without errors
- [ ] Reset Neo4j between dry runs: `utils/neo4j_setup.cypher`
