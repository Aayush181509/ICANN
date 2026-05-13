# Section 04: Linking Financial Documents via Knowledge Graphs

**Duration:** ~60 minutes  
**Goal:** Scale the knowledge graph from one document to three — NMB Bank FY2022, NMB Bank FY2023, and Nepal Telecom FY2023 — and connect them via shared entities and cross-year relationships.

---

## The Multi-Document Problem

In CA practice, you rarely analyze a single document:
- Year-over-year trend analysis requires **multiple annual reports**
- Peer comparison requires **reports from different companies**
- Audit work requires connecting **annual reports + financial statements**

A plain RAG system treats each document as a silo. A knowledge graph can **connect** them.

```
NMB Bank AR 2022 ──► Entity Extraction ──┐
                                          │
NMB Bank AR 2023 ──► Entity Extraction ──┼──► Entity Resolution ──► Unified Graph
                                          │         (merge same entities)
Nepal Telecom AR 2023 ► Entity Extraction ──┘

Cross-document edges:
(NMB Bank FY2022) ──[YEAR_OVER_YEAR]──► (NMB Bank FY2023)
(Net Profit 2022) ──[PRIOR_YEAR_OF]──► (Net Profit 2023)
```


```python
import os
import json
import textwrap
from openai import OpenAI
from pypdf import PdfReader
from py2neo import Graph, Node, Relationship
from IPython.display import IFrame
from pyvis.network import Network

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

graph = Graph("bolt://localhost:7687", auth=("neo4j", "icandemo123"))

# Clear graph for fresh start
graph.run("MATCH (n) DETACH DELETE n")
print("Graph cleared. Ready for multi-document extraction.")

DOCS = {
    "nmb_2022" : {
        "path"    : "../data/annual_reports/nmb_bank_annual_report_2022.pdf",
        "company" : "NMB Bank",
        "year"    : "2022",
        "color"   : "#4A90D9"
    },
    "nmb_2023" : {
        "path"    : "../data/annual_reports/nmb_bank_annual_report_2023.pdf",
        "company" : "NMB Bank",
        "year"    : "2023",
        "color"   : "#2471A3"
    },
    "ntc_2023" : {
        "path"    : "../data/annual_reports/nepal_telecom_annual_report_2023.pdf",
        "company" : "Nepal Telecom",
        "year"    : "2023",
        "color"   : "#E67E22"
    },
}
```

## Entity Resolution — Why It Matters

The same real-world entity can appear with different names across documents:

| Document | Name in text |
|----------|-------------|
| NMB AR 2022 | *"NMB Bank"* |
| NMB AR 2023 | *"NMB Bank Ltd."* |
| Financial Statements | *"Nepal Merchant Banking and Finance Company"* |

Without entity resolution, these become **three separate nodes** instead of one. Cross-document queries fail.

We will use GPT-4o-mini to normalize entity names to a canonical form before inserting into Neo4j.


```python
EXTRACTION_PROMPT = """
You are a financial document analyst. Extract structured entities from this annual report excerpt.
Normalize all company/person names to their most common canonical form (e.g., 'NMB Bank' not 'NMB Bank Ltd.').

Return a JSON object with these keys:
{
  "companies": [{"name": str, "type": str, "registration_no": str or null}],
  "persons": [{"name": str, "designation": str}],
  "financial_metrics": [{"name": str, "value": str, "unit": str, "period": str}],
  "subsidiaries": [{"name": str, "ownership_pct": str or null}],
  "audit_firms": [{"name": str}],
  "relationships": [
    {"from": str, "relation": str, "to": str}
  ]
}

Relation types: REPORTED, SUBSIDIARY_OF, AUDITED_BY, CHAIRED_BY, FILED_FOR, LED_BY
Return ONLY valid JSON.
"""

def extract_entities(text: str, doc_key: str) -> dict:
    truncated = text[:3000]  # cost control
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user",   "content": f"Document: {doc_key}\n\nExcerpt:\n{truncated}"}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    return json.loads(resp.choices[0].message.content)

# Load all 3 PDFs and extract entities
doc_entities = {}
for doc_key, meta in DOCS.items():
    reader = PdfReader(meta["path"])
    text = "\n".join(p.extract_text() or "" for p in reader.pages[:8])
    print(f"Extracting entities from {doc_key}...")
    doc_entities[doc_key] = extract_entities(text, doc_key)
    counts = {k: len(v) if isinstance(v, list) else 0 for k, v in doc_entities[doc_key].items()}
    print(f"  → {counts}")

print("\nExtraction complete.")
```


