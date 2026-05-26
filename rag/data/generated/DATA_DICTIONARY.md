# Data Dictionary — ICAN CA RAG Training (Synthetic Data)

All data below is **synthetic**. The fictional company is
**Himal Trading & Manufacturing Pvt. Ltd.** (PAN 300123456), with year-end
**2082-03-31** (Nepali FY 2081/82). No real entity is referenced.

> **Teaching-friendly issues** have been intentionally seeded across the data set.
> Look for them with your participants.

---

## PDF documents — `data/generated/pdf/`

| # | File | Purpose | Notable items to discover |
|---|---|---|---|
| 01 | `01_annual_report_extract.pdf`        | Directors' report, KPIs, borrowings, RPT, going concern | Cross-refs to loan agreement and RPT listing |
| 02 | `02_audit_planning_memo.pdf`          | Risks, materiality, team                                | 5 significant risks; performance materiality NPR 15.75 lakh |
| 03 | `03_internal_control_policy.pdf`      | Segregation, approval matrix, vendor master controls    | Three-tier approval thresholds; exception register |
| 04 | `04_procurement_policy.pdf`           | 3-quote rule, 3-way match, related-party rule           | Tender required > NPR 10,00,000 |
| 05 | `05_tax_compliance_memo.pdf`          | IT, VAT, TDS status                                     | Open exposures incl. transfer pricing |
| 06 | `06_loan_agreement_summary.pdf`       | Covenants, security, EoD                                | DSCR ≥ 1.25x, D/E ≤ 2.0x, CR ≥ 1.10x |
| 07 | `07_board_minutes.pdf`                | RPT approvals, IA findings                              | Family entities approved; sole-source flagged |
| 08 | `08_management_letter.pdf`            | Findings from audit                                     | Duplicate vendors, missing PAN, IT shared IDs |
| 09 | `09_nfrs_accounting_policy_note.pdf`  | Revenue/inventory/PPE/FI/RPT policies                   | NFRS 15, NAS 2, NAS 16, NFRS 9, NAS 24 |
| 10 | `10_inventory_observation_memo.pdf`   | Physical count exceptions                               | Variances at 3 locations; slow-moving 4.7% |

## Excel workbooks — `data/generated/xlsx/`

| # | File | Sheets | Notes |
|---|---|---|---|
| 01 | `01_trial_balance.xlsx`              | TB                              | 20 accounts, totals row |
| 02 | `02_general_ledger_sample.xlsx`      | GL_Sales / GL_Purchases / GL_Adjustments | JE-0099 round-number, late-night, junior-posted |
| 03 | `03_fixed_asset_register.xlsx`       | FAR                             | 8 assets with NBV |
| 04 | `04_accounts_receivable_aging.xlsx`  | AR_Aging                        | C004 flat aging (RPT signal); C008 fully overdue |
| 05 | `05_inventory_listing.xlsx`          | Inventory                       | RM-027 / FG-205 / FG-509 slow / obsolete |
| 06 | `06_bank_reconciliation.xlsx`        | Bank_Recon / Outstanding_Items  | Stale cheques outstanding > 170 days |
| 07 | `07_loan_schedule.xlsx`              | Loan_Schedule / Covenants       | EMI table + covenant tracker |
| 08 | `08_tax_computation.xlsx`            | Income_Tax / VAT / TDS          | Income-tax refund of NPR 16 lakh; late TDS |
| 09 | `09_audit_checklist.xlsx`            | Checklist                       | 11 audit procedures with status |
| 10 | `10_related_party_transactions.xlsx` | RPT                             | One un-approved entry on 2082-02-20 |

## CSV transactional files — `data/generated/csv/`

| # | File | Rows ≈ | Teaching trigger |
|---|---|---|---|
| 01 | `01_sales_transactions.csv`     | 121 | Round-number RPT sale on year-end |
| 02 | `02_purchase_transactions.csv`  | 103 | **Duplicate invoice numbers**, vendor-name variants |
| 03 | `03_journal_entries.csv`        |  82 | Self-approved JE-9001; missing approver JE-9002 |
| 04 | `04_vendor_master.csv`          |  12 | V006 missing PAN; V011/V012 are duplicates of V001/V003 |
| 05 | `05_customer_master.csv`        |   8 | C006 missing PAN; C004 is a related party |
| 06 | `06_payroll_summary.csv`        |   8 | Salary, SSF, TDS, net |
| 07 | `07_expense_claims.csv`         |  40 | Some without receipts; rare un-approved claims |
| 08 | `08_budget_vs_actual.csv`       |   9 | Revenue +8%, COGS +7%, Utilities +15% |
| 09 | `09_inventory_movements.csv`    | 150 | Stock movement journal |
| 10 | `10_risk_register.csv`          |  10 | Used in capstone risk-mapping |

---

## How to use this in the training

* **Notebook 03** — open every file type and preview.
* **Notebook 05** — RAG over PDFs only.
* **Notebook 07** — multi-document RAG combining PDFs + structured ledgers.
* **Notebook 09** — pick three failures and reproduce them (e.g. ask a question outside the corpus).
* **Notebook 10/11** — build a graph: Vendor → Invoice → Approver; query related-party paths.
* **Notebook 12/13** — capstone agent that pulls from PDFs, queries CSVs, and walks the graph.

---

## Reproducibility

All data is deterministically generated from seed `20260526` in
`src/data_generation.py`. Re-running the script overwrites the existing files.
