"""Build and query a knowledge graph over the synthetic CA dataset.

Uses NetworkX (in-memory). Suitable for thousands of nodes; for production-
scale graphs swap in Neo4j or Memgraph with the same interface.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import networkx as nx
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "data" / "generated" / "csv"
XLSX_DIR = ROOT / "data" / "generated" / "xlsx"


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------
def build_finance_graph() -> nx.MultiDiGraph:
    """Build a small but meaningful KG from the CSV / XLSX data.

    Node types: Company, Vendor, Customer, Employee, Account, Invoice, JE,
    Loan, Covenant, Policy. Edge types: ``issued``, ``paid_to``, ``approved_by``,
    ``related_to``, ``has_covenant``, ``requires_approval`` etc.
    """
    G = nx.MultiDiGraph()
    G.add_node("Himal Trading", type="Company", pan="300123456")

    # Vendors
    vmaster = pd.read_csv(CSV_DIR / "04_vendor_master.csv")
    for _, r in vmaster.iterrows():
        G.add_node(r["vendor_code"], type="Vendor", name=r["vendor_name"],
                   pan=r.get("pan", ""), related_party=(r["related_party"] == "Yes"))
        G.add_edge("Himal Trading", r["vendor_code"], rel="buys_from")
        if r["related_party"] == "Yes":
            G.add_edge("Himal Trading", r["vendor_code"], rel="related_party")

    # Customers
    cmaster = pd.read_csv(CSV_DIR / "05_customer_master.csv")
    for _, r in cmaster.iterrows():
        G.add_node(r["customer_code"], type="Customer", name=r["customer_name"],
                   pan=r.get("pan", ""))
        G.add_edge("Himal Trading", r["customer_code"], rel="sells_to")

    # Employees
    employees = [
        ("E001", "Ramesh Shrestha", "CEO"),
        ("E002", "Sita Karki", "CFO"),
        ("E003", "Bikram Thapa", "Procurement Manager"),
        ("E004", "Anju Pradhan", "Accounts Manager"),
        ("E005", "Deepak Adhikari", "Internal Auditor"),
        ("E006", "Meera Gurung", "Store Officer"),
        ("E007", "Prakash Rai", "HR Manager"),
        ("E008", "Sunita Maharjan", "Junior Accountant"),
    ]
    for code, name, designation in employees:
        G.add_node(code, type="Employee", name=name, designation=designation)
        G.add_edge("Himal Trading", code, rel="employs")

    # Invoices (purchases) → Vendor; Invoice approved_by Employee
    purchases = pd.read_csv(CSV_DIR / "02_purchase_transactions.csv")
    for _, r in purchases.iterrows():
        inv_id = r["invoice_no"]
        G.add_node(inv_id, type="Invoice", amount=float(r["amount"]),
                   date=r["date"], approval=r.get("approval_status", ""))
        G.add_edge(r["vendor_code"], inv_id, rel="issued")
        G.add_edge(inv_id, "Himal Trading", rel="payable_by")
        # naive approver assignment: amounts > 5,00,000 → CFO; else PM
        if float(r["amount"]) > 500_000:
            G.add_edge(inv_id, "E002", rel="approved_by")  # CFO
        else:
            G.add_edge(inv_id, "E003", rel="approved_by")  # Procurement Manager

    # Journal entries → Account; posted_by/approved_by Employee
    je = pd.read_csv(CSV_DIR / "03_journal_entries.csv")
    for _, r in je.iterrows():
        jid = r["je_no"]
        G.add_node(jid, type="JE", amount=float(r["amount"]), date=r["date"],
                   narration=r.get("narration", ""))
        # Connect accounts
        G.add_node(r["account_debit"], type="Account")
        G.add_node(r["account_credit"], type="Account")
        G.add_edge(jid, r["account_debit"], rel="debits")
        G.add_edge(jid, r["account_credit"], rel="credits")
        if r["posted_by"]:
            G.add_edge(jid, r["posted_by"], rel="posted_by")
        if r["approved_by"]:
            G.add_edge(jid, r["approved_by"], rel="approved_by")

    # Loan → Covenants
    G.add_node("LOAN-NCB-001", type="Loan", lender="Nepal Commercial Bank Ltd.",
               principal=200_000_000, rate=0.105, tenor_years=7)
    G.add_edge("Himal Trading", "LOAN-NCB-001", rel="has_loan")
    for cname, threshold in [("DSCR>=1.25", 1.25), ("D/E<=2.0", 2.0), ("CR>=1.10", 1.10)]:
        G.add_node(cname, type="Covenant", threshold=threshold)
        G.add_edge("LOAN-NCB-001", cname, rel="has_covenant")

    # Policies → Roles
    G.add_node("Procurement Policy", type="Policy")
    G.add_node("Internal Control Policy", type="Policy")
    G.add_edge("Procurement Policy", "E002", rel="requires_approval")   # CFO
    G.add_edge("Procurement Policy", "E003", rel="requires_approval")   # PM
    G.add_edge("Internal Control Policy", "E002", rel="requires_approval")
    G.add_edge("Internal Control Policy", "E001", rel="requires_approval")  # CEO for >5L

    return G


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------
def neighbours(G: nx.MultiDiGraph, node: str, rel: str | None = None) -> list[tuple[str, str]]:
    """Return [(neighbour, rel), ...] outgoing from ``node``."""
    out = []
    if node not in G:
        return out
    for _, nb, data in G.out_edges(node, data=True):
        if rel is None or data.get("rel") == rel:
            out.append((nb, data.get("rel", "")))
    return out


def find_invoices_for_vendor(G: nx.MultiDiGraph, vendor_code: str) -> list[dict]:
    out = []
    for _, inv, data in G.out_edges(vendor_code, data=True):
        if data.get("rel") == "issued":
            out.append({"invoice": inv, **G.nodes[inv]})
    return out


def find_high_value_approvers(G: nx.MultiDiGraph, threshold: float = 500_000) -> list[dict]:
    """Find all invoices over `threshold` and the employees that approved them."""
    out = []
    for n, attrs in G.nodes(data=True):
        if attrs.get("type") != "Invoice":
            continue
        if attrs.get("amount", 0) < threshold:
            continue
        approver = None
        for _, nb, d in G.out_edges(n, data=True):
            if d.get("rel") == "approved_by":
                approver = nb
                break
        if approver:
            out.append({
                "invoice": n,
                "amount": attrs["amount"],
                "approver": approver,
                "approver_name": G.nodes[approver].get("name"),
            })
    return out


def find_related_party_paths(G: nx.MultiDiGraph) -> list[dict]:
    """Return every (Company → Vendor → Invoice → Approver) path
    where the vendor is flagged as a related party."""
    out = []
    for v, attrs in G.nodes(data=True):
        if attrs.get("type") != "Vendor" or not attrs.get("related_party"):
            continue
        for _, inv, d in G.out_edges(v, data=True):
            if d.get("rel") != "issued":
                continue
            inv_attrs = G.nodes[inv]
            approver = None
            for _, ap, dd in G.out_edges(inv, data=True):
                if dd.get("rel") == "approved_by":
                    approver = ap
                    break
            out.append({
                "vendor": v,
                "vendor_name": attrs.get("name"),
                "invoice": inv,
                "amount": inv_attrs.get("amount"),
                "approver": approver,
                "approver_name": G.nodes[approver].get("name") if approver else None,
            })
    return out


def find_documents_connected_to_loan(G: nx.MultiDiGraph) -> list[dict]:
    out = []
    for _, n, d in G.out_edges("LOAN-NCB-001", data=True):
        out.append({"item": n, "rel": d.get("rel"), **G.nodes[n]})
    return out


def graph_summary(G: nx.MultiDiGraph) -> dict:
    """Return counts by node-type / edge-type — used in notebook 10."""
    nt: dict[str, int] = {}
    for _, a in G.nodes(data=True):
        nt[a.get("type", "Unknown")] = nt.get(a.get("type", "Unknown"), 0) + 1
    et: dict[str, int] = {}
    for _, _, d in G.edges(data=True):
        et[d.get("rel", "?")] = et.get(d.get("rel", "?"), 0) + 1
    return {"nodes": len(G), "edges": G.number_of_edges(),
            "node_types": nt, "edge_types": et}


# ---------------------------------------------------------------------------
# Visualisation helper
# ---------------------------------------------------------------------------
def draw_subgraph(G: nx.MultiDiGraph, nodes: Iterable[str], ax=None, title: str = ""):
    """Quick matplotlib draw of a small subgraph (for notebook display)."""
    import matplotlib.pyplot as plt
    sub = G.subgraph(nodes).copy()
    pos = nx.spring_layout(sub, seed=7, k=0.9)
    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 6))
    color_map = {
        "Company": "#1f77b4", "Vendor": "#ff7f0e", "Customer": "#2ca02c",
        "Employee": "#d62728", "Invoice": "#9467bd", "JE": "#8c564b",
        "Loan": "#e377c2", "Covenant": "#7f7f7f", "Policy": "#bcbd22",
        "Account": "#17becf",
    }
    colors = [color_map.get(sub.nodes[n].get("type", ""), "#cccccc") for n in sub.nodes]
    labels = {n: f"{n}\n{sub.nodes[n].get('name','')}" for n in sub.nodes}
    nx.draw(sub, pos, ax=ax, node_color=colors, with_labels=True, labels=labels,
            node_size=1400, font_size=8, edge_color="#888", arrows=True)
    edge_labels = {(u, v): d.get("rel", "") for u, v, d in sub.edges(data=True)}
    nx.draw_networkx_edge_labels(sub, pos, edge_labels=edge_labels, ax=ax, font_size=7)
    ax.set_title(title)
    ax.axis("off")
    return ax
