"""Lightweight document loaders for the training set.

Designed to be:
    * beginner-readable (no LangChain document classes)
    * tolerant — missing files print a warning instead of raising
    * uniform — every loader returns a list of ``Document`` dicts with
        ``{"text": str, "metadata": {...}}``
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = ROOT / "data" / "generated"


# ---------------------------------------------------------------------------
# PDF loader (page-by-page)
# ---------------------------------------------------------------------------
def load_pdf(path: str | Path) -> list[dict]:
    """Return one document per *page* with metadata = {source, page}."""
    path = Path(path)
    if not path.exists():
        print(f"[warn] PDF not found: {path}")
        return []
    docs: list[dict] = []
    # Prefer pymupdf for better text extraction; fall back to pypdf.
    try:
        import fitz  # pymupdf
        with fitz.open(path) as pdf:
            for i, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()
                if text:
                    docs.append({
                        "text": text,
                        "metadata": {
                            "source": path.name,
                            "doc_type": _infer_doc_type(path.name),
                            "page": i,
                        },
                    })
    except Exception:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
        for i, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                docs.append({
                    "text": text,
                    "metadata": {
                        "source": path.name,
                        "doc_type": _infer_doc_type(path.name),
                        "page": i,
                    },
                })
    return docs


def _infer_doc_type(filename: str) -> str:
    f = filename.lower()
    if "annual_report" in f: return "annual_report"
    if "audit_planning" in f: return "audit_memo"
    if "internal_control" in f: return "policy"
    if "procurement" in f: return "policy"
    if "tax" in f: return "tax_memo"
    if "loan" in f: return "loan_agreement"
    if "board_minutes" in f: return "minutes"
    if "management_letter" in f: return "management_letter"
    if "nfrs" in f or "accounting_policy" in f: return "policy"
    if "inventory_observation" in f: return "audit_memo"
    return "document"


def load_pdfs_in_folder(folder: str | Path) -> list[dict]:
    folder = Path(folder)
    docs: list[dict] = []
    if not folder.exists():
        print(f"[warn] PDF folder not found: {folder}")
        return docs
    for p in sorted(folder.glob("*.pdf")):
        docs.extend(load_pdf(p))
    return docs


# ---------------------------------------------------------------------------
# Excel loader
# ---------------------------------------------------------------------------
def load_excel(path: str | Path) -> dict[str, pd.DataFrame]:
    """Return a dict {sheet_name: DataFrame}."""
    path = Path(path)
    if not path.exists():
        print(f"[warn] Excel not found: {path}")
        return {}
    return pd.read_excel(path, sheet_name=None, engine="openpyxl")


def excel_to_text_documents(path: str | Path, max_rows: int = 50) -> list[dict]:
    """Convert each sheet to a markdown table — useful for RAG over tables.

    For large sheets we only embed the first ``max_rows`` (rest is truncated and
    a marker is added). This is a deliberately simple approach — production
    pipelines use table-aware retrieval.
    """
    path = Path(path)
    sheets = load_excel(path)
    docs: list[dict] = []
    for sheet_name, df in sheets.items():
        head = df.head(max_rows)
        truncated = len(df) > max_rows
        md = head.to_markdown(index=False)
        text = (
            f"Workbook: {path.name}\n"
            f"Sheet: {sheet_name}\n"
            f"Rows shown: {len(head)} of {len(df)}{' (truncated)' if truncated else ''}\n\n"
            f"{md}"
        )
        docs.append({
            "text": text,
            "metadata": {
                "source": path.name,
                "doc_type": "spreadsheet",
                "sheet": sheet_name,
            },
        })
    return docs


# ---------------------------------------------------------------------------
# CSV loader
# ---------------------------------------------------------------------------
def load_csv(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        print(f"[warn] CSV not found: {path}")
        return pd.DataFrame()
    return pd.read_csv(path)


def csv_to_text_documents(path: str | Path, max_rows: int = 50) -> list[dict]:
    path = Path(path)
    df = load_csv(path)
    if df.empty:
        return []
    head = df.head(max_rows)
    md = head.to_markdown(index=False)
    text = (
        f"CSV file: {path.name}\n"
        f"Rows shown: {len(head)} of {len(df)}{' (truncated)' if len(df) > max_rows else ''}\n\n"
        f"{md}"
    )
    return [{
        "text": text,
        "metadata": {
            "source": path.name,
            "doc_type": "csv",
        },
    }]


# ---------------------------------------------------------------------------
# Plain text / markdown
# ---------------------------------------------------------------------------
def load_text(path: str | Path) -> list[dict]:
    path = Path(path)
    if not path.exists():
        print(f"[warn] Text file not found: {path}")
        return []
    return [{
        "text": path.read_text(encoding="utf-8", errors="ignore"),
        "metadata": {"source": path.name, "doc_type": "text"},
    }]


# ---------------------------------------------------------------------------
# One-call helper for a whole folder (used by Notebook 08)
# ---------------------------------------------------------------------------
def load_folder(folder: str | Path) -> list[dict]:
    """Walk a folder and load every supported file. Sub-folder names become
    ``doc_type`` metadata so participants can filter on them later."""
    folder = Path(folder)
    if not folder.exists():
        print(f"[warn] Folder not found: {folder}")
        return []
    docs: list[dict] = []
    for path in sorted(folder.rglob("*")):
        if path.is_dir():
            continue
        suffix = path.suffix.lower()
        sub = path.parent.name if path.parent != folder else None
        try:
            if suffix == ".pdf":
                docs.extend(load_pdf(path))
            elif suffix in (".xlsx", ".xls"):
                docs.extend(excel_to_text_documents(path))
            elif suffix == ".csv":
                docs.extend(csv_to_text_documents(path))
            elif suffix in (".txt", ".md"):
                docs.extend(load_text(path))
            else:
                continue
        except Exception as e:  # noqa: BLE001
            print(f"[warn] Skipping {path.name}: {type(e).__name__}: {e}")
            continue
        # Tag with subfolder name as doc_type override
        if sub:
            for d in docs[-10:]:  # only the newly added ones in this iteration
                d["metadata"].setdefault("folder", sub)
    return docs
