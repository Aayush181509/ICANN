"""Build all 14 teaching notebooks programmatically with nbformat.

Run:
    cd rag
    python notebooks/_build_notebooks.py

Each notebook follows the template:
    * Title + learning objectives
    * Concept explanation (markdown)
    * Code cell(s) with comments
    * Expected output description
    * Exercise for participants
    * Reflection questions
    * Common errors
    * Professional-use caution
"""
from __future__ import annotations

from pathlib import Path

import nbformat as nbf

OUT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Reusable header block (kept in every notebook)
# ---------------------------------------------------------------------------
TRAINING_HEADER = """\
> **ICAN CA Training — Generative AI & RAG (6 hours).** This notebook is part \
of a 14-notebook curriculum. All data is synthetic. Confidential client data \
must not be used with public APIs without engagement-letter authority. AI \
output must always be verified by a qualified professional.
"""


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text)


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text)


def save(name: str, cells: list[nbf.NotebookNode]):
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3 (rag)",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python"}
    path = OUT / name
    nbf.write(nb, path)
    print(f"  wrote {path.name}")


# Shared first code cell — adds project root to sys.path so `from src...` works
BOOTSTRAP = """\
# --- Bootstrap (don't edit) ---
# Adds the project root to sys.path so we can do `from src.xxx import yyy`.
import sys, os
from pathlib import Path
ROOT = Path.cwd()
# Walk up until we find the project root (folder that contains src/)
for _ in range(4):
    if (ROOT / 'src').exists() and (ROOT / 'requirements.txt').exists():
        break
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
print('Project root:', ROOT)
"""


# ===========================================================================
# 00 — Environment setup
# ===========================================================================
def nb_00():
    cells = [
        md(f"# 00 — Environment Setup\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n\n"
            "By the end of this notebook you can:\n"
            "1. Confirm Python and required libraries are installed.\n"
            "2. Load your API keys from `.env` and see which provider is active.\n"
            "3. Confirm the synthetic dataset has been generated.\n"
            "4. Make one successful call to the configured LLM (or see the mock fallback).\n"
        ),
        code(BOOTSTRAP),
        md("## Step 1 — Check Python version\n\nWe target Python 3.10+."),
        code(
            "import sys, platform\n"
            "print('Python:', sys.version.split()[0], 'on', platform.system())\n"
            "assert sys.version_info >= (3, 9), 'Please use Python 3.9+'"
        ),
        md("## Step 2 — Check critical libraries are installed"),
        code(
            "missing = []\n"
            "for pkg in ['pandas', 'openpyxl', 'dotenv', 'pypdf', 'numpy', 'tqdm']:\n"
            "    try:\n"
            "        __import__(pkg)\n"
            "    except Exception as e:\n"
            "        missing.append((pkg, str(e)))\n"
            "if missing:\n"
            "    print('Missing packages:', missing)\n"
            "    print('Fix: open a terminal and run  pip install -r requirements.txt')\n"
            "else:\n"
            "    print('Core packages: ok')"
        ),
        md(
            "## Step 3 — Load environment variables and report status\n\n"
            "Copy `.env.example` to `.env` and fill in *at least one* provider key. "
            "The `llm_status()` helper tells you which provider will be used."
        ),
        code(
            "from src.llm_client import llm_status, ask_llm\n"
            "status = llm_status()\n"
            "for k, v in status.items():\n"
            "    print(f'  {k:20s}: {v}')\n"
            "if status['is_mock']:\n"
            "    print('\\n[note] No real provider key detected. ask_llm() will return MOCK answers.')"
        ),
        md(
            "## Step 4 — Confirm the dataset is on disk\n\n"
            "If anything is missing, run `python src/data_generation.py` from the project root."
        ),
        code(
            "from pathlib import Path\n"
            "for d in ['data/generated/pdf', 'data/generated/xlsx', 'data/generated/csv']:\n"
            "    files = sorted(Path(d).glob('*'))\n"
            "    print(f'  {d}  →  {len(files)} files')\n"
            "    for f in files[:3]:\n"
            "        print('     -', f.name)\n"
            "    if len(files) > 3:\n"
            "        print(f'     ... and {len(files)-3} more')"
        ),
        md("## Step 5 — One smoke-test LLM call\n\nA single short call to confirm everything is wired."),
        code(
            "answer = ask_llm(\n"
            "    'In one short sentence, explain what materiality means in an audit.',\n"
            "    system='You are an experienced Nepali Chartered Accountant.'\n"
            ")\n"
            "print(answer)"
        ),
        md(
            "## Expected output\n\n"
            "* If a real key is set: a one-sentence professional definition of materiality.\n"
            "* If no key is set: a `[MOCK LLM]` message echoing your prompt.\n"
        ),
        md(
            "## Common errors\n\n"
            "| Error | Likely cause | Fix |\n"
            "|---|---|---|\n"
            "| `ModuleNotFoundError: dotenv` | Forgot `pip install -r requirements.txt` | Activate the venv and reinstall |\n"
            "| `Project root: ...` looks wrong | You opened the notebook from a strange folder | Run JupyterLab from the `rag/` folder |\n"
            "| `AuthenticationError` | Bad API key | Re-open `.env`, check for stray quotes/spaces |\n"
            "| Empty `data/generated/*` | Forgot to generate data | `python src/data_generation.py` |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "The synthetic dataset is safe to use. The moment you switch to **real client data** "
            "(later in Notebook 08), check your engagement-letter terms and prefer the local "
            "embedding model (`EMBEDDING_PROVIDER=local`)."
        ),
    ]
    save("00_environment_setup.ipynb", cells)


# ===========================================================================
# 01 — Intro to GenAI & prompting
# ===========================================================================
def nb_01():
    cells = [
        md(f"# 01 — Generative AI & Prompting for CAs\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n\n"
            "1. Distinguish AI / ML / Generative AI / LLM / GPT.\n"
            "2. Understand tokens, context window, temperature.\n"
            "3. Recognise **hallucinations** and why they happen.\n"
            "4. Apply five prompting patterns useful to a CA:\n"
            "   * role prompting\n"
            "   * few-shot prompting\n"
            "   * structured-output prompting\n"
            "   * chain-of-thought *output* (we ask the model to **show** its reasoning)\n"
            "   * grounded prompting (provide the source text in the prompt)\n"
        ),
        md(
            "## Concepts in plain language\n\n"
            "**AI** is the broad field. **Machine Learning** is the subset where the system learns from data. "
            "**Generative AI** is the kind of ML that creates new content — text, images, code. "
            "**LLMs** (Large Language Models) are the engines behind ChatGPT, Claude, Gemini. "
            "**GPT** (Generative Pre-trained Transformer) is one family of LLMs.\n\n"
            "**Token** ≈ a piece of a word. \"depreciation\" is 1–3 tokens; \"NPR 1,25,000\" is several. "
            "**Context window** = how many tokens the model can read at once.\n\n"
            "**Hallucination** = the model confidently produces something that *sounds right* but is wrong. "
            "Always verify before relying on AI output for professional work."
        ),
        code(BOOTSTRAP),
        code(
            "from src.llm_client import ask_llm\n"
            "# Helper for tidy printing\n"
            "def show(title, text):\n"
            "    print('=' * 70)\n"
            "    print(title)\n"
            "    print('-' * 70)\n"
            "    print(text)\n"
            "    print()"
        ),
        md("## Pattern 1 — Role prompting\n\nWe tell the model *who it is*. This shapes vocabulary and tone."),
        code(
            "no_role = ask_llm('Explain the difference between provisions and contingent liabilities.')\n"
            "with_role = ask_llm(\n"
            "    'Explain the difference between provisions and contingent liabilities.',\n"
            "    system='You are a senior Nepali Chartered Accountant teaching CA students. Use NFRS/NAS terminology.'\n"
            ")\n"
            "show('Without role', no_role)\n"
            "show('With role',    with_role)"
        ),
        md("## Pattern 2 — Few-shot prompting\n\nWe show the model 2-3 examples of the format we want."),
        code(
            "prompt = '''\\\n"
            "Classify each finding as HIGH / MEDIUM / LOW risk.\n\n"
            "Finding: Vendor master has 2 entries for the same vendor.\nRisk: MEDIUM\n\n"
            "Finding: A purchase of NPR 8 lakh was made without dual approval.\nRisk: HIGH\n\n"
            "Finding: Bank reconciliation done 6 days after month-end (policy says 5).\nRisk: LOW\n\n"
            "Finding: Related-party purchase booked without benchmark pricing.\nRisk:\n"
            "'''\n"
            "show('Few-shot', ask_llm(prompt))"
        ),
        md("## Pattern 3 — Structured output prompting\n\nAsk for JSON so we can use the result downstream."),
        code(
            "from src.llm_client import ask_llm_json\n"
            "memo = '''\\\n"
            "During the audit we noted three findings: (1) two purchase invoices exceeding NPR 5,00,000 \n"
            "lacked dual approval, (2) the vendor master contains duplicate entries for Kathmandu Steel \n"
            "Suppliers, and (3) related-party purchases from Himal Family Enterprises lack benchmark pricing.\n"
            "'''\n"
            "result = ask_llm_json(\n"
            "    f'Extract findings from the memo as a JSON list of {{\"finding\":..., \"area\":..., \"risk\":...}}. \\n\\nMemo:\\n{memo}'\n"
            ")\n"
            "print(result)"
        ),
        md("## Pattern 4 — Chain-of-thought *output*\n\nWe ask the model to **show** its reasoning steps in the answer. This often improves accuracy."),
        code(
            "q = (\n"
            "    'A company has revenue NPR 48.6 crore and net profit NPR 4.2 crore. '\n"
            "    'Loan outstanding is NPR 18.2 crore at 10.5%. '\n"
            "    'Roughly estimate the interest coverage ratio. Show working step by step.'\n"
            ")\n"
            "show('Reasoning output', ask_llm(q))"
        ),
        md("## Pattern 5 — Grounded prompting\n\nGive the model the source. This is the foundation of RAG."),
        code(
            "policy = '''\\\n"
            "Procurement Policy, clause 1: For purchases above NPR 1,00,000 a minimum of three competitive quotations \n"
            "must be obtained. For purchases above NPR 10,00,000 a sealed-bid tender process is required. Sole-source \n"
            "procurement is permitted only with the CFO's prior written approval and documented justification.\n"
            "'''\n"
            "q = 'Per the policy below, can the company sole-source a NPR 12 lakh purchase? Quote the relevant clause.\\n\\n' + policy\n"
            "show('Grounded answer', ask_llm(q))"
        ),
        md(
            "## Hallucination demo (important!)\n\n"
            "We deliberately ask about a fictional ICAN circular. Watch what the model invents."
        ),
        code(
            "show('Possibly hallucinated', ask_llm('What does ICAN Technical Circular 99/2099-50 say about cryptoasset audit?'))"
        ),
        md(
            "**Lesson.** The model may *describe a plausible-looking circular that does not exist*. "
            "Never rely on an LLM for citations of laws, standards, or circulars without an independent check.\n"
        ),
        md(
            "## Practical CA prompts (try these live)\n\n"
            "1. *Summarise this audit memo in 5 bullet points.*\n"
            "2. *Extract risks and rate them HIGH/MEDIUM/LOW.*\n"
            "3. *Draft a polite email asking a vendor to provide PAN documentation.*\n"
            "4. *Explain a tax provision to a non-finance director.*\n"
            "5. *Convert these messy notes into an audit checklist.*\n"
        ),
        code(
            "# Exercise — change the inputs below and observe the answers\n"
            "your_memo = 'During inventory observation at Bhaktapur, slow-moving SKU FG-509 (NPR 2.16 lakh, 700+ days old) was noted.'\n"
            "show('Summary', ask_llm(f'Summarise in 3 bullets: {your_memo}'))"
        ),
        md(
            "## Reflection questions\n\n"
            "* In which of your firm's workflows would few-shot prompting save the most time?\n"
            "* What is the worst that could happen if a hallucinated tax citation reached a client?\n"
            "* When is *structured-output* prompting better than free text for your work?\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| Model ignores your role | Move the role to the `system` argument, not the prompt body |\n"
            "| JSON cell prints `_parse_error` | Re-run; if it persists, add `Respond with only JSON, no commentary.` |\n"
            "| Mock answers everywhere | Set a key in `.env` and restart the kernel |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "* LLMs sound confident even when wrong — *especially* on standards, laws, and citations.\n"
            "* Treat LLM output as a **draft from an articled assistant**, never as final professional work.\n"
        ),
    ]
    save("01_intro_to_gen_ai_and_prompting.ipynb", cells)


