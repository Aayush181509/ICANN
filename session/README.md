# ICAN Training Session — CA Professionals (Beginner Track)

Seven hands-on notebooks that take an absolute-beginner CA professional from raw Python to a working machine-learning model — all examples use Nepali business / financial data.

## Folder layout

```
session/
├── 01_NumPy_Basics.ipynb           ← arrays, vectorised maths, indexing, filtering
├── 02_Pandas_Basics.ipynb          ← DataFrames, CSV, selection, groupby
├── 03_Matplotlib_Seaborn.ipynb     ← line / bar / pie / hist / box / heatmap
├── 04_Data_Cleaning.ipynb          ← missing values, duplicates, text fixes, outliers
├── 05_Feature_Engineering.ipynb    ← ratios, dates, binning, encoding, scaling
├── 06_Regression.ipynb             ← predict revenue (linear regression)
├── 07_Classification.ipynb         ← predict loan default (logistic + tree)
└── data/                           ← ready-to-share CSV files for all exercises
    ├── monthly_sales.csv           — FY 2081-82 BS revenue / expense / units
    ├── invoices.csv                — 200 invoices with VAT, customer, city, product
    ├── invoices_dirty.csv          — same invoices with deliberate dirtiness (for cleaning)
    ├── nepse_prices.csv            — 12-month prices for NABIL, NTC, NICA, CHCL, HDL
    ├── payroll.csv                 — 25 employees with EPF / SSF / Net Salary
    ├── loans.csv                   — 300 loans with default flag (classification target)
    ├── customers.csv               — 150 customers, credit limit, days past due
    ├── daily_revenue.csv           — 90 days of revenue + ads + footfall + festival
    ├── quarterly_pl.csv            — small P&L for chart demos
    └── trial_balance.csv           — 14-account trial balance for cleaning / pandas demos
```

## Teaching flow

Each notebook follows the same pattern:

1. **Concept** — short markdown explanation tied to a CA scenario
2. **Demonstration** — a working code cell you run live in class
3. **Practice question** — a small, similar exercise for the participant
4. **Solution** — collapsed under a `<details>` block so they try first
5. **Mini-project** at the end — pulls together everything learned

Notebooks are **independent** but build on each other in order. The data folder is referenced as `data/...` from every notebook — keep both side-by-side when sharing.

## Sharing with the class

Zip and share the entire `session/` folder. The participants only need to install:

```
pip install numpy pandas matplotlib seaborn scikit-learn nbformat jupyter
```

## How the data and notebooks were built

The `_build_*.py` and `_generate_data.py` scripts are kept in this folder so you can re-generate or tweak everything later. They are **not** required to teach the class — feel free to delete them before distribution.
