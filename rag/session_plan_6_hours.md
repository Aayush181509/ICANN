# 6-Hour Session Plan — Generative AI & RAG for CA Professionals

**Audience.** ICAN Chartered Accountants and finance professionals, beginner-level Python.
**Format.** Hands-on, laptop-driven. ~70% live coding + practice, ~30% concepts.
**Pre-requisite.** Completed `setup_instructions.md` (Python, `.env`, `data_generation.py` ran).

> **Two breaks** built in (15 min + 15 min) plus a 30-min lunch (or move to a 5-hr compact form if no lunch). Times below assume a 09:30–16:30 day with lunch 12:30–13:00.

---

## At a glance

| Hour | Block | Notebooks | Outcome |
|---|---|---|---|
| 0 | Welcome + Setup check | 00 | Everyone's environment works |
| 1 | GenAI fundamentals + First LLM call | 01, 02 | Can talk to an LLM from Python |
| 2 | Financial data + Embeddings | 03, 04 | Can load PDFs/Excel/CSV and embed text |
| 3 | Basic RAG + Citations | 05, 06 | Working grounded Q&A on audit memos |
| 4 | Multi-doc RAG + Own-data + Limits | 07, 08, 09 | Can run RAG on participant data; knows failure modes |
| 5 | Knowledge graphs + Graph RAG | 10, 11 | Can model relationships and query them |
| 6 | Agentic RAG + Capstone + Wrap | 12, 13 | Builds a CA assistant tying it all together |

---

## Hour 0 — Welcome & Setup check (09:30 – 09:45)

* **Learning objective.** Confirm every laptop is ready.
* **Demo.** Open `00_environment_setup.ipynb`, run all cells, show ✅ marks.
* **Hands-on.** Participants run the same notebook. Instructors triage red cells.
* **Discussion.** Quick poll — who has tried ChatGPT before? Who has used Python before?

## Hour 1 — Generative AI fundamentals + First LLM call (09:45 – 10:45)

### Concepts (25 min, notebook 01)
* What is AI vs ML vs Generative AI vs LLM vs GPT — analogy: *LLM as a very fast but un-trained articled assistant who has read a lot but never audited anything*.
* Tokens, context window, temperature.
* **Hallucination** — show one live to make it real.
* Prompting patterns: role, few-shot, structured output, chain-of-thought *output* (not hidden reasoning).
* CA-specific prompts: summarise an audit memo, extract risks, draft client email, explain tax provision, convert messy notes into a checklist.

### First call (35 min, notebook 02)
* Walk through the `ask_llm()` wrapper.
* **Demo task:** ask the model to extract audit risks from one paragraph.
* **Hands-on:** participants ask three of their own questions (finance, tax, accounting).
* Structured JSON output for downstream automation.
* **Reflection.** What did the model get *wrong*? Why?

**Break — 10:45 – 11:00**

## Hour 2 — Financial data + Embeddings (11:00 – 12:00)

### Loading PDFs, Excel, CSV (25 min, notebook 03)
* `pypdf` for narrative documents (audit memo).
* `pandas.read_excel` with multiple sheets (trial balance + GL).
* `pandas.read_csv` for transactional data.
* Light cleaning: missing PAN/VAT, duplicate invoice numbers, type coercion.
* **Demo.** Find the three duplicate invoices in the purchases CSV with one line of pandas.

### Embeddings & vector search (35 min, notebook 04)
* **Analogy.** *Embeddings are like converting a sentence into a GPS coordinate of meaning — sentences about "related party loans" land near each other.*
* Semantic vs keyword search — live side-by-side comparison.
* Chunking, chunk size, chunk overlap, why they matter.
* Build a Chroma vector store over the 10 generated PDFs.
* **Hands-on.** Search "vendor approval thresholds" and "loan covenant" against the store. Inspect the top-3 chunks.

**Lunch — 12:30 – 13:00** (if HR/admin signals a slightly different schedule, push notebooks 04 → 05 either side of the break.)

## Hour 3 — Basic RAG + Citations (13:00 – 14:00)

### Build the pipeline (30 min, notebook 05)
* Pipeline diagram: *load → chunk → embed → retrieve → prompt → answer*.
* Code the four functions step by step. Highlight the prompt template that injects retrieved context.
* **Demo task.** "What are the key audit risks?" — show retrieved chunks first, then the grounded answer.