# ===========================================================================
# 02 — First LLM call: simple Q&A
# ===========================================================================
def nb_02():
    cells = [
        md(f"# 02 — Your First LLM Call from Python\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Use the `ask_llm()` wrapper to call any configured provider.\n"
            "2. Send a CA/finance question and read the structured answer.\n"
            "3. Ask the model for **JSON** so the result can be used in pandas.\n"
            "4. Build a **prompt template** for repeated tasks.\n"
        ),
        code(BOOTSTRAP),
        code("from src.llm_client import ask_llm, ask_llm_json"),
        md("## 2.1 — A plain finance question"),
        code("print(ask_llm('What is deferred tax, in one paragraph?'))"),
        md("## 2.2 — Ask three CA-style questions in a loop"),
        code(
            "questions = [\n"
            "    'Give 3 audit risks specific to a manufacturing company in Nepal.',\n"
            "    'List the typical documentation expected to support a related-party transaction.',\n"
            "    'Explain (briefly) the difference between TDS and Advance Tax in Nepal.'\n"
            "]\n"
            "for q in questions:\n"
            "    print('Q:', q)\n"
            "    print('A:', ask_llm(q))\n"
            "    print('-' * 60)"
        ),
        md("## 2.3 — Structured JSON output for downstream automation"),
        code(
            "import pandas as pd\n"
            "memo = '''\\\n"
            "1. Bank reconciliation has stale cheques older than 6 months.\n"
            "2. Two vendors lack PAN/VAT registration in the master.\n"
            "3. Inventory item FG-509 is 700+ days old and not provided for.\n"
            "4. Related-party purchases without benchmark pricing.\n"
            "'''\n"
            "obj = ask_llm_json(\n"
            "    'Extract a JSON array of findings from the memo. Each item has \"finding\", '\n"
            "    '\"category\" (one of Finance, Procurement, Inventory, Compliance), and '\n"
            "    '\"recommended_action\".\\n\\nMemo:\\n' + memo\n"
            ")\n"
            "print(obj)\n"
            "if isinstance(obj, list):\n"
            "    df = pd.DataFrame(obj)\n"
            "    display(df)"
        ),
        md("## 2.4 — Build a prompt template (DRY)\n\nWe wrap a repeated prompt in a function for cleanliness."),
        code(
            "def summarise_to_bullets(text, n=5):\n"
            "    prompt = f'Summarise the text below in exactly {n} short bullet points for a CA audience.\\n\\n{text}'\n"
            "    return ask_llm(prompt, system='You are a Nepali CA assistant. Be concise.')\n"
            "\n"
            "memo = ('During our planning meeting we identified five risks. Revenue cut-off is the most '\n"
            "        'significant given the Q4 spike. Inventory existence is high risk due to the new '\n"
            "        'production line. Related-party transactions need careful inspection. Loan DSCR has '\n"
            "        'tight headroom. Going concern needs revisiting.')\n"
            "print(summarise_to_bullets(memo, n=5))"
        ),
        md(
            "## Expected output\n\n"
            "* Section 2.3 should give a JSON array → DataFrame with the four findings.\n"
            "* Section 2.4 should give exactly five bullets.\n"
        ),
        md(
            "## Exercise\n\n"
            "Pick one of your routine emails (vendor follow-up, audit-confirmation letter) and turn it into a "
            "reusable `ask_llm` template. Run it on three different inputs.\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| `obj['_parse_error']` shows up | The model added commentary. Re-run; if persistent, tighten the prompt: *only JSON, no markdown fences*. |\n"
            "| 429 / rate limit | Wait a few seconds. For class delivery, lower `temperature` and `k`. |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "Do not paste real client emails, balance sheets, or PII into a public LLM provider "
            "without engagement-letter authority. Synthetic data only at this stage."
        ),
    ]
    save("02_first_llm_call_simple_qa.ipynb", cells)


