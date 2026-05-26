# Drop your own files here

Notebook `08_rag_on_participants_own_data.ipynb` auto-detects whatever you put in this folder.

**Supported formats**
* `.pdf`  — narrative documents (policies, memos, reports)
* `.xlsx` / `.xls` — workbooks (the notebook reads all sheets)
* `.csv` — transactional data
* `.txt` / `.md` — plain notes

**Folder layout (optional but recommended)**
You can either dump files flat into this folder, or create sub-folders by type:

```
user_data/
├── policies/
├── audit_memos/
├── ledgers/
└── minutes/
```

The sub-folder name is captured as `doc_type` metadata so the notebook can filter on it.

---

## ⚠️ Confidentiality reminder — read before adding files

This is a **training environment**. Before placing real files here:

1. **Anonymise** — replace company names, PANs, employee IDs.
2. **Check your engagement letter** for AI-use restrictions.
3. **Use the local embedding provider** (`EMBEDDING_PROVIDER=local` in `.env`) so no embedding text leaves the laptop.
4. **Be careful with `LLM_PROVIDER`** — if it's `openai` / `anthropic` / `google`, the retrieved chunks are sent to the provider for the answer step. Use `mock` if you only want to test retrieval.
5. Files in this folder are **ignored by git** by default. Keep it that way.

If in doubt, work on a copy of the synthetic data in `data/generated/` instead.
