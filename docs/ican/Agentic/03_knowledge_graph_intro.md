# Section 03: Knowledge Graph Basics in Neo4j

**Duration:** ~75 minutes  
**Goal:** Extract financial entities from an NMB Bank annual report, store them in a Neo4j knowledge graph, and write Cypher queries to traverse relationships.

---

## What is a Knowledge Graph?

Imagine reading a **newspaper article** about NMB Bank. A good journalist would capture:
- *Who* is involved (people, companies)
- *What* happened (metrics, events)
- *How* they relate (audited by, subsidiary of, reported in)

A knowledge graph stores exactly this — **entities as nodes** and **relationships as edges**.

**Traditional database** (a table) stores facts in rows:  
```
┌──────────────┬───────────┬──────────────┐
│ Company      │ Metric    │ Value        │
├──────────────┼───────────┼──────────────┤
│ NMB Bank     │ Net Profit│ NPR 2.3B     │
└──────────────┴───────────┴──────────────┘
```

**Knowledge graph** stores connected facts:  
```
(NMB Bank) ──[REPORTED]──► (Net Profit: NPR 2.3B)
     │
     └──[SUBSIDIARY_OF]──► (NMB Microfinance)
     │
     └──[AUDITED_BY]──► (Deloitte Haskins & Sells)
     │
     └──[CHAIRED_BY]──► (Person: Ram Bahadur Khatri)
```

The graph wins when you need to **traverse relationships**: *"Who are the auditors of all subsidiaries of NMB Bank?"*

## Graph vs. Table: When Graph Wins

| Query | Table | Graph |
|-------|-------|-------|
| Find all subsidiaries | Requires JOIN across 3 tables | One Cypher hop: `(c)-[:SUBSIDIARY_OF]->()` |
| Find auditor of a subsidiary | Multiple JOINs + subquery | Two hops: `(c)-[:SUBSIDIARY_OF]->(s)-[:AUDITED_BY]->(a)` |
| Track metric across years | Self-JOIN on year column | Follow `PRIOR_YEAR_OF` edge |
| Who else has the same auditor? | Complex GROUP BY + JOIN | Pattern match: `()-[:AUDITED_BY]->(a)<-[:AUDITED_BY]-()` |

**For CA professionals:** Knowledge graphs naturally represent the structure of audit trails, corporate hierarchies, and multi-year comparisons — the same relationships you reason about daily.


```python
# Connect to Neo4j
# Prerequisites:
#   1. Neo4j Desktop installed and running
#   2. Database named 'ican-finance' created
#   3. Password set to 'icandemo123'

import os
import json
import textwrap
from openai import OpenAI
from pypdf import PdfReader
from py2neo import Graph, Node, Relationship
from IPython.display import display, HTML

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Connect to Neo4j
NEO4J_URI      = "bolt://localhost:7687"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "icandemo123"

graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Test connection
result = graph.run("RETURN 'Neo4j connected!' AS message").data()
print(result[0]["message"])
```

## Entity Types We Will Extract

We will instruct GPT-4o-mini to extract these entity types from the annual report:

| Entity Type | Examples |
|-------------|----------|
| **Company** | NMB Bank, NMB Microfinance |
| **Person** | Board members, CEO, CFO |
| **FinancialMetric** | Net Profit, CAR, Total Assets |
| **Subsidiary** | NMB Microfinance, NMB Capital |
| **AuditFirm** | Deloitte Haskins & Sells |
| **Year** | FY2023, FY2022 |

```
Schema:
  (:Company {name, type, registration_no})
  (:Person {name, designation})
  (:FinancialMetric {name, value, unit, period})
  (:Subsidiary {name, ownership_pct})
  (:AuditFirm {name})
  (:Year {value})
```


```python
# Extract a sample section of the PDF for entity extraction
PDF_PATH = "../data/annual_reports/nmb_bank_annual_report_2023.pdf"
reader = PdfReader(PDF_PATH)

# Use first 5 pages (cover, highlights, board info) + financial highlights pages
# Adjust page range based on your actual PDF structure
sample_pages = reader.pages[:8]
sample_text = "\n".join(p.extract_text() or "" for p in sample_pages)

# Truncate to 3000 chars for the extraction prompt (cost control)
sample_text_truncated = sample_text[:3000]

print(f"Using {len(sample_text_truncated)} characters from first 8 pages.")
print("--- Preview ---")
print(sample_text_truncated[:500])
```


