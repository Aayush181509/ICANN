"""Build session/02_Pandas_Basics.ipynb"""
from pathlib import Path
from _nb_helper import md, code, save_notebook

C = []

C.append(md(r"""
# Notebook 2 — Pandas Basics for CA Professionals

**Goal:** Work with real Excel-style data in Python using Pandas.

**You will learn:**
1. What Pandas is and how it relates to Excel
2. Series and DataFrame — the two main objects
3. Loading a CSV file and looking at it
4. Selecting columns and filtering rows
5. Adding new calculated columns (like a new Excel column)
6. Sorting data
7. GroupBy — like a Pivot Table
8. Saving your results back to Excel/CSV
9. A short mini-project at the end

> Throughout the notebook we will use Nepali invoice, sales and payroll data placed in the `data/` folder beside this notebook.

---
"""))

# ---- Section 1 ----
C.append(md(r"""
## 1. What is Pandas?

Pandas is a Python library that gives you a **DataFrame** — basically an Excel sheet inside Python.

| Excel             | Pandas        |
|-------------------|---------------|
| Workbook          | (your script) |
| Worksheet         | `DataFrame`   |
| Column            | `Series`      |
| Cell              | one value     |
| Pivot Table       | `groupby()`   |
| AutoFilter        | boolean mask  |
"""))

C.append(code(r"""
import pandas as pd
import numpy as np
print("Pandas version:", pd.__version__)
"""))

# ---- Section 2: Series ----
C.append(md(r"""
## 2. A Series — one column of data

A `Series` is a single column with a **label** for each row (the **index**).
"""))

C.append(code(r"""
monthly = pd.Series(
    data=[1250000, 1380000, 1120000, 1450000, 1620000],
    index=["Shrawan", "Bhadra", "Ashwin", "Kartik", "Mangsir"],
    name="Revenue_NPR",
)
print(monthly)
print()
print("Total :", monthly.sum())
print("Mean  :", monthly.mean())
"""))

C.append(md(r"""
### Practice 1
Create a Series called `expenses` for these 5 months:
- Shrawan: 920000, Bhadra: 980000, Ashwin: 870000, Kartik: 1050000, Mangsir: 1180000

Then print the **total** and the **highest** expense.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
expenses = pd.Series(
    [920000, 980000, 870000, 1050000, 1180000],
    index=["Shrawan","Bhadra","Ashwin","Kartik","Mangsir"],
    name="Expense_NPR",
)
print(expenses)
print("Total :", expenses.sum())
print("Max   :", expenses.max())
"""))
C.append(md(r"""</details>"""))

# ---- Section 3: DataFrame ----
C.append(md(r"""
## 3. A DataFrame — the full table

A `DataFrame` is several Series joined together. Each column has a name; each row has an index.
"""))

C.append(code(r"""
df = pd.DataFrame({
    "Month":   ["Shrawan", "Bhadra", "Ashwin", "Kartik", "Mangsir"],
    "Revenue": [1250000, 1380000, 1120000, 1450000, 1620000],
    "Expense": [ 920000,  980000,  870000, 1050000, 1180000],
})
df
"""))

C.append(md(r"""
### Practice 2
Create a small DataFrame with 4 employees of your choice. Columns:
`Name`, `Department`, `Salary`. Print the DataFrame.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
staff = pd.DataFrame({
    "Name":       ["Ramesh", "Sita", "Hari", "Anita"],
    "Department": ["Audit", "Tax", "Audit", "Advisory"],
    "Salary":     [55000, 72000, 48000, 95000],
})
print(staff)
"""))
C.append(md(r"""</details>"""))

# ---- Section 4: Reading CSV ----
C.append(md(r"""
## 4. Loading data from a CSV file

In real life you don't type the data — you read it from a file. We have a folder called `data/` with several Nepali financial datasets already prepared.
"""))

C.append(code(r"""
invoices = pd.read_csv("data/invoices.csv")
invoices.head()        # show first 5 rows
"""))

C.append(md(r"""
### Practice 3
Load the file `data/monthly_sales.csv` into a DataFrame called `sales` and show the first 5 rows.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
sales = pd.read_csv("data/monthly_sales.csv")
sales.head()
"""))
C.append(md(r"""</details>"""))

