"""Build session/04_Data_Cleaning.ipynb"""
from pathlib import Path
from _nb_helper import md, code, save_notebook

C = []

C.append(md(r"""
# Notebook 4 — Data Cleaning for CA Professionals

**Goal:** Take messy real-world financial data and make it analysis-ready.

**You will learn:**
1. Why "real" data is always dirty
2. Spotting missing values
3. Filling or dropping missing values
4. Removing duplicate rows
5. Cleaning text columns (extra spaces, wrong case)
6. Fixing data types (numbers stored as text, dates as strings)
7. Detecting outliers
8. Renaming columns
9. A short mini-project on a dirty invoice file

> We will mostly use `data/invoices_dirty.csv` — a deliberately messy version of the invoice file.

---
"""))

# Section 1
C.append(md(r"""
## 1. Why is real data dirty?

Open any client's accounting export and you'll typically find:

| Problem               | Example                                       |
|-----------------------|-----------------------------------------------|
| Missing values        | blank `Amount` cells                          |
| Duplicate rows        | the same invoice entered twice               |
| Inconsistent text     | `"himalayan traders "`  vs  `"EVEREST SUPPLIERS"` |
| Wrong data types      | amount stored as text, date as string         |
| Outliers / typos      | a NPR 90 lakh invoice that should be 90,000  |

If we model or chart this data without cleaning, the results will be **wrong** — a serious risk in audit & assurance work.
"""))

C.append(code(r"""
import pandas as pd
import numpy as np

inv = pd.read_csv("data/invoices_dirty.csv")
print("Shape:", inv.shape)
inv.head()
"""))

# Section 2
C.append(md(r"""
## 2. Spotting missing values
"""))

C.append(code(r"""
# True wherever a cell is missing
inv.isna().head()
"""))

C.append(code(r"""
# How many missing per column?
inv.isna().sum()
"""))

C.append(md(r"""
### Practice 1
Find how many missing values each column of `inv` has, and what % of rows are missing in `Amount_NPR`.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
print(inv.isna().sum())
pct = inv["Amount_NPR"].isna().mean() * 100
print(f"\nMissing in Amount_NPR: {pct:.2f}%")
"""))
C.append(md(r"""</details>"""))

# Section 3
C.append(md(r"""
## 3. Handling missing values

You have three common choices:

| Approach   | When to use                                                   |
|------------|----------------------------------------------------------------|
| Drop rows  | A handful of rows missing in a critical column                |
| Fill with 0 | Missing means "no value" (e.g. no discount applied)          |
| Fill with mean / median | Missing because of bad entry, but the row is otherwise valid |
""")
)

C.append(code(r"""
# Method 1 — drop any row that has a missing value
clean1 = inv.dropna()
print("Rows before:", len(inv), "→ after drop:", len(clean1))
"""))

C.append(code(r"""
# Method 2 — fill missing Amount_NPR with the median (more robust than mean)
clean2 = inv.copy()
median_amt = clean2["Amount_NPR"].median()
clean2["Amount_NPR"] = clean2["Amount_NPR"].fillna(median_amt)

# Fill missing City with the string "Unknown"
clean2["City"] = clean2["City"].fillna("Unknown")

print("Missing after fill:")
print(clean2.isna().sum())
"""))

C.append(md(r"""
### Practice 2
Make a copy of `inv` called `inv2`. In `inv2`:

1. Fill missing `Amount_NPR` with the column's **mean**.
2. Fill missing `City` with the value `"Not Provided"`.
3. Confirm there are no missing values left.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
inv2 = inv.copy()
inv2["Amount_NPR"] = inv2["Amount_NPR"].fillna(inv2["Amount_NPR"].mean())
inv2["City"]       = inv2["City"].fillna("Not Provided")
print(inv2.isna().sum())
"""))
C.append(md(r"""</details>"""))

# Section 4
C.append(md(r"""
## 4. Removing duplicate rows

Duplicates can sneak in when invoices are re-uploaded or merged from two files.
"""))

C.append(code(r"""
# Total duplicate rows
print("Duplicate rows:", inv.duplicated().sum())

# Drop them, keep the first occurrence
inv_dedup = inv.drop_duplicates()
print("After dedup    :", len(inv_dedup))
"""))

C.append(code(r"""
# Often we only care about duplicates in a key column like Invoice_No
print("Duplicate Invoice_No:", inv.duplicated(subset=["Invoice_No"]).sum())
inv_unique_inv = inv.drop_duplicates(subset=["Invoice_No"])
print("After dedup by Invoice_No:", len(inv_unique_inv))
"""))

C.append(md(r"""
### Practice 3
1. How many rows in `inv` have a **duplicate `Invoice_No`**?
2. Keep only the **first** occurrence and store the result in `inv_clean`.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
print("Duplicate Invoice_No:", inv.duplicated(subset=["Invoice_No"]).sum())
inv_clean = inv.drop_duplicates(subset=["Invoice_No"], keep="first")
print("Final rows:", len(inv_clean))
"""))
C.append(md(r"""</details>"""))

# Section 5
C.append(md(r"""
## 5. Cleaning text columns

Text is the most common source of subtle bugs — `" Himalayan Traders "` and `"HIMALAYAN TRADERS"` look the same to us, but Pandas treats them as **different customers**.
"""))

C.append(code(r"""
# Look — same customer, three different versions
print(inv["Customer"].value_counts().head(8))
"""))

C.append(code(r"""
# Standard recipe: strip spaces + put in title-case
inv["Customer"] = inv["Customer"].str.strip().str.title()
print(inv["Customer"].value_counts().head(8))
"""))