```python
# GPT-4o-mini entity extraction prompt
EXTRACTION_PROMPT = """
You are a financial document analyst. Extract structured entities from this annual report excerpt.

Return a JSON object with these keys:
{
  "companies": [{"name": str, "type": str, "registration_no": str or null}],
  "persons": [{"name": str, "designation": str}],
  "financial_metrics": [{"name": str, "value": str, "unit": str, "period": str}],
  "subsidiaries": [{"name": str, "ownership_pct": str or null}],
  "audit_firms": [{"name": str}],
  "years": [str],
  "relationships": [
    {"from": str, "relation": str, "to": str}
  ]
}

Relationship types allowed: REPORTED, SUBSIDIARY_OF, AUDITED_BY, CHAIRED_BY, FILED_FOR, LED_BY

Return ONLY valid JSON. No markdown, no explanation.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": EXTRACTION_PROMPT},
        {"role": "user",   "content": f"Annual Report Excerpt:\n{sample_text_truncated}"}
    ],
    temperature=0,
    response_format={"type": "json_object"}
)

entities_raw = response.choices[0].message.content
print("Raw extraction output:")
print(entities_raw)
```


```python
# Parse and display the extracted entities
entities = json.loads(entities_raw)

print("=== Extracted Entities ===")
for entity_type, items in entities.items():
    if isinstance(items, list) and items:
        print(f"\n{entity_type.upper()} ({len(items)} found):")
        for item in items:
            print(f"  {item}")
```


```python
# Create nodes in Neo4j for each entity type
# First clear any existing data from previous runs
graph.run("MATCH (n) DETACH DELETE n")
print("Cleared existing graph.")

node_registry = {}  # name -> Node (for relationship creation)

def get_or_create_node(label: str, props: dict, key: str = "name") -> Node:
    name = props.get(key, props.get("value", "unknown"))
    if name in node_registry:
        return node_registry[name]
    node = Node(label, **{k: v for k, v in props.items() if v})
    graph.create(node)
    node_registry[name] = node
    return node

# Companies
for c in entities.get("companies", []):
    get_or_create_node("Company", c)

# Persons
for p in entities.get("persons", []):
    get_or_create_node("Person", p)

# Financial Metrics
for m in entities.get("financial_metrics", []):
    get_or_create_node("FinancialMetric", m)

# Subsidiaries
for s in entities.get("subsidiaries", []):
    get_or_create_node("Subsidiary", s)

# Audit Firms
for a in entities.get("audit_firms", []):
    get_or_create_node("AuditFirm", a)

# Years
for y in entities.get("years", []):
    node = Node("Year", value=y)
    graph.create(node)
    node_registry[y] = node

print(f"Created {len(node_registry)} nodes in Neo4j.")
```


```python
# Create relationships
rel_count = 0
for rel in entities.get("relationships", []):
    from_name = rel.get("from", "")
    to_name   = rel.get("to", "")
    rel_type  = rel.get("relation", "").upper().replace(" ", "_")

    if from_name in node_registry and to_name in node_registry:
        r = Relationship(node_registry[from_name], rel_type, node_registry[to_name])
        graph.create(r)
        rel_count += 1
        print(f"  Created: ({from_name}) -[{rel_type}]-> ({to_name})")
    else:
        missing = [n for n in [from_name, to_name] if n not in node_registry]
        print(f"  Skipped: ({from_name}) -[{rel_type}]-> ({to_name})  [nodes not found: {missing}]")

print(f"\nTotal relationships created: {rel_count}")
```


```python
# Visualize the graph using pyvis (renders as HTML in the notebook)
from pyvis.network import Network
from IPython.display import IFrame

# Fetch all nodes and relationships from Neo4j
all_nodes = graph.run("MATCH (n) RETURN n, labels(n) AS labels").data()
all_rels   = graph.run("MATCH (a)-[r]->(b) RETURN a.name AS from_name, a.value AS from_val, type(r) AS rel, b.name AS to_name, b.value AS to_val").data()

COLOR_MAP = {
    "Company"        : "#4A90D9",
    "Person"         : "#E8A838",
    "FinancialMetric": "#5CB85C",
    "Subsidiary"     : "#9B59B6",
    "AuditFirm"      : "#E74C3C",
    "Year"           : "#95A5A6",
}

net = Network(height="500px", width="100%", notebook=True, cdn_resources="inline")
net.force_atlas_2based()

for row in all_nodes:
    n     = row["n"]
    label = row["labels"][0] if row["labels"] else "Unknown"
    name  = n.get("name") or n.get("value") or "?"
    net.add_node(name, label=name, color=COLOR_MAP.get(label, "#cccccc"), title=label)

for row in all_rels:
    frm = row["from_name"] or row["from_val"] or "?"
    to  = row["to_name"]   or row["to_val"]   or "?"
    net.add_edge(frm, to, label=row["rel"], arrows="to")

graph_html = "nmb_graph.html"
net.save_graph(graph_html)
print("Graph visualization saved. Displaying below:")
IFrame(graph_html, width="100%", height="520")
```