# ===========================================================================
# 03 — Loading financial data: PDF / Excel / CSV
# ===========================================================================
def nb_03():
    cells = [
        md(f"# 03 — Loading PDFs, Excel, and CSV Files\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Read narrative PDFs (audit memos, policies) with `pypdf` / `pymupdf`.\n"
            "2. Read multi-sheet Excel workbooks with `pandas.read_excel`.\n"
            "3. Read transactional CSVs with `pandas.read_csv`.\n"
            "4. Preview and clean common issues: duplicates, missing PAN, type coercion.\n"
        ),
        code(BOOTSTRAP),
        md("## 3.1 — Read a PDF page-by-page"),
        code(
            "from src.document_loaders import load_pdf\n"
            "pages = load_pdf('data/generated/pdf/02_audit_planning_memo.pdf')\n"
            "print(f'{len(pages)} page(s)')\n"
            "print('--- First 500 chars of page 1 ---')\n"
            "print(pages[0]['text'][:500])\n"
            "print('--- metadata ---')\n"
            "print(pages[0]['metadata'])"
        ),
        md("## 3.2 — Read a multi-sheet Excel"),
        code(
            "from src.document_loaders import load_excel\n"
            "wb = load_excel('data/generated/xlsx/02_general_ledger_sample.xlsx')\n"
            "print('Sheets:', list(wb))\n"
            "for name, df in wb.items():\n"
            "    print(f'\\n=== {name} ({len(df)} rows) ===')\n"
            "    display(df.head(3))"
        ),
        md("## 3.3 — Read a CSV and quick preview"),
        code(
            "import pandas as pd\n"
            "purchases = pd.read_csv('data/generated/csv/02_purchase_transactions.csv')\n"
            "print('Shape:', purchases.shape)\n"
            "print('Columns:', list(purchases.columns))\n"
            "display(purchases.head())\n"
            "print('\\nApproval status counts:')\n"
            "print(purchases['approval_status'].value_counts())"
        ),
        md("## 3.4 — Find the duplicate invoice numbers (teaching trigger)\n\nThis is a *real* problem your participants will recognise."),
        code(
            "dupes = purchases[purchases['invoice_no'].duplicated(keep=False)].sort_values('invoice_no')\n"
            "print(f'Duplicate-invoice rows: {len(dupes)}')\n"
            "display(dupes[['invoice_no','date','vendor_name','amount','approval_status']])"
        ),
        md("**Discussion.** Two of the duplicate invoices are under different *vendor names* that look like the same supplier. This is exactly the kind of finding the audit team should flag in the management letter."),
        md("## 3.5 — Find missing PAN/VAT entries"),
        code(
            "vendors = pd.read_csv('data/generated/csv/04_vendor_master.csv')\n"
            "missing_pan = vendors[vendors['pan'].isna() | (vendors['pan'] == '')]\n"
            "display(missing_pan)"
        ),
        md("## 3.6 — Quick cleaning patterns"),
        code(
            "# Normalise vendor names — strip, title-case, collapse spaces\n"
            "import re\n"
            "def normalise(name):\n"
            "    return re.sub(r'\\s+', ' ', str(name).strip().title())\n"
            "vendors['vendor_name_norm'] = vendors['vendor_name'].apply(normalise)\n"
            "display(vendors[['vendor_code','vendor_name','vendor_name_norm','pan']])"
        ),
        md("## 3.7 — Cast date columns properly"),
        code(
            "purchases['date'] = pd.to_datetime(purchases['date'], errors='coerce')\n"
            "print('Date range:', purchases['date'].min(), '→', purchases['date'].max())"
        ),
        md(
            "## Expected output\n\n"
            "* Section 3.1 — text of the audit planning memo (page 1).\n"
            "* Section 3.4 — at least 4 rows with duplicate `invoice_no`.\n"
            "* Section 3.5 — at least one vendor with empty PAN.\n"
        ),
        md(
            "## Exercise\n\n"
            "1. Open `data/generated/xlsx/04_accounts_receivable_aging.xlsx` and identify the customer "
            "with **all** balances overdue.\n"
            "2. In the journal-entries CSV, find any JE posted by the same employee who approved it "
            "(maker = checker violation)."
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| `FileNotFoundError` | Run `python src/data_generation.py` from the project root |\n"
            "| `ImportError: openpyxl` | `pip install openpyxl` |\n"
            "| Garbled PDF text | The PDF is scanned — needs OCR (Notebook 09 covers this limitation) |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "`pandas` is showing you only the rows you ask for. **Always verify the row count "
            "(`df.shape`) matches the original source** so you know nothing was silently dropped."
        ),
    ]
    save("03_loading_financial_data_pdf_excel_csv.ipynb", cells)


# ===========================================================================
# 04 — Embeddings and vector search
# ===========================================================================
def nb_04():
    cells = [
        md(f"# 04 — Embeddings & Vector Search\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Explain embeddings in plain language.\n"
            "2. Compare **keyword search** with **semantic search**.\n"
            "3. Chunk a document (size + overlap) and understand why.\n"
            "4. Build a simple vector store over our PDFs.\n"
        ),
        md(
            "## What is an embedding?\n\n"
            "**Analogy.** An embedding turns a sentence into a *GPS coordinate of meaning*. "
            "Two sentences about the same topic land near each other, even if they use different words. "
            "We can then \"search by meaning\" instead of search by exact words.\n\n"
            "Concretely: an embedding is a fixed-length vector of numbers (e.g. 384 numbers per chunk). "
            "We measure similarity with **cosine similarity** (dot-product after normalisation)."
        ),
        code(BOOTSTRAP),
        md("## 4.1 — Keyword vs semantic search side by side"),
        code(
            "import pandas as pd\n"
            "from src.document_loaders import load_pdfs_in_folder\n"
            "from src.rag_utils import VectorStore, chunk_documents\n"
            "\n"
            "docs = load_pdfs_in_folder('data/generated/pdf')\n"
            "print(f'Loaded {len(docs)} page-documents from PDFs')"
        ),
        code(
            "# Build the vector store (first run downloads the embedding model ~80 MB)\n"
            "chunks = chunk_documents(docs, chunk_size=800, overlap=120)\n"
            "print(f'Created {len(chunks)} chunks')\n"
            "store = VectorStore()\n"
            "store.add(chunks)\n"
            "print(f'Vector store size: {len(store)} chunks')"
        ),
        code(
            "query = 'vendor approval thresholds'\n"
            "\n"
            "# --- Keyword search (naive substring) ---\n"
            "keyword_hits = [c for c in chunks if query.lower() in c['text'].lower()][:3]\n"
            "print(f'\\nKEYWORD SEARCH found {len(keyword_hits)} chunks')\n"
            "for h in keyword_hits:\n"
            "    print('  -', h['metadata'].get('source'), 'p.', h['metadata'].get('page'))\n"
            "\n"
            "# --- Semantic search ---\n"
            "semantic_hits = store.search(query, k=3)\n"
            "print(f'\\nSEMANTIC SEARCH top 3')\n"
            "for h in semantic_hits:\n"
            "    print(f\"  - {h['metadata'].get('source'):40s} p.{h['metadata'].get('page')}  score={h['score']:.3f}\")"
        ),
        md(
            "**Why is semantic search different?** The exact phrase \"vendor approval thresholds\" "
            "may not appear anywhere — but the *Approval Matrix* in the Internal Control Policy and the "
            "*Vendor Selection* clause in the Procurement Policy are *semantically* close. Keyword search misses them; semantic search finds them."
        ),
        md("## 4.2 — Inspect a chunk"),
        code(
            "top = store.search('loan covenant compliance', k=1)[0]\n"
            "print('Source:', top['metadata'])\n"
            "print('Score :', round(top['score'], 3))\n"
            "print('Text  :')\n"
            "print(top['text'])"
        ),
        md("## 4.3 — Chunking — why size and overlap matter"),
        code(
            "from src.rag_utils import chunk_text\n"
            "long = docs[0]['text']\n"
            "print('Document length (chars):', len(long))\n"
            "for size in [200, 800, 1500]:\n"
            "    cks = chunk_text(long, chunk_size=size, overlap=80)\n"
            "    print(f'  chunk_size={size:5d}  →  {len(cks):3d} chunks  '\n"
            "          f\"avg {sum(len(c) for c in cks)//len(cks)} chars\")"
        ),
        md(
            "**Trade-off.** Small chunks = precise retrieval but lose context. Large chunks = more context "
            "but the LLM has to wade through irrelevant text. 600–1000 chars with 100–150 overlap is a "
            "sensible default for short business documents. Overlap prevents a fact from being split at the boundary."
        ),
        md("## 4.4 — Filter by metadata"),
        code(
            "# Search only inside the Procurement Policy\n"
            "hits = store.search('sole-source approval', k=3, where={'source': '04_procurement_policy.pdf'})\n"
            "for h in hits:\n"
            "    print(h['metadata'], 'score=', round(h['score'], 3))\n"
            "    print(h['text'][:200], '...\\n')"
        ),
        md(
            "## Expected output\n\n"
            "* Keyword search → 0 hits for \"vendor approval thresholds\" (exact phrase isn't in the docs).\n"
            "* Semantic search → top hits are the Internal Control Policy and Procurement Policy.\n"
        ),
        md(
            "## Exercise\n\n"
            "1. Try queries: `\"related party benchmark\"`, `\"DSCR ratio\"`, `\"physical count exceptions\"`. "
            "Inspect the top chunks. Are they the *right* ones?\n"
            "2. Increase `chunk_size` to 2000 and re-build. Does retrieval get better or worse?\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| First run very slow | The embedding model (~80 MB) is downloading. Subsequent runs are fast. |\n"
            "| Out-of-memory | Reduce chunks (larger `chunk_size`) or limit to a subset of PDFs. |\n"
            "| Wrong chunk retrieved | Re-tune chunk size / overlap; consider a hybrid keyword+semantic search (out of scope today). |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "Semantic search gives you the **most similar** chunk — that is not the same as the "
            "**most authoritative** chunk. Citations matter (covered in Notebook 06)."
        ),
    ]
    save("04_embeddings_and_vector_search.ipynb", cells)