```python
# GPT-4o-mini prompt for entity normalization across documents
# This ensures 'NMB Bank' and 'NMB Bank Ltd.' become the same node

all_company_names = set()
for doc_key, entities in doc_entities.items():
    for c in entities.get("companies", []):
        all_company_names.add(c["name"])
    for c in entities.get("subsidiaries", []):
        all_company_names.add(c["name"])

NORMALIZE_PROMPT = """You are given a list of company names extracted from different financial documents.
Some entries refer to the same real company but with slight name variations.

Return a JSON object mapping each name to its canonical (preferred) name:
{ "original_name": "canonical_name", ... }

Rules:
- Prefer the shorter, cleaner name (e.g., 'NMB Bank' over 'NMB Bank Ltd.')
- Keep names that are clearly distinct separate
Return ONLY valid JSON.
"""

names_list = "\n".join(f"- {n}" for n in sorted(all_company_names))
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": NORMALIZE_PROMPT},
        {"role": "user",   "content": f"Company names:\n{names_list}"}
    ],
    temperature=0,
    response_format={"type": "json_object"}
)
name_map = json.loads(resp.choices[0].message.content)
print("Canonical name mappings:")
for orig, canonical in name_map.items():
    if orig != canonical:
        print(f"  '{orig}' → '{canonical}'")
```


```python
# Merge entities across documents into Neo4j using MERGE (create if not exists)
# Each node gets a SOURCE_DOC property indicating which document it came from

node_registry = {}  # canonical_name -> py2neo Node

def canonical(name: str) -> str:
    return name_map.get(name, name)

def upsert_node(label: str, props: dict, doc_key: str):
    name_key = "name" if "name" in props else "value"
    raw_name = props.get(name_key, "unknown")
    canon_name = canonical(raw_name)

    if canon_name not in node_registry:
        node = Node(label, **{**{k: v for k, v in props.items() if v}, name_key: canon_name})
        node["SOURCE_DOC"] = doc_key
        graph.create(node)
        node_registry[canon_name] = node
    else:
        # Node exists — update SOURCE_DOC to note it appears in multiple docs
        existing = node_registry[canon_name]
        existing_source = existing.get("SOURCE_DOC", "")
        if doc_key not in existing_source:
            existing["SOURCE_DOC"] = existing_source + "," + doc_key
            graph.push(existing)
    return node_registry[canon_name]

for doc_key, entities in doc_entities.items():
    print(f"Inserting nodes from {doc_key}...")
    for c in entities.get("companies", []):        upsert_node("Company",         c, doc_key)
    for p in entities.get("persons", []):           upsert_node("Person",          p, doc_key)
    for m in entities.get("financial_metrics", []): upsert_node("FinancialMetric", m, doc_key)
    for s in entities.get("subsidiaries", []):      upsert_node("Subsidiary",      s, doc_key)
    for a in entities.get("audit_firms", []):       upsert_node("AuditFirm",       a, doc_key)

print(f"\nTotal unique nodes in registry: {len(node_registry)}")
```


```python
# Add intra-document relationships
rel_count = 0
for doc_key, entities in doc_entities.items():
    for rel in entities.get("relationships", []):
        from_name = canonical(rel.get("from", ""))
        to_name   = canonical(rel.get("to", ""))
        rel_type  = rel.get("relation", "").upper().replace(" ", "_")
        if from_name in node_registry and to_name in node_registry:
            r = Relationship(node_registry[from_name], rel_type, node_registry[to_name],
                             SOURCE_DOC=doc_key)
            graph.create(r)
            rel_count += 1

# Add cross-document YEAR_OVER_YEAR relationships for NMB Bank metrics
# Link FY2022 metrics to their FY2023 counterparts
metrics_2022 = {m["name"]: canonical(m["name"]) for m in doc_entities["nmb_2022"].get("financial_metrics", [])}
metrics_2023 = {m["name"]: canonical(m["name"]) for m in doc_entities["nmb_2023"].get("financial_metrics", [])}

for name_22 in metrics_2022:
    # Find matching metric in 2023 (same base name, different period)
    for name_23 in metrics_2023:
        base_22 = name_22.replace("2022", "").replace("FY22", "").strip()
        base_23 = name_23.replace("2023", "").replace("FY23", "").strip()
        if base_22 and base_22 == base_23 and name_22 in node_registry and name_23 in node_registry:
            r = Relationship(node_registry[name_22], "PRIOR_YEAR_OF", node_registry[name_23])
            graph.create(r)
            rel_count += 1
            print(f"  Linked: ({name_22}) -[PRIOR_YEAR_OF]-> ({name_23})")

print(f"\nTotal relationships created: {rel_count}")
```