C.append(md(r"""
### Practice 4
Notice that some `Customer` values are still capitalised differently (e.g. `"Everest Suppliers"` vs `"EVEREST SUPPLIERS"`). Confirm they are all consistent **now** using `.unique()`.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
print(inv["Customer"].unique())
print("Distinct customers:", inv["Customer"].nunique())
"""))
C.append(md(r"""</details>"""))

# Section 6
C.append(md(r"""
## 6. Fixing data types

A common headache: **numbers that came in as text**, or **dates that are just strings**.
"""))

C.append(code(r"""
print(inv.dtypes)
"""))

C.append(code(r"""
# Convert Date column from string → real datetime
inv["Date"] = pd.to_datetime(inv["Date"])

# Now we can extract year, month, weekday, etc.
inv["Year"]    = inv["Date"].dt.year
inv["Month"]   = inv["Date"].dt.month
inv["Weekday"] = inv["Date"].dt.day_name()

inv[["Date", "Year", "Month", "Weekday"]].head()
"""))

C.append(md(r"""
### Practice 5
Suppose someone gives you this Series of amounts where the values are stored as **strings with commas**:
`["1,250", "3,400", "12,800", "5,000"]`

Convert it into a real numeric Series and find the total.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
s = pd.Series(["1,250", "3,400", "12,800", "5,000"])
nums = s.str.replace(",", "").astype(int)
print(nums)
print("Total:", nums.sum())
"""))
C.append(md(r"""</details>"""))

# Section 7
C.append(md(r"""
## 7. Detecting outliers — the IQR method

The **IQR (Inter-Quartile Range) method** is a standard, safe way to flag suspicious values:

1. `Q1` = 25th percentile.
2. `Q3` = 75th percentile.
3. `IQR = Q3 − Q1`.
4. Anything below `Q1 − 1.5·IQR` or above `Q3 + 1.5·IQR` is considered an **outlier**.
"""))

C.append(code(r"""
amt = inv["Amount_NPR"].dropna()

q1, q3 = amt.quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr

print(f"Q1 = {q1:,.0f}   Q3 = {q3:,.0f}   IQR = {iqr:,.0f}")
print(f"Acceptable range: {low:,.0f}  →  {high:,.0f}")

outliers = inv[(inv["Amount_NPR"] < low) | (inv["Amount_NPR"] > high)]
print(f"\nOutlier rows: {len(outliers)}")
outliers[["Invoice_No", "Customer", "Amount_NPR"]].head()
"""))

C.append(md(r"""
### Practice 6
Use the IQR method on `Quantity` to find unusually high quantity invoices. Print their count and the rows.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
q = inv["Quantity"]
q1, q3 = q.quantile([0.25, 0.75])
iqr = q3 - q1
high = q3 + 1.5 * iqr
out = inv[inv["Quantity"] > high]
print("Outlier rows:", len(out))
out[["Invoice_No","Product","Quantity"]].head()
"""))
C.append(md(r"""</details>"""))

# Section 8
C.append(md(r"""
## 8. Renaming columns

Good column names = self-documenting analysis.
"""))

C.append(code(r"""
inv = inv.rename(columns={
    "Amount_NPR": "Amount",
    "VAT_NPR":    "VAT",
    "Total_NPR":  "Total",
})
inv.columns
"""))

# Mini Project
C.append(md(r"""
## 9. Mini-Project — Clean the messy invoice file end-to-end

Re-open `data/invoices_dirty.csv` and apply the **full cleaning pipeline**:

1. Load it into `df`.
2. Drop duplicate rows.
3. Fill missing `Amount_NPR` with the **median**.
4. Fill missing `City` with `"Unknown"`.
5. Clean `Customer` names → strip whitespace, Title case.
6. Convert `Date` column to real datetime.
7. Add a `Year` and `Month` column.
8. Flag any `Amount_NPR` outlier in a new column `Is_Outlier` (True/False) using the IQR method.
9. Save the cleaned file as `invoices_clean.csv`.

Print the **before/after row counts** and the **missing-value counts** after each major step.
"""))

C.append(code(r"""
# Your code here
df = pd.read_csv("data/invoices_dirty.csv")
print("Before:", df.shape)
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))

C.append(code(r"""
df = pd.read_csv("data/invoices_dirty.csv")
print("Loaded:", df.shape)

# 1. drop duplicates
df = df.drop_duplicates()
print("After dedup:", df.shape)

# 2. missing values
df["Amount_NPR"] = df["Amount_NPR"].fillna(df["Amount_NPR"].median())
df["City"]       = df["City"].fillna("Unknown")
print("Missing after fill:\n", df.isna().sum())

# 3. clean customer text
df["Customer"] = df["Customer"].str.strip().str.title()

# 4. dates
df["Date"]  = pd.to_datetime(df["Date"])
df["Year"]  = df["Date"].dt.year
df["Month"] = df["Date"].dt.month

# 5. outliers
q1, q3 = df["Amount_NPR"].quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
df["Is_Outlier"] = (df["Amount_NPR"] < low) | (df["Amount_NPR"] > high)

# 6. save
df.to_csv("invoices_clean.csv", index=False)
print("\nSaved invoices_clean.csv with shape:", df.shape)
print("Outliers flagged:", df["Is_Outlier"].sum())
"""))
C.append(md(r"""</details>"""))

C.append(md(r"""
---
### What's next?
With clean data in hand we can build new, useful columns from existing ones —
in `05_Feature_Engineering` we'll create ratios, date features, customer-level aggregates
and ready our data for machine-learning models.
"""))

save_notebook(C, Path(__file__).parent / "04_Data_Cleaning.ipynb")
