"""A minimal, transparent ReAct-style agent for the capstone notebook.

Design goals
------------
* Beginner-readable: no LangChain / no LangGraph / no Anthropic-tool-use API.
* Transparent: every step is printed (Thought → Action → Observation).
* Bounded: max 6 iterations, safe Python evaluator for arithmetic.
* Tools wired up:
    1. search_documents(query)   — RAG over the vector store
    2. query_table(name, expr)   — small pandas expression on a known CSV/XLSX
    3. query_graph(question)     — pre-built KG canned queries
    4. calculate(expression)     — safe numeric eval
"""
from __future__ import annotations

import ast
import operator as op
import re
from dataclasses import dataclass
from typing import Callable

import pandas as pd
import networkx as nx

from .llm_client import ask_llm
from .graph_utils import (
    find_invoices_for_vendor,
    find_high_value_approvers,
    find_related_party_paths,
    find_documents_connected_to_loan,
)


# ---------------------------------------------------------------------------
# Tool 4: safe arithmetic
# ---------------------------------------------------------------------------
_OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg,
    ast.Mod: op.mod, ast.FloorDiv: op.floordiv,
}


def safe_calc(expr: str):
    """Evaluate a numeric expression (no names, no calls). Used by the agent."""
    expr = expr.strip().strip("`")
    tree = ast.parse(expr, mode="eval")

    def _ev(node):
        if isinstance(node, ast.Expression):
            return _ev(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_ev(node.left), _ev(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
            return _OPS[type(node.op)](_ev(node.operand))
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    return _ev(tree)


# ---------------------------------------------------------------------------
# Tool 2: pandas query
# ---------------------------------------------------------------------------
def make_table_tool(tables: dict[str, pd.DataFrame]) -> Callable[[str, str], str]:
    """Returns a tool function ``query_table(name, expr)`` bound to the given
    dictionary of DataFrames. ``expr`` is a pandas-style expression evaluated
    via DataFrame.query / DataFrame.eval — no arbitrary Python."""

    def _tool(name: str, expr: str) -> str:
        if name not in tables:
            return f"Unknown table '{name}'. Available: {list(tables)}"
        df = tables[name]
        try:
            # Allow simple .query() with backticks for column names
            result = df.query(expr) if expr else df
        except Exception as e:  # noqa: BLE001
            return f"Query error: {e}"
        return result.head(15).to_markdown(index=False)

    return _tool


# ---------------------------------------------------------------------------
# Tool 3: graph canned queries
# ---------------------------------------------------------------------------
def make_graph_tool(G: nx.MultiDiGraph) -> Callable[[str], str]:
    def _tool(question: str) -> str:
        q = question.lower()
        if "related party" in q:
            paths = find_related_party_paths(G)
            if not paths:
                return "No related-party invoice paths found."
            lines = ["Related-party invoice paths:"]
            for p in paths[:20]:
                lines.append(
                    f"  - {p['vendor_name']} ({p['vendor']}) → "
                    f"invoice {p['invoice']} (NPR {p['amount']:,.0f}) → "
                    f"approved by {p['approver_name']}"
                )
            return "\n".join(lines)
        if "high value" in q or "above" in q:
            # extract a number if present
            m = re.search(r"([\d,]{4,})", question)
            thr = int(m.group(1).replace(",", "")) if m else 500_000
            rows = find_high_value_approvers(G, threshold=thr)
            if not rows:
                return f"No invoices above NPR {thr:,.0f}."
            lines = [f"Invoices above NPR {thr:,.0f}:"]
            for r in rows[:20]:
                lines.append(
                    f"  - {r['invoice']} (NPR {r['amount']:,.0f}) "
                    f"approved by {r['approver_name']}"
                )
            return "\n".join(lines)
        if "loan" in q or "covenant" in q:
            items = find_documents_connected_to_loan(G)
            return "Loan-connected items: " + ", ".join(i["item"] for i in items)
        # Fallback: vendor invoices
        m = re.search(r"\bV\d{3}\b", question)
        if m:
            invs = find_invoices_for_vendor(G, m.group(0))
            if not invs:
                return f"No invoices for vendor {m.group(0)}."
            lines = [f"Invoices for {m.group(0)}:"]
            for i in invs[:20]:
                lines.append(f"  - {i['invoice']} (NPR {i['amount']:,.0f})")
            return "\n".join(lines)
        return ("Graph tool supports: 'related party paths', 'high value above <amount>', "
                "'loan / covenant', and vendor codes like V004.")

    return _tool


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
AGENT_SYSTEM = """\
You are a careful CA-Assistant agent. You answer audit/tax/accounting
questions by calling tools. Always think before you act.

You have these tools:
  - search_documents(query)        → returns relevant paragraphs from PDFs
  - query_table(table, expression) → query a CSV/XLSX as pandas (use .query syntax)
  - query_graph(question)          → asks the knowledge graph
  - calculate(expression)          → evaluates simple arithmetic

Respond in this exact format, one block per step:

Thought: <what you want to do and why>
Action: <one of: search_documents, query_table, query_graph, calculate, FINAL>
Action Input: <the argument(s) for the action>

When you have enough information, respond with:

Thought: I now know the final answer.
Action: FINAL
Action Input: <the final answer for the user, with citations where possible>

Rules:
  * Use at most 6 steps.
  * If a tool fails, try a different one.
  * Never invent facts. If tools cannot answer, say so in the final answer.
"""


@dataclass
class AgentTrace:
    question: str
    steps: list[dict]
    answer: str


_ACTION_RE = re.compile(r"Action:\s*(\w+)", re.IGNORECASE)
_INPUT_RE = re.compile(r"Action Input:\s*(.*)", re.IGNORECASE | re.DOTALL)


def _parse(step_text: str) -> tuple[str | None, str]:
    a = _ACTION_RE.search(step_text or "")
    i = _INPUT_RE.search(step_text or "")
    action = a.group(1).strip() if a else None
    inp = i.group(1).strip() if i else ""
    # cut off subsequent "Thought:" so the input is clean
    inp = re.split(r"\nThought:|\nObservation:", inp, maxsplit=1)[0].strip()
    return action, inp


def run_agent(
    question: str,
    tools: dict[str, Callable],
    model: str | None = None,
    max_steps: int = 6,
    verbose: bool = True,
) -> AgentTrace:
    """A tiny ReAct-style loop. ``tools`` is a dict of name → callable."""
    history: list[str] = []
    trace: list[dict] = []

    for step in range(1, max_steps + 1):
        prompt = (
            f"Question: {question}\n\n"
            + "\n".join(history)
            + "\n\nWhat is the next step?"
        )
        raw = ask_llm(prompt, system=AGENT_SYSTEM, model=model, temperature=0.0)
        if verbose:
            print(f"\n— Step {step} —\n{raw}\n")
        action, action_input = _parse(raw)
        trace.append({"step": step, "raw": raw, "action": action, "input": action_input})

        if action is None:
            history.append(raw)
            continue

        if action.upper() == "FINAL":
            return AgentTrace(question=question, steps=trace, answer=action_input)

        tool = tools.get(action)
        if tool is None:
            obs = f"Unknown tool '{action}'. Available: {list(tools)}"
        else:
            try:
                if action == "query_table":
                    # input format: name | expression
                    if "|" in action_input:
                        nm, ex = action_input.split("|", 1)
                        obs = tool(nm.strip(), ex.strip())
                    else:
                        obs = tool(action_input.strip(), "")
                else:
                    obs = tool(action_input)
            except Exception as e:  # noqa: BLE001
                obs = f"Tool error: {type(e).__name__}: {e}"

        obs_text = str(obs)
        if verbose:
            print(f"Observation: {obs_text[:500]}{' ...[truncated]' if len(obs_text) > 500 else ''}")
        history.append(raw + f"\nObservation: {obs_text}")
        trace[-1]["observation"] = obs_text

    return AgentTrace(
        question=question, steps=trace,
        answer="(Max steps reached without a FINAL answer.)",
    )