```python
# Pyvis visualization — nodes color-coded by source document
SOURCE_COLORS = {
    "nmb_2022" : "#AED6F1",  # light blue
    "nmb_2023" : "#2E86C1",  # dark blue
    "ntc_2023" : "#E67E22",  # orange
    "multiple" : "#8E44AD",  # purple = appears in multiple docs
}

all_nodes = graph.run("MATCH (n) RETURN n, labels(n) AS labels").data()
all_rels   = graph.run("MATCH (a)-[r]->(b) RETURN a.name AS fn, a.value AS fv, type(r) AS rel, b.name AS tn, b.value AS tv, r.SOURCE_DOC AS src").data()

net = Network(height="550px", width="100%", notebook=True, cdn_resources="inline")
net.force_atlas_2based()

for row in all_nodes:
    n     = row["n"]
    label = row["labels"][0] if row["labels"] else "Unknown"
    name  = n.get("name") or n.get("value") or "?"
    src   = n.get("SOURCE_DOC", "nmb_2023")
    color = SOURCE_COLORS.get("multiple" if "," in str(src) else src, "#cccccc")
    net.add_node(name, label=name, color=color, title=f"{label} | {src}")

for row in all_rels:
    frm = row["fn"] or row["fv"] or "?"
    to  = row["tn"] or row["tv"] or "?"
    net.add_edge(frm, to, label=row["rel"], arrows="to")

net.save_graph("multi_doc_graph.html")
print("Legend: Light Blue=NMB 2022 | Dark Blue=NMB 2023 | Orange=Nepal Telecom | Purple=Multi-doc")
IFrame("multi_doc_graph.html", width="100%", height="570")
```


```python
# Cypher traversal: All financial metrics for NMB Bank across both years
print("Query: All financial metrics for NMB Bank across FY2022 and FY2023")
print("-" * 65)

results = graph.run("""
    MATCH (c:Company {name: 'NMB Bank'})-[:REPORTED]->(m:FinancialMetric)
    RETURN m.name AS metric, m.value AS value, m.unit AS unit, m.period AS period
    ORDER BY period, metric
""").data()

if results:
    current_period = None
    for r in results:
        if r["period"] != current_period:
            print(f"\n  {r['period'] or 'Unknown period'}:")
            current_period = r["period"]
        print(f"    {r['metric']}: {r['value']} {r.get('unit') or ''}")
else:
    print("  No REPORTED relationships found. (Check entity extraction output.)")
```


```python
# Cypher comparison: NMB Bank vs Nepal Telecom total assets in FY2023
print("Query: Compare NMB Bank vs Nepal Telecom Total Assets in FY2023")
print("-" * 65)

results = graph.run("""
    MATCH (c)-[:REPORTED]->(m:FinancialMetric)
    WHERE (m.name CONTAINS 'Total Asset' OR m.name CONTAINS 'total asset')
      AND (m.period CONTAINS '2023')
    RETURN c.name AS company, m.name AS metric, m.value AS value, m.unit AS unit
    ORDER BY company
""").data()

if results:
    for r in results:
        print(f"  {r['company']}: {r['metric']} = {r['value']} {r.get('unit') or ''}")
else:
    print("  Total Asset metrics not found. Showing all FY2023 metrics instead:")
    results = graph.run("""
        MATCH (c)-[:REPORTED]->(m:FinancialMetric)
        WHERE m.period CONTAINS '2023'
        RETURN c.name AS company, m.name AS metric, m.value AS value
        ORDER BY company, metric LIMIT 10
    """).data()
    for r in results:
        print(f"  [{r['company']}] {r['metric']}: {r['value']}")
```


```python
# Cross-year NMB Bank subgraph visualization
results = graph.run("""
    MATCH (a:FinancialMetric)-[r:PRIOR_YEAR_OF]->(b:FinancialMetric)
    RETURN a.name AS m22, a.value AS v22, b.name AS m23, b.value AS v23
""").data()

if results:
    print("Year-over-year metric linkages (NMB Bank FY2022 → FY2023):")
    print("-" * 60)
    for r in results:
        print(f"  {r['m22']} ({r['v22']}) → {r['m23']} ({r['v23']})")
else:
    print("No PRIOR_YEAR_OF edges found.")
    print("(This link is created when the same metric name appears in both FY2022 and FY2023.)")
```

## What This Enables for CA Professionals

| Use Case | How the Graph Helps |
|----------|--------------------|
| **Audit trail** | Every fact has a `SOURCE_DOC` property — you can always trace which document a number came from |
| **Year-over-year analysis** | Follow `PRIOR_YEAR_OF` edges — no need to manually align columns in Excel |
| **Inter-company comparison** | Both NMB Bank and Nepal Telecom are in the same graph — one query compares them |
| **Relationship queries** | *"Find all companies audited by the same firm as NMB Bank"* is one Cypher pattern |
| **Due diligence** | Quickly surface subsidiaries, board members, and audit history across all documents |

---

> **Next:** Section 05 combines this graph with vector search (from Sections 01–02) into a **GraphRAG pipeline** that handles both factual lookups and relationship traversals in a single query.