# ===========================================================================
# 05 — Basic RAG for CA use cases
# ===========================================================================
def nb_05():
    cells = [
        md(f"# 05 — Basic RAG for CA Use Cases\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Understand the RAG pipeline: load → chunk → embed → retrieve → prompt → answer.\n"
            "2. Build a basic RAG system over the synthetic CA documents.\n"
            "3. Ask CA-specific questions and read grounded answers.\n"
        ),
        md(
            "## The RAG idea in one paragraph\n\n"
            "Pure LLMs answer from memory — sometimes brilliantly, sometimes by hallucinating. "
            "**RAG (Retrieval-Augmented Generation)** changes that: before answering, we *retrieve* the most "
            "relevant chunks from our own documents, paste them into the prompt, and ask the model to answer "
            "**only from those chunks**. Result: grounded answers with sources."
        ),
        code(BOOTSTRAP),
        md("## 5.1 — Build the store (one-time, ~15s)"),
        code(
            "from src.rag_utils import build_store_from_folder, rag_answer\n"
            "store = build_store_from_folder('data/generated/pdf', chunk_size=800, overlap=120)\n"
            "print(f'Store has {len(store)} chunks.')"
        ),
        md("## 5.2 — Ask a CA-typical question"),
        code(
            "question = 'What are the key audit risks identified in the planning memo?'\n"
            "answer, hits = rag_answer(question, store, k=4, return_hits=True)\n"
            "print('QUESTION:', question)\n"
            "print('\\n--- ANSWER ---')\n"
            "print(answer)\n"
            "print('\\n--- RETRIEVED CHUNKS ---')\n"
            "for h in hits:\n"
            "    print(f\"  {h['metadata'].get('source')} p.{h['metadata'].get('page')}  score={h['score']:.3f}\")"
        ),
        md("## 5.3 — A batch of CA questions"),
        code(
            "ca_questions = [\n"
            "    'Which transactions look unusual based on the audit memos?',\n"
            "    'What does the procurement policy say about approvals for purchases above NPR 5 lakh?',\n"
            "    'Are there any possible compliance issues with related parties?',\n"
            "    'Summarise the related party transactions disclosed in the annual report.',\n"
            "    'What is the loan covenant for DSCR and is it being met?',\n"
            "]\n"
            "for q in ca_questions:\n"
            "    print('Q:', q)\n"
            "    print('A:', rag_answer(q, store, k=4))\n"
            "    print('-' * 80)"
        ),
        md(
            "## What just happened?\n\n"
            "For each question, the system:\n"
            "1. Embedded the question.\n"
            "2. Found the top-4 most similar chunks from your PDFs.\n"
            "3. Built a prompt: \"Answer this question using only the context below: [chunks]\".\n"
            "4. Sent it to the LLM and returned the answer with citations.\n"
        ),
        md(
            "## Expected output\n\n"
            "Answers should quote the planning memo's five risks, the policy's three-tier approval matrix, "
            "and the loan agreement's 1.25x DSCR covenant. Each fact should be tagged with the source filename "
            "and page number."
        ),
        md(
            "## Exercise\n\n"
            "1. Ask: *\"What are the policy rules for related-party purchases?\"* — does the answer combine "
            "the Procurement Policy and the NFRS policy note?\n"
            "2. Reduce `k` to 1 and re-ask the audit-risk question. What is missing?\n"
            "3. Increase `k` to 8. Does the answer get better or noisier?\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| Answer says \"I could not find this\" | The information isn't in the docs *or* retrieval missed. Try rephrasing the question or raising `k`. |\n"
            "| Answer cites a wrong page | Inspect the retrieved chunks — the model may be paraphrasing across two chunks. |\n"
            "| Answer invents facts | Bad sign — try a stricter system prompt (\"Use ONLY the context. Quote verbatim where possible.\") |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "RAG is **not** \"AI that is always right\". It is \"AI that is *less likely* to hallucinate, "
            "because we forced it to look at our text first\". Always check the cited chunk yourself before "
            "relying on the answer for client work."
        ),
    ]
    save("05_basic_rag_for_ca_usecases.ipynb", cells)


# ===========================================================================
# 06 — RAG with sources and citations
# ===========================================================================
def nb_06():
    cells = [
        md(f"# 06 — RAG with Sources & Citations\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Understand why **citations matter for a CA** (audit trail, working papers).\n"
            "2. Display the retrieved chunk, source filename, and page in the answer.\n"
            "3. Teach the system to say *\"I could not find this\"* instead of hallucinating.\n"
        ),
        code(BOOTSTRAP),
        code(
            "from src.rag_utils import build_store_from_folder, rag_answer\n"
            "store = build_store_from_folder('data/generated/pdf')\n"
            "print('Store size:', len(store))"
        ),
        md("## 6.1 — Answer with citations and supporting evidence"),
        code(
            "def answer_with_evidence(question, k=4):\n"
            "    answer, hits = rag_answer(question, store, k=k, return_hits=True)\n"
            "    print('Q:', question)\n"
            "    print('\\nANSWER (with inline citations):')\n"
            "    print(answer)\n"
            "    print('\\nSOURCE CHUNKS (the evidence the model saw):')\n"
            "    for i, h in enumerate(hits, 1):\n"
            "        m = h['metadata']\n"
            "        print(f\"\\n[{i}] {m.get('source')}  page {m.get('page','-')}  (score {h['score']:.3f})\")\n"
            "        snippet = h['text'][:300].replace('\\n', ' ')\n"
            "        print('   ', snippet, '...')\n"
            "    return answer, hits\n"
            "\n"
            "_ = answer_with_evidence('What are the financial covenants on the term loan?')"
        ),
        md("## 6.2 — \"I don't know\" behaviour\n\nA question that the corpus **cannot** answer."),
        code(
            "_ = answer_with_evidence('What was the depreciation rate used in FY 1998/99?')"
        ),
        md(
            "**Lesson.** The system prompt instructs the model to reply with exactly "
            "*\"I could not find this in the provided documents.\"* when retrieval is weak or the answer is missing. "
            "This is *much* safer than guessing for a CA workflow."
        ),
        md("## 6.3 — Build a working-paper-style record"),
        code(
            "from datetime import datetime\n"
            "import pandas as pd\n"
            "\n"
            "def as_workpaper(question, k=4):\n"
            "    answer, hits = rag_answer(question, store, k=k, return_hits=True)\n"
            "    rows = [{\n"
            "        'source': h['metadata'].get('source'),\n"
            "        'page': h['metadata'].get('page'),\n"
            "        'similarity': round(h['score'], 3),\n"
            "        'snippet': h['text'][:200].replace('\\n', ' ') + '...',\n"
            "    } for h in hits]\n"
            "    df = pd.DataFrame(rows)\n"
            "    print(f'Question      : {question}')\n"
            "    print(f'Asked at      : {datetime.now().isoformat(timespec=\"seconds\")}')\n"
            "    print('Answer:')\n"
            "    print(answer)\n"
            "    print('\\nRetrieved evidence:')\n"
            "    display(df)\n"
            "    return df\n"
            "\n"
            "_ = as_workpaper('What approval threshold applies to a NPR 6 lakh purchase?')"
        ),
        md(
            "## Expected output\n\n"
            "* Answers contain `[source: filename, p.N]` tags.\n"
            "* The depreciation-FY1998 question returns the *I-could-not-find* sentence.\n"
            "* Section 6.3 produces a clean evidence table you could paste into a working paper.\n"
        ),
        md(
            "## Exercise\n\n"
            "1. Compose 5 questions, of which 2 are *deliberately unanswerable*. Run them through "
            "`answer_with_evidence`. Did the system correctly refuse on the 2 unanswerable ones?\n"
            "2. Modify `DEFAULT_SYSTEM` in `src/rag_utils.py` to ask the model to also list the "
            "**filename(s) it consulted** at the bottom of every answer.\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| Answer contains a citation that doesn't appear in the retrieved chunks | The model invented it. Lower temperature, tighten the system prompt, verify manually. |\n"
            "| \"I could not find this\" for a question the docs *do* answer | Retrieval missed — try rephrasing or raise `k`. |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "A citation that *looks* like a workpaper reference is still **not** a workpaper reference until "
            "a human has verified the source contains the cited fact. Always inspect the evidence chunks."
        ),
    ]
    save("06_rag_with_sources_and_citations.ipynb", cells)