```python
# Cypher Query 1: Find all subsidiaries of NMB Bank
print("Query: Find all subsidiaries of NMB Bank")
print("-" * 50)

results = graph.run("""
    MATCH (c:Company)-[:SUBSIDIARY_OF]->(s:Subsidiary)
    RETURN c.name AS company, s.name AS subsidiary, s.ownership_pct AS ownership
""").data()

if results:
    for r in results:
        ownership = f" ({r['ownership']}% owned)" if r.get('ownership') else ""
        print(f"  {r['company']} → {r['subsidiary']}{ownership}")
else:
    print("  No subsidiary relationships found in this extract.")
    print("  (Run on a larger section of the PDF to populate this.)") 
```


```python
# Cypher Query 2: Who audited this company and in which year?
print("Query: Who audited NMB Bank and in which year?")
print("-" * 50)

results = graph.run("""
    MATCH (c)-[:AUDITED_BY]->(a:AuditFirm)
    OPTIONAL MATCH (c)-[:FILED_FOR]->(y:Year)
    RETURN c.name AS company, a.name AS auditor, collect(y.value) AS years
""").data()

if results:
    for r in results:
        years = ", ".join(r["years"]) if r["years"] else "not specified"
        print(f"  {r['company']} was audited by {r['auditor']} for years: {years}")
else:
    print("  No audit relationships found in this extract.")
```


```python
# Cypher Query 3: Show all financial metrics reported for FY2023
print("Query: Show all financial metrics reported for FY2023")
print("-" * 50)

results = graph.run("""
    MATCH (c)-[:REPORTED]->(m:FinancialMetric)
    WHERE m.period CONTAINS '2023' OR m.period CONTAINS 'FY2023'
    RETURN c.name AS company, m.name AS metric, m.value AS value, m.unit AS unit
    ORDER BY company, metric
""").data()

if results:
    for r in results:
        unit = r.get('unit') or ""
        print(f"  [{r['company']}] {r['metric']}: {r['value']} {unit}")
else:
    # Fallback: show all metrics
    results = graph.run("""
        MATCH (m:FinancialMetric)
        RETURN m.name AS metric, m.value AS value, m.unit AS unit, m.period AS period
        ORDER BY period, metric
    """).data()
    print("  (Showing all extracted financial metrics:)")
    for r in results:
        print(f"  {r['metric']}: {r['value']} {r.get('unit','')} ({r.get('period','')})")
```

## What Cypher Reads Like (SQL Analogy)

CA professionals are familiar with SQL-style thinking. Here is how Cypher maps:

| SQL | Cypher | Meaning |
|-----|--------|---------|
| `SELECT * FROM Company` | `MATCH (c:Company) RETURN c` | Get all companies |
| `JOIN Company ON auditor_id` | `MATCH (c)-[:AUDITED_BY]->(a)` | Follow a relationship |
| `WHERE name = 'NMB Bank'` | `WHERE c.name = 'NMB Bank'` | Filter by property |
| `GROUP BY company` | `WITH c, collect(m)` | Aggregate by node |

**Key difference:** In Cypher, you *draw the pattern* you want to find:  
`(company)-[:AUDITED_BY]->(auditor)` literally reads as *"company audited by auditor"*.

No need to remember foreign keys or JOIN conditions — the relationships are first-class citizens.


```python
# Summary: What is in our Neo4j graph right now?
summary = graph.run("""
    MATCH (n)
    RETURN labels(n)[0] AS label, count(n) AS count
    ORDER BY count DESC
""").data()

print("Current graph contents:")
print("-" * 30)
for row in summary:
    print(f"  {row['label']:<20} : {row['count']} nodes")

rel_count_total = graph.run("MATCH ()-[r]->() RETURN count(r) AS total").data()[0]["total"]
print(f"\n  Relationships      : {rel_count_total}")
print("\nNext step → Section 04: Scale this to 3 documents!")
```
