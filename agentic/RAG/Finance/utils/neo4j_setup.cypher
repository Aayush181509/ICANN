// ============================================================
// ICAN Workshop — Neo4j Reset Script
// Run this between demo dry-runs to start with a clean graph
// Neo4j Browser: paste and run, or use: cypher-shell -f neo4j_setup.cypher
// ============================================================

// Step 1: Delete all nodes and relationships
MATCH (n) DETACH DELETE n;

// Step 2: Drop existing indexes (optional — run if you get duplicate-index errors)
// DROP INDEX company_name IF EXISTS;
// DROP INDEX person_name IF EXISTS;
// DROP INDEX metric_name IF EXISTS;

// Step 3: Create indexes for fast lookup
CREATE INDEX company_name IF NOT EXISTS FOR (c:Company) ON (c.name);
CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name);
CREATE INDEX metric_name IF NOT EXISTS FOR (m:FinancialMetric) ON (m.name);
CREATE INDEX year_value IF NOT EXISTS FOR (y:Year) ON (y.value);
CREATE INDEX subsidiary_name IF NOT EXISTS FOR (s:Subsidiary) ON (s.name);
CREATE INDEX auditfirm_name IF NOT EXISTS FOR (a:AuditFirm) ON (a.name);

// Step 4: Seed a minimal test graph (verify connection is working)
CREATE (:Company {name: 'NMB Bank', type: 'Commercial Bank', registration_no: 'B-00024'})
CREATE (:Year {value: '2023'})
CREATE (:Year {value: '2022'});

// Verify
MATCH (n) RETURN labels(n) AS label, count(n) AS count;