# ===========================================================================
# 07 — Multi-document RAG
# ===========================================================================
def nb_07():
    cells = [
        md(f"# 07 — Multi-Document RAG\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Combine narrative documents (PDFs) with structured documents (Excel/CSV) in a single store.\n"
            "2. Tag each chunk with `doc_type` metadata.\n"
            "3. Use **metadata filters** to search within a category (\"only policies\").\n"
            "4. Compare facts across documents (cross-document Q&A).\n"
        ),
        code(BOOTSTRAP),
        md("## 7.1 — Load PDFs + spreadsheets into one store"),
        code(
            "from pathlib import Path\n"
            "from src.document_loaders import load_pdfs_in_folder, excel_to_text_documents, csv_to_text_documents\n"
            "from src.rag_utils import VectorStore, chunk_documents\n"
            "\n"
            "docs = []\n"
            "docs.extend(load_pdfs_in_folder('data/generated/pdf'))\n"
            "for p in sorted(Path('data/generated/xlsx').glob('*.xlsx')):\n"
            "    docs.extend(excel_to_text_documents(p))\n"
            "for p in sorted(Path('data/generated/csv').glob('*.csv')):\n"
            "    docs.extend(csv_to_text_documents(p))\n"
            "print(f'Loaded {len(docs)} documents (PDF pages + sheets + CSV summaries)')\n"
            "\n"
            "chunks = chunk_documents(docs, chunk_size=800, overlap=120)\n"
            "store = VectorStore()\n"
            "store.add(chunks)\n"
            "print(f'Store has {len(store)} chunks.')"
        ),
        md("## 7.2 — Inspect the doc_type distribution"),
        code(
            "from collections import Counter\n"
            "print(Counter(c['metadata'].get('doc_type','?') for c in chunks))"
        ),
        md("## 7.3 — Filtered retrieval — only policies"),
        code(
            "from src.rag_utils import rag_answer\n"
            "answer = rag_answer(\n"
            "    'What is the approval threshold for related-party purchases?',\n"
            "    store, k=4, where={'doc_type': 'policy'},\n"
            ")\n"
            "print(answer)"
        ),
        md("## 7.4 — Cross-document question\n\nA question that requires combining the loan agreement *and* the annual report."),
        code(
            "answer, hits = rag_answer(\n"
            "    'Compare the loan terms in the loan agreement summary with what the annual report discloses about borrowings.',\n"
            "    store, k=6, return_hits=True,\n"
            ")\n"
            "print(answer)\n"
            "print('\\nSources consulted:')\n"
            "for h in hits:\n"
            "    print('  -', h['metadata'].get('source'), 'p.', h['metadata'].get('page'))"
        ),
        md("## 7.5 — Find inconsistencies\n\n*\"Is the related-party listing consistent with what the board minutes approved?\"*"),
        code(
            "print(rag_answer(\n"
            "    'Are all related-party transactions in the RPT listing supported by board approval recorded in the minutes? Flag any without approval.',\n"
            "    store, k=6,\n"
            "))"
        ),
        md("## 7.6 — Ledger-supported audit risks"),
        code(
            "print(rag_answer(\n"
            "    'Which audit risks mentioned in the planning memo are supported by patterns visible in the ledger data?',\n"
            "    store, k=6,\n"
            "))"
        ),
        md(
            "## Expected output\n\n"
            "* 7.3 — answer cites the Procurement Policy and Internal Control Policy.\n"
            "* 7.4 — answer cites both `06_loan_agreement_summary.pdf` *and* `01_annual_report_extract.pdf`.\n"
            "* 7.5 — should flag the row dated 2082-02-20 (Himal Family Enterprises) as not Board-approved.\n"
        ),
        md(
            "## Exercise\n\n"
            "1. Build a `doc_type` filter that searches only `spreadsheet` docs and ask: \"What is the year-end inventory balance?\"\n"
            "2. Use `where={'source': '07_board_minutes.pdf'}` and ask about Q3 financial performance.\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| Filter returns 0 hits | Check the exact metadata value with `Counter` first (case matters). |\n"
            "| Cross-doc answer misses one side | Increase `k` so both documents are likely to be retrieved. |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "When the system combines facts from two documents, *each* fact still needs verification "
            "against its source. A consistent-sounding combination can still contain a hallucinated link "
            "between unrelated facts."
        ),
    ]
    save("07_multi_document_rag.ipynb", cells)


# ===========================================================================
# 08 — RAG on participants' own data
# ===========================================================================
def nb_08():
    cells = [
        md(f"# 08 — RAG on Your Own Data\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Drop your own PDF / Excel / CSV / text files into `data/user_data/`.\n"
            "2. Auto-detect, chunk, embed, and build a private vector store.\n"
            "3. Ask questions and inspect citations against *your* documents.\n"
            "4. Apply confidentiality safeguards.\n"
        ),
        md(
            "## ⚠️ Before you add files — read this\n\n"
            "1. **Anonymise.** Remove or mask client names, PANs, employee IDs.\n"
            "2. **Engagement-letter authority.** Confirm AI use is permitted.\n"
            "3. **Set `EMBEDDING_PROVIDER=local` in `.env`** so embeddings stay on your laptop.\n"
            "4. **Switch `LLM_PROVIDER=mock`** if you want to test retrieval *without* sending chunks to a public LLM.\n"
            "5. Files in `data/user_data/` are ignored by git by default. Keep it that way.\n"
        ),
        code(BOOTSTRAP),
        md("## 8.1 — Detect what's available"),
        code(
            "from pathlib import Path\n"
            "user_dir = Path('data/user_data')\n"
            "files = [p for p in user_dir.rglob('*') if p.is_file() and p.suffix.lower() in ('.pdf','.xlsx','.xls','.csv','.txt','.md')]\n"
            "print(f'Found {len(files)} supported file(s):')\n"
            "for f in files:\n"
            "    print('  -', f.relative_to(user_dir))\n"
            "if not files:\n"
            "    print('\\nNo files yet. Falling back to the synthetic dataset so the lesson still runs.')"
        ),
        md("## 8.2 — Build the store (auto-fallback to synthetic data)"),
        code(
            "from src.rag_utils import build_store_from_folder\n"
            "from pathlib import Path\n"
            "\n"
            "source_folder = 'data/user_data' if any(Path('data/user_data').rglob('*.*')) else 'data/generated/pdf'\n"
            "print('Using folder:', source_folder)\n"
            "store = build_store_from_folder(source_folder, chunk_size=800, overlap=120)\n"
            "print(f'Store size: {len(store)} chunks')"
        ),
        md("## 8.3 — Configure your questions"),
        code(
            "# Edit this list with questions about your own data\n"
            "your_questions = [\n"
            "    'Summarise the most important findings.',\n"
            "    'What are the key risks?',\n"
            "    'Are there any policy violations?',\n"
            "    'Are PAN/VAT numbers consistently captured?',\n"
            "]\n"
            "from src.rag_utils import rag_answer\n"
            "for q in your_questions:\n"
            "    answer, hits = rag_answer(q, store, k=4, return_hits=True)\n"
            "    print('Q:', q)\n"
            "    print('A:', answer)\n"
            "    print('Sources:', [(h['metadata'].get('source'), h['metadata'].get('page')) for h in hits])\n"
            "    print('-' * 80)"
        ),
        md("## 8.4 — Save the store to disk (optional, persistent)"),
        code(
            "# Persist a Chroma-backed store so we don't re-embed every notebook reload.\n"
            "from src.rag_utils import build_store_from_folder\n"
            "try:\n"
            "    persistent = build_store_from_folder(source_folder, persist_dir='outputs/vector_store/user_data')\n"
            "    print('Persisted store size:', len(persistent))\n"
            "except Exception as e:\n"
            "    print('Skipping Chroma persistence:', e)"
        ),
        md(
            "## Expected output\n\n"
            "* The detect cell lists every supported file in `data/user_data/`.\n"
            "* If you added nothing, the notebook silently falls back to the synthetic PDFs.\n"
        ),
        md(
            "## Exercise\n\n"
            "1. Drop one *anonymised* policy document and ask 3 policy-compliance questions.\n"
            "2. Drop a trial-balance Excel and ask: *\"Which expense lines show unusual growth versus last year?\"*\n"
            "3. With a `doc_type` filter, restrict retrieval to only the policy file.\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| `[warn] Skipping ...: ParserError` | The file is corrupt or password-protected. |\n"
            "| Slow embedding | Large files — increase `chunk_size`, or limit files in `data/user_data/`. |\n"
            "| OCR-needed PDF returns nothing | The PDF is a scan; OCR is required (covered in Notebook 09). |\n"
        ),
        md(
            "## ⚠️ Professional caution (repeat)\n\n"
            "*Anything you put in `data/user_data/` and ask a public LLM about will be sent to that LLM.* "
            "Use the **mock** or **local** providers if confidentiality matters and you have no engagement "
            "authority. Delete the files after the session if they were a one-off."
        ),
    ]
    save("08_rag_on_participants_own_data.ipynb", cells)