# ---- Section 5: Inspecting ----
C.append(md(r"""
## 5. Quick inspection — get to know your data

| Code              | What it does                            |
|-------------------|-----------------------------------------|
| `df.head(n)`      | first n rows                            |
| `df.tail(n)`      | last n rows                             |
| `df.shape`        | (rows, columns)                         |
| `df.columns`      | column names                            |
| `df.dtypes`       | data type of each column                |
| `df.info()`       | full overview                           |
| `df.describe()`   | quick statistics for numeric columns    |
"""))

C.append(code(r"""
print("Shape   :", invoices.shape)
print("Columns :", list(invoices.columns))
print()
invoices.info()
"""))

C.append(code(r"""
invoices.describe()    # statistics for all numeric columns
"""))

C.append(md(r"""
### Practice 4
Load `data/loans.csv` into a DataFrame called `loans`. Then:

1. Print its **shape**.
2. Show its **column names**.
3. Show `describe()` for the numeric columns.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
loans = pd.read_csv("data/loans.csv")
print("Shape   :", loans.shape)
print("Columns :", list(loans.columns))
loans.describe()
"""))
C.append(md(r"""</details>"""))

# ---- Section 6: Selecting columns ----
C.append(md(r"""
## 6. Selecting columns

You can pick a single column (gives a Series), or several columns (gives a DataFrame).
"""))

C.append(code(r"""
# Single column → Series
invoices["Amount_NPR"].head()
"""))

C.append(code(r"""
# Several columns → DataFrame
invoices[["Customer", "City", "Total_NPR"]].head()
"""))

C.append(md(r"""
### Practice 5
From `invoices`, show only the columns `Invoice_No`, `Product`, `Quantity`, `Amount_NPR` — first 10 rows.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
invoices[["Invoice_No","Product","Quantity","Amount_NPR"]].head(10)
"""))
C.append(md(r"""</details>"""))

# ---- Section 7: Filtering rows ----
C.append(md(r"""
## 7. Filtering rows — the AutoFilter of Pandas

Just like `np.array[condition]`, but on a whole table.
"""))

C.append(code(r"""
# Invoices with amount over NPR 1 lakh
big = invoices[invoices["Amount_NPR"] > 100000]
print("Found", len(big), "high-value invoices")
big.head()
"""))

C.append(code(r"""
# Combine conditions with & (and) and | (or) — wrap each in ()
overdue_big = invoices[(invoices["Payment_Status"] == "Overdue") &
                       (invoices["Amount_NPR"] > 50000)]
overdue_big.head()
"""))

C.append(md(r"""
### Practice 6
From `invoices`:

1. Find all invoices from the city **"Kathmandu"**.
2. Find all **"Pending"** invoices above NPR 30,000.
3. Count how many invoices have `Quantity` > 30.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
ktm = invoices[invoices["City"] == "Kathmandu"]
pending = invoices[(invoices["Payment_Status"] == "Pending") &
                   (invoices["Amount_NPR"] > 30000)]
print("KTM invoices    :", len(ktm))
print("Pending > 30K   :", len(pending))
print("Qty > 30 count  :", (invoices["Quantity"] > 30).sum())
"""))
C.append(md(r"""</details>"""))

# ---- Section 8: Sorting ----
C.append(md(r"""
## 8. Sorting

`sort_values(by="ColumnName")` is your friend — just like Data → Sort in Excel.
"""))

C.append(code(r"""
# Top 5 highest invoices
top5 = invoices.sort_values("Total_NPR", ascending=False).head(5)
top5[["Invoice_No","Customer","Total_NPR","Payment_Status"]]
"""))

C.append(md(r"""
### Practice 7
Sort `invoices` by `Quantity` (largest first) and show the top 10.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
invoices.sort_values("Quantity", ascending=False).head(10)
"""))
C.append(md(r"""</details>"""))

# ---- Section 9: New columns ----
C.append(md(r"""
## 9. Creating new columns

You can build new columns from existing ones — like adding a new column with an Excel formula.
"""))

