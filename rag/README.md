# RAG for CA Professionals — ICAN 6-Hour Training

A complete, beginner-friendly, hands-on training package on **Generative AI, Prompting, RAG, Knowledge Graphs, Graph RAG, Multi-document RAG, and Agentic RAG** — designed specifically for Chartered Accountants and finance professionals.

> **Audience.** Practising CAs and finance professionals in Nepal (ICAN) who are mostly new to Python, APIs, and AI engineering.
> **Goal.** By the end, every participant can run a working RAG system on their own audit / tax / accounting files and understand both the power and the limits of the technology.

---

## 1. What's in the box

```
rag/
├── README.md                    ← you are here
├── requirements.txt             ← minimal pip install list
├── .env.example                 ← copy to .env and fill in API keys
├── setup_instructions.md        ← step-by-step environment setup
├── session_plan_6_hours.md      ← minute-by-minute teaching plan
│
├── data/
│   ├── generated/               ← synthetic financial data (auto-generated)
│   │   ├── pdf/                 ← 10 fictional CA-style PDF documents
│   │   ├── xlsx/                ← 10 multi-sheet workbooks
│   │   ├── csv/                 ← 10 transaction-style CSVs
│   │   └── DATA_DICTIONARY.md
│   └── user_data/               ← drop your own files here for Notebook 08
│
├── notebooks/                   ← 14 teaching notebooks (00 → 13)
│
├── src/                         ← shared Python helpers
│   ├── data_generation.py
│   ├── document_loaders.py
│   ├── rag_utils.py
│   ├── graph_utils.py
│   ├── evaluation_utils.py
│   └── agentic_rag_utils.py
│
└── outputs/                     ← vector stores, graph dumps, reports
```

## 2. Quick start (10 minutes)

```bash
# 1. Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys
cp .env.example .env
#   then open .env and fill in at least one provider key

# 4. Generate the synthetic dataset (one-time, ~30 seconds)
python src/data_generation.py

# 5. Launch Jupyter
jupyter lab notebooks/
```

Start with `00_environment_setup.ipynb` and work through them in order.

## 3. Notebook map

| # | Notebook | Hour | What participants learn |
|---|---|---|---|
| 00 | Environment setup | 0 | Python, `.env`, sanity checks |
| 01 | Intro to GenAI & prompting | 1 | LLMs, tokens, hallucination, prompt patterns |
| 02 | First LLM call — simple Q&A | 1 | The `ask_llm()` wrapper, structured output |
| 03 | Loading financial data (PDF/Excel/CSV) | 2 | Reading, previewing, cleaning |
| 04 | Embeddings & vector search | 2 | Semantic vs keyword, chunking, Chroma |
| 05 | Basic RAG for CA use cases | 3 | End-to-end RAG pipeline on audit memos |
| 06 | RAG with sources & citations | 3 | Grounded answers, "I don't know" behavior |
| 07 | Multi-document RAG | 4 | Cross-document comparison & filtering |
| 08 | RAG on your own data | 4 | Drop-in folder for participant files |
| 09 | RAG limitations & evaluation | 4 | Failure modes, eval checklist |
| 10 | Intro to knowledge graphs | 5 | Nodes, edges, NetworkX |
| 11 | Graph RAG for financial docs | 5 | Entity extraction + graph retrieval |
| 12 | Agentic RAG intro | 6 | Tool-using agents, safe patterns |
| 13 | Capstone — CA assistant | 6 | Integrated audit / tax / IC reviewer |

## 4. Professional safeguards — read this before teaching

This training uses **only synthetic data**. When participants later apply these techniques to real client information:

* **AI output must always be verified** by a qualified professional.
* **AI does not replace professional judgment.** Audit conclusions, tax positions, and accounting treatments require human sign-off.
* **Confidential client data must not be uploaded to public APIs** without explicit client consent and engagement-letter authority. Prefer local embedding models or on-premise deployments when handling PII / sensitive financials.
* **RAG improves grounding, it does not guarantee correctness.** Retrieval can miss, chunking can split a critical sentence, and the LLM can still hallucinate.
* **Current laws and standards must be checked from official sources** — ICAN, NRB, Inland Revenue Department, IASB. The model's training data is frozen and may be out of date.

These reminders are repeated inside every notebook that does retrieval or generation.

## 5. Support

* If a notebook errors on a missing API key, every notebook degrades to a **mock LLM** so the rest of the lesson still runs.
* If embeddings download is slow on the venue Wi-Fi, the `sentence-transformers` model (~80 MB) can be pre-cached on USB.
* For installation problems, see `setup_instructions.md`.

Happy teaching!