# ===========================================================================
# 09 — RAG limitations & evaluation
# ===========================================================================
def nb_09():
    cells = [
        md(f"# 09 — RAG Limitations & Simple Evaluation\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Recognise the 8 most common RAG failure modes.\n"
            "2. Reproduce 2-3 of them with our own data.\n"
            "3. Build a tiny evaluation harness with expected keywords + expected sources.\n"
            "4. Apply a *Safe-Use Checklist* before relying on RAG for client work.\n"
        ),
        md(
            "## The 8 failure modes\n\n"
            "1. **Hallucination** — model invents facts/citations.\n"
            "2. **Incomplete source corpus** — the answer is *not* in our docs.\n"
            "3. **Poor chunking** — a key fact is split across two chunks.\n"
            "4. **OCR / scanned PDFs** — extraction returns empty text.\n"
            "5. **Tables** — `pypdf` flattens tables into garbled rows.\n"
            "6. **Wrong retrieval** — semantically close but factually wrong chunk wins.\n"
            "7. **Missing metadata** — can't filter or attribute correctly.\n"
            "8. **Outdated regulation** — model's training is frozen; laws change.\n"
            "9. **Confidentiality** — sending client data to a public API.\n"
            "10. **Overreliance** — trusting AI output without verification.\n"
        ),
        code(BOOTSTRAP),
        code(
            "from src.rag_utils import build_store_from_folder, rag_answer\n"
            "store = build_store_from_folder('data/generated/pdf')\n"
            "print('Store size:', len(store))"
        ),
        md("## 9.1 — Reproduce: hallucination from an out-of-corpus question"),
        code(
            "print(rag_answer('What is the current corporate tax rate in Bhutan?', store, k=3))\n"
            "# Expected: the model should answer \"I could not find this in the provided documents.\""
        ),
        md("## 9.2 — Reproduce: wrong retrieval"),
        code(
            "# 'approval matrix' is a phrase in the Internal Control Policy.\n"
            "# But the term may also be (weakly) similar to chunks in the procurement and management letter.\n"
            "answer, hits = rag_answer('What is the approval matrix?', store, k=1, return_hits=True)\n"
            "print(answer)\n"
            "for h in hits:\n"
            "    print('  retrieved:', h['metadata'].get('source'), 'p.', h['metadata'].get('page'))"
        ),
        md(
            "Try the same with `k=1` versus `k=4`. With `k=1` retrieval misses are *fatal*; with `k=4` "
            "the right chunk usually survives. This is the classic recall-vs-precision trade-off."
        ),
        md("## 9.3 — Reproduce: poor chunking"),
        code(
            "from src.rag_utils import VectorStore, chunk_documents\n"
            "from src.document_loaders import load_pdfs_in_folder\n"
            "\n"
            "docs = load_pdfs_in_folder('data/generated/pdf')\n"
            "# Deliberately tiny chunks → important threshold numbers may be cut in half\n"
            "tiny_chunks = chunk_documents(docs, chunk_size=120, overlap=0)\n"
            "bad_store = VectorStore(); bad_store.add(tiny_chunks)\n"
            "print('Tiny-chunk answer:')\n"
            "print(rag_answer('What is the DSCR covenant on the term loan?', bad_store, k=3))"
        ),
        md("## 9.4 — A small evaluation set"),
        code(
            "from src.evaluation_utils import EvalCase, evaluate\n"
            "import pandas as pd\n"
            "\n"
            "cases = [\n"
            "    EvalCase(\n"
            "        question='What are the five significant audit risks?',\n"
            "        expected_keywords=['revenue', 'inventory', 'related party', 'covenant', 'going concern'],\n"
            "        expected_source_contains='audit_planning',\n"
            "    ),\n"
            "    EvalCase(\n"
            "        question='What is the DSCR covenant?',\n"
            "        expected_keywords=['1.25', 'dscr', 'debt-service'],\n"
            "        expected_source_contains='loan_agreement',\n"
            "    ),\n"
            "    EvalCase(\n"
            "        question='Which approval is required for purchases above NPR 5 lakh?',\n"
            "        expected_keywords=['cfo', 'ceo', 'board', '5,00,000'],\n"
            "        expected_source_contains='internal_control',\n"
            "    ),\n"
            "    EvalCase(\n"
            "        question='List two related-party entities and their nature.',\n"
            "        expected_keywords=['annapurna', 'himal family', 'common director', 'family'],\n"
            "        expected_source_contains='annual_report',\n"
            "    ),\n"
            "    EvalCase(\n"
            "        question='When does the financial year end?',\n"
            "        expected_keywords=['2082', 'ashad', '03-31'],\n"
            "        expected_source_contains=None,\n"
            "    ),\n"
            "]\n"
            "def fn(q):\n"
            "    return rag_answer(q, store, k=4, return_hits=True)\n"
            "rows = evaluate(cases, fn)\n"
            "display(pd.DataFrame(rows))"
        ),
        md("## 9.5 — The Safe-Use Checklist"),
        code(
            "from src.evaluation_utils import SAFE_USE_CHECKLIST\n"
            "print(SAFE_USE_CHECKLIST)"
        ),
        md(
            "## Exercise\n\n"
            "1. Add three of your own eval cases above. Aim for at least one *unanswerable* case.\n"
            "2. Pick the worst-performing case and improve it by **only** changing the chunk size — no LLM swap.\n"
            "3. Discuss with a partner: which failure mode is the most dangerous for your day-to-day work?\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "RAG is *plumbing*, not *judgement*. It improves grounding but does not guarantee correctness. "
            "A score of 100% on five eval cases does not justify using the system unsupervised on a client engagement."
        ),
    ]
    save("09_rag_limitations_and_evaluation.ipynb", cells)


# ===========================================================================
# 10 — Intro to knowledge graphs
# ===========================================================================
def nb_10():
    cells = [
        md(f"# 10 — Intro to Knowledge Graphs\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Understand nodes, edges, relationships.\n"
            "2. See why graphs are useful for *connection* questions (\"who approved what?\").\n"
            "3. Build a small graph from our synthetic data using NetworkX.\n"
            "4. Run three useful graph queries.\n"
        ),
        md(
            "## A knowledge graph in one minute\n\n"
            "* A **node** is a thing (a vendor, an employee, an invoice).\n"
            "* An **edge** is a relationship (`issued`, `approved_by`, `related_to`).\n"
            "* A **graph** is just lots of nodes and edges together.\n\n"
            "Where text-based RAG is good at *\"what does the policy say about X?\"*, "
            "graphs are good at *\"who approved which payment to which related party?\"* — "
            "relationship-heavy questions where the answer is a path, not a paragraph."
        ),
        code(BOOTSTRAP),
        md("## 10.1 — Build the graph"),
        code(
            "from src.graph_utils import build_finance_graph, graph_summary\n"
            "G = build_finance_graph()\n"
            "summary = graph_summary(G)\n"
            "print('Total nodes:', summary['nodes'])\n"
            "print('Total edges:', summary['edges'])\n"
            "print('Nodes by type:')\n"
            "for k, v in summary['node_types'].items():\n"
            "    print(f'  {k:12s} {v}')\n"
            "print('Edges by relation:')\n"
            "for k, v in summary['edge_types'].items():\n"
            "    print(f'  {k:18s} {v}')"
        ),
        md("## 10.2 — Visualise a small subgraph"),
        code(
            "import matplotlib.pyplot as plt\n"
            "from src.graph_utils import draw_subgraph\n"
            "\n"
            "# Pick: the company, two related-party vendors, their first 2 invoices each, and their approvers\n"
            "nodes = ['Himal Trading', 'V004', 'V010', 'E001', 'E002', 'E003']\n"
            "for n in list(nodes):\n"
            "    if n.startswith('V'):\n"
            "        out = [b for _, b, d in G.out_edges(n, data=True) if d.get('rel') == 'issued'][:2]\n"
            "        nodes.extend(out)\n"
            "fig, ax = plt.subplots(figsize=(10, 7))\n"
            "draw_subgraph(G, nodes, ax=ax, title='Related-party vendors and approvers (sample)')\n"
            "plt.show()"
        ),
        md("## 10.3 — Query 1: all invoices issued by a specific vendor"),
        code(
            "from src.graph_utils import find_invoices_for_vendor\n"
            "for inv in find_invoices_for_vendor(G, 'V004')[:10]:\n"
            "    print(f\"  {inv['invoice']:18s} NPR {inv['amount']:>12,.0f}  (date {inv.get('date')})\")"
        ),
        md("## 10.4 — Query 2: employees who approved high-value invoices"),
        code(
            "from src.graph_utils import find_high_value_approvers\n"
            "for row in find_high_value_approvers(G, threshold=500_000)[:15]:\n"
            "    print(f\"  {row['invoice']:18s} NPR {row['amount']:>12,.0f}  approved by  {row['approver']}  ({row['approver_name']})\")"
        ),
        md("## 10.5 — Query 3: related-party transaction paths"),
        code(
            "from src.graph_utils import find_related_party_paths\n"
            "paths = find_related_party_paths(G)\n"
            "print(f'{len(paths)} related-party invoice paths:')\n"
            "for p in paths[:15]:\n"
            "    print(f\"  {p['vendor_name']:35s} → {p['invoice']:16s} NPR {p['amount']:>10,.0f} → approved by {p['approver_name']}\")"
        ),
        md(
            "## Expected output\n\n"
            "* ~120 invoice nodes, ~80 JE nodes, 12 vendors, 8 employees.\n"
            "* The plot shows two related-party vendors (V004 Annapurna, V010 Himal Family) with sample invoices and their approvers.\n"
            "* Query 3 lists every invoice issued by a related-party vendor and who approved it.\n"
        ),
        md(
            "## Exercise\n\n"
            "1. Add an edge to mark `E001` (CEO) as the *spouse* of someone at vendor `V010`. "
            "(Hint: `G.add_edge('E001', 'V010', rel='family_of')`).\n"
            "2. Write a query that returns every employee with a `family_of` edge to a vendor that issued an invoice.\n"
            "3. Sketch on paper: what other relationships from your firm's day-to-day work would be valuable as a graph?"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| `KeyError` on a node | The node wasn't added — check the vendor / employee code. |\n"
            "| Visualisation is unreadable | Pass a smaller `nodes` list; spring layout works best for <30 nodes. |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "Graphs make **connections** very visible — including connections the data does not actually "
            "support. *Always* verify that the relationship encoded as an edge is supported by source evidence."
        ),
    ]
    save("10_intro_to_knowledge_graphs.ipynb", cells)