C.append(code(r"""
sales = pd.read_csv("data/monthly_sales.csv")

# New calculated columns
sales["Profit"]      = sales["Revenue_NPR"] - sales["Expense_NPR"]
sales["Margin_pct"]  = (sales["Profit"] / sales["Revenue_NPR"] * 100).round(2)
sales["VAT_NPR"]     = sales["Revenue_NPR"] * 0.13

sales
"""))

C.append(md(r"""
### Practice 8
Load `data/payroll.csv` into `pay`. Add a new column `Annual_Net` = `Net_Salary` × 12. Then sort by `Annual_Net` (descending) and show the top 5 employees.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
pay = pd.read_csv("data/payroll.csv")
pay["Annual_Net"] = pay["Net_Salary"] * 12
pay.sort_values("Annual_Net", ascending=False).head(5)
"""))
C.append(md(r"""</details>"""))

# ---- Section 10: groupby ----
C.append(md(r"""
## 10. GroupBy — the Pandas Pivot Table

`groupby()` is the most powerful feature you'll use. It splits data into groups, applies a function to each group, and combines the result. Exactly like a Pivot Table.
"""))

C.append(code(r"""
# Total invoice amount per city
invoices.groupby("City")["Total_NPR"].sum().sort_values(ascending=False)
"""))

C.append(code(r"""
# Multiple metrics at once
invoices.groupby("Payment_Status").agg(
    Count        = ("Invoice_No", "count"),
    Total_Amount = ("Total_NPR", "sum"),
    Avg_Amount   = ("Total_NPR", "mean"),
).round(0)
"""))

C.append(md(r"""
### Practice 9
Using `invoices`:

1. Find the **total Amount_NPR per Product**.
2. Find the **average Quantity per Customer**.
3. Count how many invoices each `City` has.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
print(invoices.groupby("Product")["Amount_NPR"].sum())
print()
print(invoices.groupby("Customer")["Quantity"].mean().round(1))
print()
print(invoices.groupby("City").size())
"""))
C.append(md(r"""</details>"""))

# ---- Section 11: Save ----
C.append(md(r"""
## 11. Saving your work to a file

Once you have cleaned / processed data, you can save the result.
"""))

C.append(code(r"""
top5 = invoices.sort_values("Total_NPR", ascending=False).head(5)

top5.to_csv("top5_invoices.csv", index=False)   # save as CSV
# top5.to_excel("top5_invoices.xlsx", index=False)   # needs openpyxl

print("Saved top5_invoices.csv")
"""))

# ---- Mini Project ----
C.append(md(r"""
## 12. Mini-Project — Sales Analysis

Using `data/invoices.csv`, answer the following:

1. **Which city has the highest total sales?**
2. **Which product is sold the most (by quantity)?**
3. **What % of invoices are still pending or overdue?**
4. **List the top 3 customers by total revenue.**
5. **Find the average invoice amount city-wise.**
"""))

C.append(code(r"""
inv = pd.read_csv("data/invoices.csv")

# Your code here
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))

C.append(code(r"""
# 1
print("Top city by sales:")
print(inv.groupby("City")["Total_NPR"].sum().sort_values(ascending=False).head(1))
print()

# 2
print("Top product by qty:")
print(inv.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(1))
print()

# 3
pending_or_over = inv[inv["Payment_Status"] != "Paid"]
print(f"Pending+Overdue: {len(pending_or_over)/len(inv)*100:.1f}%")
print()

# 4
print("Top 3 customers:")
print(inv.groupby("Customer")["Total_NPR"].sum().sort_values(ascending=False).head(3))
print()

# 5
print("Average invoice per city:")
print(inv.groupby("City")["Total_NPR"].mean().round(0).sort_values(ascending=False))
"""))
C.append(md(r"""</details>"""))

C.append(md(r"""
---
### What's next?
Pandas is now your everyday tool for working with tabular data.
In the next notebook (`03_Matplotlib_Seaborn`) we will turn this data into **charts** — line graphs, bar charts, heatmaps — so we can present it to clients and partners.
"""))

save_notebook(C, Path(__file__).parent / "02_Pandas_Basics.ipynb")