### Citations & safe refusals (30 min, notebook 06)
* Why citations matter for a CA: *evidence trail, workpaper standard, professional skepticism*.
* Add source filename + page number to the answer.
* Train the participants to spot "the model invented a citation".
* **Hands-on.** Ask a question the docs *cannot* answer ("What was the depreciation rate in 1998?") and verify the system says "no answer found".

**Break — 14:00 – 14:15**

## Hour 4 — Multi-doc RAG + Own-data + Limits (14:15 – 15:15)

### Multi-document RAG (20 min, notebook 07)
* Tag each chunk with `doc_type` metadata: `policy`, `minutes`, `ledger`, `memo`.
* Filtered retrieval — *"only look at policies"*.
* **Demo cross-document question.** "Compare loan terms in the loan agreement with the disclosures in the annual report excerpt."

### Run RAG on participant data (20 min, notebook 08)
* Participants drop their own (anonymised!) PDFs/Excels into `data/user_data/`.
* The notebook auto-detects and indexes.
* **Strong reminder.** *Do not use real client data on a public API. Use the local embedding model. Do not paste anything you would not put on a fax to a competitor.*

### Limitations & evaluation (20 min, notebook 09)
* The eight failure modes — hallucination, poor chunking, OCR on scanned PDFs, table extraction, wrong retrieval, missing metadata, outdated law, confidentiality.
* Build a 5-question eval set, grade the answers, discuss.
* **Group discussion.** Where would you *not* use this in your firm yet?

## Hour 5 — Knowledge Graphs + Graph RAG (15:15 – 16:00)

### Intro to knowledge graphs (20 min, notebook 10)
* Nodes / edges / relationships explained on a whiteboard.
* CA-friendly examples — *Vendor → issued → Invoice → approved-by → Employee*.
* Build a small graph in NetworkX from the vendor master + purchases CSV.
* Three queries: all transactions for a vendor, employees approving > NPR 5,00,000, related party paths.

### Graph RAG (25 min, notebook 11)
* When relationships matter more than text similarity (e.g. *"who approved the payment to a related party?"*).
* Extract entities from documents, link to the graph, retrieve graph neighbourhood as context.
* **Demo.** A question that **basic RAG misses** but **Graph RAG answers correctly**.

## Hour 6 — Agentic RAG + Capstone + Wrap (16:00 – 16:30 with a soft overrun)

### Agentic RAG intro (15 min, notebook 12)
* Tools = "buttons the AI can press". Planner + retriever + calculator + spreadsheet tool + graph tool.
* Walk through one agent run. Show the trace — *thought → tool → observation → next thought*.

### Capstone (10 min walk-through, notebook 13)
* Pick **one** capstone scenario:
  1. Audit risk assistant
  2. Tax compliance Q&A
  3. Financial statement review
  4. Internal control review
  5. Related party transaction assistant
* The notebook produces a short professional-style report with citations and a *limitations* footer.

### Wrap-up + professional safeguards (5 min)
* The five non-negotiables (verify, judgment, confidentiality, official sources, RAG ≠ correctness).
* Where to go next: longer notebooks, NRB circulars dataset, your own firm's policy corpus, evaluation harness.
* Feedback form, group photo.

---

## What to demo live (the high-impact moments)

1. **The hallucination** in notebook 01. Makes the rest of the day feel real.
2. **Find duplicate invoices in 5 seconds** with pandas in notebook 03.
3. **Semantic vs keyword** side-by-side in notebook 04.
4. **Cite-the-page** answer in notebook 06.
5. **The cross-document inconsistency** discovered in notebook 07.
6. **A question basic RAG misses, Graph RAG nails** in notebook 11.
7. **The agent trace** in notebook 12.

## Common live-class hazards & mitigations

| Hazard | Mitigation |
|---|---|
| Venue Wi-Fi dies during embeddings | Use the `local` embedding provider — fully offline. |
| API quota exhausted mid-class | Switch `LLM_PROVIDER` to `mock` in `.env`. All retrieval still demos. |
| Participant's laptop too slow for Chroma | The notebooks fall back to an in-memory FAISS store. |
| Someone uploads real client data | Stop, delete, restart kernel, repeat the safeguard reminder. |

## After the session — suggested follow-ups

* A 2-hour advanced workshop on **evaluation** (RAGAS, hit-rate, faithfulness).
* A 2-hour deep dive on **table-aware RAG** (Unstructured.io, Camelot for scanned tax returns).
* A 1-hour clinic on **on-premise deployment** (Ollama + local Llama) for confidential client data.
* A study group reading NRB circulars + ICAI/ICAN guidance into the corpus.
