# Setup Instructions — ICAN CA RAG Training

This guide walks you (and your participants) through getting a laptop ready for the 6-hour session. Allow **~20 minutes** for first-time setup.

---

## 1. Prerequisites

| Tool | Version | How to check | Where to get it |
|---|---|---|---|
| Python | 3.10 – 3.12 | `python3 --version` | <https://www.python.org/downloads/> |
| pip | latest | `pip --version` | bundled with Python |
| Git (optional) | any | `git --version` | <https://git-scm.com/> |
| A code editor | VS Code recommended | — | <https://code.visualstudio.com/> |

> **Windows users:** during Python install, tick the box **"Add Python to PATH"**.

## 2. Create a clean virtual environment

A virtual environment keeps the training libraries isolated from your system Python.

```bash
# Move into the project folder
cd rag

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Your prompt should now start with `(.venv)`.

## 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **First-time downloads** include `sentence-transformers` model files (~80 MB). On a slow conference Wi-Fi, ask participants to do this **before the session** or distribute the cache via USB (`~/.cache/huggingface/`).

## 4. Configure API keys

```bash
cp .env.example .env
```

Open `.env` in your editor and paste **at least one** provider key:

* OpenAI: <https://platform.openai.com/api-keys>
* Anthropic: <https://console.anthropic.com/>
* Google AI Studio: <https://aistudio.google.com/app/apikey>

Then set `LLM_PROVIDER` in `.env` to whichever provider you filled in (`openai`, `anthropic`, or `google`).

> If no key is provided, the notebooks still run — they fall back to a **mock LLM** that returns canned answers. The retrieval, embedding, graph, and data-loading parts work fully offline.

## 5. Generate the synthetic dataset

This builds the 10 PDFs + 10 Excels + 10 CSVs in `data/generated/`.

```bash
python src/data_generation.py
```

You should see:

```
[ok] PDFs written to data/generated/pdf/ (10 files)
[ok] XLSX written to data/generated/xlsx/ (10 files)
[ok] CSVs written to data/generated/csv/ (10 files)
[ok] Data dictionary written to data/generated/DATA_DICTIONARY.md
```

## 6. Launch Jupyter

```bash
jupyter lab notebooks/
```

Open **`00_environment_setup.ipynb`** first and run every cell — it sanity-checks your install and your API key.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `command not found: python3` | Install Python from python.org. On Windows, reopen the terminal after install. |
| `pip install` is very slow / fails on `chromadb` | Try `pip install chromadb --no-cache-dir`. If still failing, see fallback to FAISS in `src/rag_utils.py`. |
| `ImportError: sentence_transformers` | Re-run `pip install -r requirements.txt` inside the activated venv. |
| `AuthenticationError: Invalid API key` | Re-open `.env`, check for trailing spaces / quotes. Restart Jupyter kernel. |
| `Could not connect to ...` (corporate firewall) | Tether to a phone hotspot, or use the `local` embedding provider so only LLM calls need outbound HTTPS. |
| Notebook says "mock LLM in use" | You haven't set a key. Open `.env`, add one, restart the kernel. |
| Out-of-memory on Windows laptop | Close other apps; the embedding model takes ~500 MB RAM. |

## Pre-session checklist (instructor)

* [ ] All laptops have Python 3.10+ installed.
* [ ] `pip install -r requirements.txt` completes on the venue Wi-Fi (or pre-cached).
* [ ] `python src/data_generation.py` produces all 30 files.
* [ ] At least one provider key is loaded — `00_environment_setup.ipynb` shows ✅ for `ask_llm`.
* [ ] Notebook 13 (capstone) runs top-to-bottom on your machine.