# ===========================================================================
# 11 — Graph RAG for financial documents
# ===========================================================================
def nb_11():
    cells = [
        md(f"# 11 — Graph RAG for Financial Documents\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Understand the difference between text RAG and Graph RAG.\n"
            "2. Combine graph neighbours + text chunks as context for the LLM.\n"
            "3. See a question where Graph RAG **beats** plain RAG.\n"
        ),
        md(
            "## Text RAG vs Graph RAG\n\n"
            "| Property | Text RAG | Graph RAG |\n"
            "|---|---|---|\n"
            "| Best for | \"What does the policy say?\" | \"Who is connected to whom?\" |\n"
            "| Retrieval unit | Chunks of text | Nodes + edges (paths) |\n"
            "| Strength | Free-form documents | Relationship-heavy data |\n"
            "| Weakness | Multi-hop reasoning is hard | Building/curating the graph is work |\n"
        ),
        code(BOOTSTRAP),
        code(
            "from src.graph_utils import (\n"
            "    build_finance_graph, find_related_party_paths,\n"
            "    find_high_value_approvers, find_invoices_for_vendor,\n"
            ")\n"
            "from src.rag_utils import build_store_from_folder, rag_answer\n"
            "from src.llm_client import ask_llm\n"
            "\n"
            "G = build_finance_graph()\n"
            "store = build_store_from_folder('data/generated/pdf')\n"
            "print('Graph nodes:', len(G), '| Text store chunks:', len(store))"
        ),
        md("## 11.1 — Plain RAG on a relationship question"),
        code(
            "q = ('List every related-party vendor, the invoices they issued, and which employee approved each invoice.')\n"
            "print('--- TEXT RAG ---')\n"
            "print(rag_answer(q, store, k=6))"
        ),
        md(
            "Plain RAG can quote the *policy* on related parties and the *RPT listing* from the PDF, "
            "but it has **no idea who approved each invoice** because that comes from the structured ledger / "
            "approval workflow, not the text. Watch how Graph RAG fixes this."
        ),
        md("## 11.2 — Graph RAG\n\nWe extract the relationships from the graph, format them as text, *then* let the LLM phrase the answer."),
        code(
            "def graph_context_for(question):\n"
            "    # Naive router: pick a graph query based on keywords in the question.\n"
            "    q = question.lower()\n"
            "    if 'related party' in q:\n"
            "        rows = find_related_party_paths(G)\n"
            "        lines = ['Related-party paths from the graph:']\n"
            "        for r in rows:\n"
            "            lines.append(\n"
            "                f\"  - vendor {r['vendor']} ({r['vendor_name']}) issued {r['invoice']} \"\n"
            "                f\"for NPR {r['amount']:,.0f}, approved by {r['approver']} ({r['approver_name']}).\"\n"
            "            )\n"
            "        return '\\n'.join(lines)\n"
            "    if 'high value' in q or 'above' in q:\n"
            "        rows = find_high_value_approvers(G)\n"
            "        return 'High-value approvers:\\n' + '\\n'.join(\n"
            "            f\"  - {r['invoice']} NPR {r['amount']:,.0f} by {r['approver_name']}\" for r in rows\n"
            "        )\n"
            "    return ''\n"
            "\n"
            "def graph_rag_answer(question, k=4):\n"
            "    # 1) gather graph context\n"
            "    g_ctx = graph_context_for(question)\n"
            "    # 2) gather text context\n"
            "    hits = store.search(question, k=k)\n"
            "    t_ctx = '\\n\\n'.join(\n"
            "        f\"[{h['metadata'].get('source')} p.{h['metadata'].get('page','-')}]\\n{h['text']}\" for h in hits\n"
            "    )\n"
            "    # 3) ask the LLM to combine them\n"
            "    prompt = (\n"
            "        f'Question: {question}\\n\\n'\n"
            "        f'GRAPH FACTS:\\n{g_ctx}\\n\\n'\n"
            "        f'DOCUMENT CONTEXT:\\n{t_ctx}\\n\\n'\n"
            "        'Answer the question using the graph facts and the document context. '\n"
            "        'Cite documents by [source, page]. Treat the graph facts as ground-truth for who-approved-what.'\n"
            "    )\n"
            "    return ask_llm(prompt, system='You are a careful CA assistant. Use only the provided context.', temperature=0.1)\n"
            "\n"
            "print('--- GRAPH RAG ---')\n"
            "print(graph_rag_answer(q))"
        ),
        md("## 11.3 — Try more questions"),
        code(
            "for q in [\n"
            "    'Which related-party invoices were approved by the CFO?',\n"
            "    'Which high-value (above NPR 5,00,000) approvals involve a related party?',\n"
            "    'Summarise the loan covenants and any documents that disclose them.',\n"
            "]:\n"
            "    print('Q:', q)\n"
            "    print(graph_rag_answer(q))\n"
            "    print('-' * 80)"
        ),
        md(
            "## Expected output\n\n"
            "* Plain RAG answer in 11.1 *describes* the related-party rules but can't list specific approver-per-invoice.\n"
            "* Graph RAG answer in 11.2 enumerates each path: vendor → invoice → amount → approver.\n"
        ),
        md(
            "## Exercise\n\n"
            "1. Extend `graph_context_for` to recognise a question about *covenants* and include the loan-covenant subgraph.\n"
            "2. Add a new node-type **Department** and connect employees; ask *\"which departments handle high-value approvals?\"*\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| `graph_context_for` returns empty | Add a new keyword route, or include a fallback summary. |\n"
            "| LLM ignores graph facts | Reword the prompt: *\"Treat graph facts as ground-truth; do not contradict them.\"* |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "Graph RAG is only as good as the graph you built. A wrong edge becomes a wrong answer with "
            "high confidence. For real engagements, build the graph from authoritative sources only (the "
            "ERP, signed approvals, official registries)."
        ),
    ]
    save("11_graph_rag_for_financial_documents.ipynb", cells)


# ===========================================================================
# 12 — Agentic RAG intro
# ===========================================================================
def nb_12():
    cells = [
        md(f"# 12 — Agentic RAG (Tool-Using AI)\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Understand what an *AI agent* is in practical terms.\n"
            "2. Wire up four tools: documents, tables, graph, calculator.\n"
            "3. Run a transparent ReAct-style loop and read the trace.\n"
            "4. Apply safe-agent patterns.\n"
        ),
        md(
            "## What is an agent?\n\n"
            "Plain RAG is **one-shot**: retrieve → answer. An **agent** is *iterative*: the LLM is given a "
            "list of tools (functions) it can call, and it decides *which* tool to call next based on what "
            "it has seen so far. We see every step.\n\n"
            "Tools in this notebook:\n"
            "1. `search_documents(query)` — RAG over PDFs.\n"
            "2. `query_table(name, expr)` — pandas-style query over a known CSV/XLSX.\n"
            "3. `query_graph(question)` — canned graph queries.\n"
            "4. `calculate(expr)` — safe arithmetic.\n"
        ),
        code(BOOTSTRAP),
        code(
            "import pandas as pd\n"
            "from pathlib import Path\n"
            "from src.rag_utils import build_store_from_folder, rag_answer\n"
            "from src.graph_utils import build_finance_graph\n"
            "from src.agentic_rag_utils import safe_calc, make_table_tool, make_graph_tool, run_agent\n"
            "\n"
            "# 1) Build the RAG store and the knowledge graph\n"
            "store = build_store_from_folder('data/generated/pdf')\n"
            "G = build_finance_graph()\n"
            "\n"
            "# 2) Load CSV/XLSX into a tables dictionary\n"
            "tables = {\n"
            "    'sales':       pd.read_csv('data/generated/csv/01_sales_transactions.csv'),\n"
            "    'purchases':   pd.read_csv('data/generated/csv/02_purchase_transactions.csv'),\n"
            "    'journals':    pd.read_csv('data/generated/csv/03_journal_entries.csv'),\n"
            "    'vendors':     pd.read_csv('data/generated/csv/04_vendor_master.csv'),\n"
            "    'rpt':         pd.read_excel('data/generated/xlsx/10_related_party_transactions.xlsx'),\n"
            "    'ar_aging':    pd.read_excel('data/generated/xlsx/04_accounts_receivable_aging.xlsx'),\n"
            "}\n"
            "for name, df in tables.items():\n"
            "    print(f'  {name:12s} {df.shape}')"
        ),
        md("## 12.1 — Wire up the four tools"),
        code(
            "def search_documents(query):\n"
            "    answer, hits = rag_answer(query, store, k=4, return_hits=True)\n"
            "    sources = ', '.join(f\"{h['metadata'].get('source')}#p{h['metadata'].get('page','-')}\" for h in hits)\n"
            "    return f'{answer}\\n[sources: {sources}]'\n"
            "\n"
            "tools = {\n"
            "    'search_documents': search_documents,\n"
            "    'query_table':      make_table_tool(tables),\n"
            "    'query_graph':      make_graph_tool(G),\n"
            "    'calculate':        lambda x: str(safe_calc(x)),\n"
            "}\n"
            "print('Tools:', list(tools))"
        ),
        md("## 12.2 — Run the agent on a CA-style task"),
        code(
            "task = (\n"
            "    'Identify all related-party purchases above NPR 5,00,000 from the purchases table, '\n"
            "    'check which vendor is a related party (use the graph), and confirm whether each was '\n"
            "    'approved per the procurement policy (use the documents). Report findings with citations.'\n"
            ")\n"
            "trace = run_agent(task, tools=tools, max_steps=6, verbose=True)\n"
            "print('\\n=== FINAL ANSWER ===')\n"
            "print(trace.answer)"
        ),
        md("## 12.3 — Inspect the trace"),
        code(
            "for s in trace.steps:\n"
            "    print(f'-- step {s[\"step\"]} -- action={s.get(\"action\")}')\n"
            "    print('  input:', (s.get('input') or '')[:200])\n"
            "    if 'observation' in s:\n"
            "        print('  observation:', s['observation'][:200])\n"
            "    print()"
        ),
        md(
            "## Expected output\n\n"
            "The agent typically performs 3-5 actions: one `query_table` for purchases over a threshold, "
            "one `query_graph` for related parties, one `search_documents` to find the approval rule. "
            "On a mock LLM the trace shows the pattern but the answer is canned."
        ),
        md(
            "## Exercise\n\n"
            "1. Run the agent on: *\"Estimate the year-end inventory provision if we doubled the provisioning rate on >365-day items.\"* "
            "(uses table + calculator)\n"
            "2. Lower `max_steps` to 2 and see how the answer degrades.\n"
            "3. Replace `search_documents` with a no-op and see what the agent does instead.\n"
        ),
        md(
            "## Common errors\n\n"
            "| Symptom | Fix |\n"
            "|---|---|\n"
            "| Agent never says FINAL | Lower temperature; verify the system prompt is loaded; raise `max_steps`. |\n"
            "| Wrong table syntax | `query_table` expects `name | expression`; e.g. `purchases | amount > 500000`. |\n"
            "| Mock LLM answer | Set a real key — agents are noticeably better with stronger models. |\n"
        ),
        md(
            "## ⚠️ Professional caution\n\n"
            "Agents have **more autonomy** than plain RAG. The minimum safety hygiene:\n"
            "1. **Bound the loop** (`max_steps`).\n"
            "2. **Safe tools only** — no `exec`, no shell, no internet writes.\n"
            "3. **Log every step** (we do — see the trace) so a reviewer can audit what happened.\n"
            "4. **Never let the agent take real-world actions** (send email, post payments) without a human in the loop."
        ),
    ]
    save("12_agentic_rag_intro.ipynb", cells)


