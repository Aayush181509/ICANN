"""Tiny RAG evaluation helpers used in Notebook 09.

Deliberately simple — no RAGAS / external eval libs. The point is to teach
*how to think* about evaluation, not to ship a metric harness.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class EvalCase:
    question: str
    expected_keywords: list[str]
    expected_source_contains: str | None = None
    notes: str | None = None


def keyword_score(answer: str, keywords: list[str]) -> float:
    """Fraction of expected keywords present in the answer (case-insensitive)."""
    if not keywords:
        return 0.0
    a = (answer or "").lower()
    hits = sum(1 for k in keywords if k.lower() in a)
    return hits / len(keywords)


def source_hit(hits: list[dict], substring: str) -> bool:
    return any(substring.lower() in (h["metadata"].get("source", "").lower())
               for h in hits)


def evaluate(
    cases: list[EvalCase],
    answer_fn: Callable[[str], tuple[str, list[dict]]],
) -> list[dict]:
    """Run each case through ``answer_fn`` and return a row per case."""
    rows = []
    for c in cases:
        answer, hits = answer_fn(c.question)
        kw = keyword_score(answer, c.expected_keywords)
        src_ok = source_hit(hits, c.expected_source_contains) if c.expected_source_contains else None
        rows.append({
            "question": c.question,
            "answer": answer,
            "n_hits": len(hits),
            "keyword_coverage": round(kw, 2),
            "expected_source_retrieved": src_ok,
            "notes": c.notes,
        })
    return rows


SAFE_USE_CHECKLIST = """\
Professional safe-use checklist (CA edition)

[ ] I have verified every figure cited by the AI against the source workpaper.
[ ] The cited source filename and page exist and contain the cited fact.
[ ] No confidential client data was sent to a public LLM provider without
    documented client consent and engagement-letter authority.
[ ] Where AI was used, the engagement file records: tool, model, prompt,
    retrieved sources, and the human reviewer.
[ ] Any tax, audit, or accounting conclusion has been signed off by a
    qualified professional.
[ ] Currency of laws and standards (NRB / IRD / ICAN / NFRS) was independently
    confirmed against official sources, not the LLM.
"""