# ===========================================================================
# 13 — Capstone CA assistant
# ===========================================================================
def nb_13():
    cells = [
        md(f"# 13 — Capstone: CA Assistant\n\n{TRAINING_HEADER}"),
        md(
            "## Learning objectives\n"
            "1. Bring it all together: documents + tables + graph + agent.\n"
            "2. Produce a short professional-style report with citations and a limitations footer.\n"
            "3. Adapt the assistant to one of five capstone scenarios.\n"
        ),
        md(
            "## Choose a scenario\n\n"
            "Pick one and run it through the assistant below:\n"
            "1. **Audit risk assistant** — \"What are the top audit risks and which evidence supports each?\"\n"
            "2. **Tax compliance Q&A** — \"What is our tax-compliance status and what action is required by 2082-06-30?\"\n"
            "3. **Financial statement review** — \"Walk me through the loan disclosures vs the loan agreement.\"\n"
            "4. **Internal control review** — \"List approval-threshold violations in the purchases data and the policy rule each violates.\"\n"
            "5. **Related-party transaction assistant** — \"Map every related-party transaction to its Board approval (if any).\"\n"
        ),
        code(BOOTSTRAP),
        code(
            "import pandas as pd\n"
            "from datetime import datetime\n"
            "from pathlib import Path\n"
            "from src.rag_utils import build_store_from_folder, rag_answer\n"
            "from src.graph_utils import build_finance_graph\n"
            "from src.agentic_rag_utils import safe_calc, make_table_tool, make_graph_tool, run_agent\n"
            "from src.llm_client import ask_llm\n"
            "from src.evaluation_utils import SAFE_USE_CHECKLIST\n"
            "\n"
            "store = build_store_from_folder('data/generated/pdf')\n"
            "G = build_finance_graph()\n"
            "tables = {\n"
            "    'sales':     pd.read_csv('data/generated/csv/01_sales_transactions.csv'),\n"
            "    'purchases': pd.read_csv('data/generated/csv/02_purchase_transactions.csv'),\n"
            "    'journals':  pd.read_csv('data/generated/csv/03_journal_entries.csv'),\n"
            "    'vendors':   pd.read_csv('data/generated/csv/04_vendor_master.csv'),\n"
            "    'rpt':       pd.read_excel('data/generated/xlsx/10_related_party_transactions.xlsx'),\n"
            "    'budget':    pd.read_csv('data/generated/csv/08_budget_vs_actual.csv'),\n"
            "}\n"
            "\n"
            "def search_documents(q):\n"
            "    ans, hits = rag_answer(q, store, k=4, return_hits=True)\n"
            "    sources = ', '.join(f\"{h['metadata'].get('source')}#p{h['metadata'].get('page','-')}\" for h in hits)\n"
            "    return f'{ans}\\n[sources: {sources}]'\n"
            "\n"
            "tools = {\n"
            "    'search_documents': search_documents,\n"
            "    'query_table':      make_table_tool(tables),\n"
            "    'query_graph':      make_graph_tool(G),\n"
            "    'calculate':        lambda x: str(safe_calc(x)),\n"
            "}\n"
            "print('Capstone assistant ready. Tools:', list(tools))"
        ),
        md("## 13.1 — Run the capstone task"),
        code(
            "# === EDIT THIS ===\n"
            "scenario_title = 'Internal Control Review — Approval-Threshold Compliance'\n"
            "scenario_task  = (\n"
            "    'For the synthetic company Himal Trading, list every purchase invoice above NPR 5,00,000 '\n"
            "    'from the purchases table; check whether the procurement policy required dual approval '\n"
            "    'for each; check whether the vendor is a related party using the graph; and produce a '\n"
            "    'short findings list with citations to the policy and ledger evidence.'\n"
            ")\n"
            "\n"
            "trace = run_agent(scenario_task, tools=tools, max_steps=6, verbose=True)\n"
            "print('\\n=== FINAL ANSWER ===')\n"
            "print(trace.answer)"
        ),
        md("## 13.2 — Render a professional-style report"),
        code(
            "report_prompt = f'''Convert the following draft findings into a short report for a Chartered \n"
            "Accountant. Sections: (1) Background, (2) Procedures performed, (3) Findings, (4) Recommended \n"
            "actions, (5) Limitations of this AI-assisted review (mention RAG hallucination risk, synthetic data, \n"
            "need for human verification). Keep it under 350 words.\\n\\n'''\n"
            "report_prompt += f'Title: {scenario_title}\\n\\nDraft findings:\\n{trace.answer}'\n"
            "report = ask_llm(report_prompt, system='You are a senior CA writing for a partner.', temperature=0.1)\n"
            "print(report)"
        ),
        md("## 13.3 — Save the report (and a quick log of the agent trace)"),
        code(
            "out_dir = Path('outputs/reports')\n"
            "out_dir.mkdir(parents=True, exist_ok=True)\n"
            "stamp = datetime.now().strftime('%Y%m%d_%H%M%S')\n"
            "report_path = out_dir / f'{stamp}_capstone_report.md'\n"
            "trace_path  = out_dir / f'{stamp}_capstone_trace.md'\n"
            "report_path.write_text(\n"
            "    f'# {scenario_title}\\n\\n*Generated {stamp}*\\n\\n{report}\\n\\n'\n"
            "    f'---\\n\\n## Limitations & safe-use checklist\\n\\n{SAFE_USE_CHECKLIST}\\n',\n"
            "    encoding='utf-8',\n"
            ")\n"
            "trace_lines = []\n"
            "for s in trace.steps:\n"
            "    trace_lines.append(f\"### Step {s['step']} — action: {s.get('action')}\")\n"
            "    trace_lines.append('**Input:** ' + (s.get('input') or '_(none)_'))\n"
            "    trace_lines.append('**Observation:**')\n"
            "    trace_lines.append('```\\n' + (s.get('observation') or '') + '\\n```')\n"
            "trace_path.write_text(\n"
            "    f'# Capstone agent trace\\n\\n{scenario_task}\\n\\n' + '\\n\\n'.join(trace_lines),\n"
            "    encoding='utf-8',\n"
            ")\n"
            "print('Wrote:')\n"
            "print('  ', report_path)\n"
            "print('  ', trace_path)"
        ),
        md(
            "## Exercise\n\n"
            "1. Edit the scenario above to one of the four other capstones and re-run.\n"
            "2. Add an extra section to the report: *\"Three questions I would ask management.\"*\n"
            "3. Compare the AI's findings list with what you would write manually — what did the AI miss? What did it get wrong?\n"
        ),
        md(
            "## ⚠️ Closing professional caution\n\n"
            "What you have built today is a **research assistant**, not an audit conclusion. Every figure, "
            "citation, and policy link must be re-verified by a qualified professional before it informs "
            "any client-facing communication. The synthetic data is benign; real client data demands the "
            "Safe-Use Checklist below."
        ),
        code("print(SAFE_USE_CHECKLIST)"),
    ]
    save("13_capstone_ca_assistant.ipynb", cells)


# ===========================================================================
# Main
# ===========================================================================
def main():
    print("Building ICAN CA RAG notebooks...")
    nb_00(); nb_01(); nb_02(); nb_03(); nb_04(); nb_05(); nb_06()
    nb_07(); nb_08(); nb_09(); nb_10(); nb_11(); nb_12(); nb_13()
    print("Done.")


if __name__ == "__main__":
    main()
