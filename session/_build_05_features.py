"""Build session/05_Feature_Engineering.ipynb"""
from pathlib import Path
from _nb_helper import md, code, save_notebook

C = []

C.append(md(r"""
# Notebook 5 — Feature Engineering for CA Professionals

**Goal:** Create new, useful columns ("features") from existing data — so that charts, dashboards and machine learning models can give better answers.

**You will learn:**
1. What is a "feature" and why we create new ones
2. Math features — ratios, growth rates, age
3. Date features — month, weekday, festival flag
4. Binning — turning numbers into buckets (e.g. invoice size: Small/Medium/Large)
5. Encoding categorical columns into numbers
6. Scaling numeric columns
7. Aggregated features — per-customer summaries
8. A short mini-project

---
"""))

# Section 1
C.append(md(r"""
## 1. What is "feature engineering"?

A **feature** is just a column in your dataset. *Feature engineering* means **creating new columns** that make the underlying signal more obvious.

A CA-style example:

| Existing columns                            | New (engineered) feature           |
|---------------------------------------------|------------------------------------|
| `Revenue`, `Expense`                        | `Profit_Margin = (R-E)/R`          |
| `Loan_Amount`, `Annual_Income`              | `Loan_to_Income_Ratio`             |
| `Invoice_Date`, `Today`                     | `Days_Outstanding`                 |
| `Amount`                                    | `Size_Bucket = Small / Medium / Large`|
| `City`                                      | encoded numbers (for ML)           |

Better features → better insights → better models.
"""))

C.append(code(r"""
import pandas as pd
import numpy as np
print("ready")
"""))

# Section 2: math features
C.append(md(r"""
## 2. Math features — ratios and percentages
"""))

C.append(code(r"""
sales = pd.read_csv("data/monthly_sales.csv")

sales["Profit"]        = sales["Revenue_NPR"] - sales["Expense_NPR"]
sales["Profit_Margin"] = (sales["Profit"] / sales["Revenue_NPR"] * 100).round(2)
sales["Expense_Ratio"] = (sales["Expense_NPR"] / sales["Revenue_NPR"] * 100).round(2)
sales["Avg_Price"]     = (sales["Revenue_NPR"] / sales["Units_Sold"]).round(0)

sales.head()
"""))

C.append(md(r"""
### Practice 1
Load `data/loans.csv` and create a new feature **`Loan_to_Income`** = `Loan_Amount` ÷ `Annual_Income`. Print the first 5 rows of `Loan_ID`, `Loan_Amount`, `Annual_Income`, `Loan_to_Income`.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
loans = pd.read_csv("data/loans.csv")
loans["Loan_to_Income"] = (loans["Loan_Amount"] / loans["Annual_Income"]).round(2)
loans[["Loan_ID","Loan_Amount","Annual_Income","Loan_to_Income"]].head()
"""))
C.append(md(r"""</details>"""))

# Section 3: Growth rate
C.append(md(r"""
## 3. Growth / change features

`pct_change()` calculates row-over-row % change — handy for month-over-month growth.
"""))

C.append(code(r"""
sales["MoM_Growth_%"] = (sales["Revenue_NPR"].pct_change() * 100).round(2)
sales[["Month","Revenue_NPR","MoM_Growth_%"]]
"""))

C.append(md(r"""
### Practice 2
Compute the month-over-month % change of `Units_Sold` in the `sales` DataFrame.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
sales["Units_Growth_%"] = (sales["Units_Sold"].pct_change() * 100).round(2)
sales[["Month","Units_Sold","Units_Growth_%"]]
"""))
C.append(md(r"""</details>"""))

# Section 4: date features
C.append(md(r"""
## 4. Date features

Most date columns hide useful information: month, day of week, weekend or not, quarter, year-end indicator. Once parsed, you can extract any of these.
"""))

C.append(code(r"""
inv = pd.read_csv("data/invoices.csv")
inv["Date"] = pd.to_datetime(inv["Date"])

inv["Year"]       = inv["Date"].dt.year
inv["Month"]      = inv["Date"].dt.month
inv["Quarter"]    = inv["Date"].dt.quarter
inv["Weekday"]    = inv["Date"].dt.day_name()
inv["Is_Weekend"] = inv["Date"].dt.weekday >= 5

# Days outstanding — assuming today is 2025-04-01
today = pd.Timestamp("2025-04-01")
inv["Days_Old"] = (today - inv["Date"]).dt.days

inv[["Date","Year","Month","Quarter","Weekday","Is_Weekend","Days_Old"]].head()
"""))

C.append(md(r"""
### Practice 3
Load `data/customers.csv` and use the `Onboarded_Date` column to compute, for each customer, **how many days they've been a customer** (use `pd.Timestamp("2025-04-01")` as "today").
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
cust = pd.read_csv("data/customers.csv")
cust["Onboarded_Date"] = pd.to_datetime(cust["Onboarded_Date"])
cust["Customer_Age_Days"] = (pd.Timestamp("2025-04-01") - cust["Onboarded_Date"]).dt.days
cust[["Customer_ID","Onboarded_Date","Customer_Age_Days"]].head()
"""))
C.append(md(r"""</details>"""))

# Section 5: binning
C.append(md(r"""
## 5. Binning — turning numbers into categories

Sometimes a category is more useful than the raw number. For example, we might want every invoice classified as **Small / Medium / Large**.

`pd.cut()` does this for you.
"""))

C.append(code(r"""
bins   = [0, 50000, 200000, np.inf]            # the cut-points
labels = ["Small", "Medium", "Large"]

inv["Size_Bucket"] = pd.cut(inv["Amount_NPR"], bins=bins, labels=labels)
inv["Size_Bucket"].value_counts()
"""))

C.append(md(r"""
### Practice 4
Bin the `Credit_Score` column in `loans` into 3 buckets:

| Range            | Label    |
|------------------|----------|
| 300 – 580        | Poor     |
| 581 – 720        | Fair     |
| 721 – 850        | Good     |

Then count how many loans fall in each bucket.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
loans["Score_Bucket"] = pd.cut(loans["Credit_Score"],
                                bins=[299, 580, 720, 850],
                                labels=["Poor","Fair","Good"])
print(loans["Score_Bucket"].value_counts())
"""))
C.append(md(r"""</details>"""))

# Section 6: encoding
C.append(md(r"""
## 6. Encoding categorical columns into numbers

Machine learning models only understand **numbers**. So a column like `Payment_Status = "Paid" / "Pending" / "Overdue"` must be converted.

Two common methods:

| Method            | When to use                                      |
|-------------------|--------------------------------------------------|
| `map()`           | A small fixed list (e.g. Yes/No, M/F)           |
| `pd.get_dummies()`| Many unordered categories (one column per value)|
"""))

C.append(code(r"""
# Method 1 — simple mapping
status_map = {"Paid": 0, "Pending": 1, "Overdue": 2}
inv["Status_Code"] = inv["Payment_Status"].map(status_map)
inv[["Payment_Status","Status_Code"]].head()
"""))

C.append(code(r"""
# Method 2 — one-hot encoding (good for unordered categories)
city_dummies = pd.get_dummies(inv["City"], prefix="City").astype(int)
city_dummies.head()
"""))

C.append(md(r"""
### Practice 5
In the `loans` DataFrame:

1. Map `Has_Collateral` to numbers: `"Yes"` → 1, `"No"` → 0. Store as `Has_Coll_Code`.
2. One-hot encode the `Sector` column with prefix `"Sec"` and show the first 5 rows.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
loans["Has_Coll_Code"] = loans["Has_Collateral"].map({"Yes": 1, "No": 0})
sec = pd.get_dummies(loans["Sector"], prefix="Sec").astype(int)
print(loans[["Has_Collateral","Has_Coll_Code"]].head())
sec.head()
"""))
C.append(md(r"""</details>"""))

# Section 7: scaling
C.append(md(r"""
## 7. Scaling numeric columns

When one column is in *lakhs* and another in *percentage points*, models can get confused by the difference in magnitude.

The fix is to **scale** all numeric columns to a similar range.

| Scaler             | Output range          |
|--------------------|-----------------------|
| **Min-Max**        | 0 to 1                |
| **Standard (Z-score)** | mean 0, std 1     |
"""))

C.append(code(r"""
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Pick the numeric columns we want to scale
num_cols = ["Loan_Amount", "Annual_Income", "Credit_Score"]

mm = MinMaxScaler()
loans_mm = pd.DataFrame(mm.fit_transform(loans[num_cols]),
                        columns=[c+"_mm" for c in num_cols])

sd = StandardScaler()
loans_sd = pd.DataFrame(sd.fit_transform(loans[num_cols]),
                        columns=[c+"_z" for c in num_cols])

pd.concat([loans[num_cols].head(),
           loans_mm.head(),
           loans_sd.head().round(2)], axis=1)
"""))

# Section 8: aggregated features
C.append(md(r"""
## 8. Aggregated features — per-customer summaries

Sometimes the right "feature" lives at a higher level. For example: instead of looking at each invoice, build a row per customer summarising their entire behaviour.
"""))

C.append(code(r"""
cust_feat = inv.groupby("Customer").agg(
    Total_Invoices = ("Invoice_No",  "count"),
    Total_Amount   = ("Amount_NPR",  "sum"),
    Avg_Amount     = ("Amount_NPR",  "mean"),
    Max_Amount     = ("Amount_NPR",  "max"),
    Pending_Count  = ("Payment_Status", lambda s: (s != "Paid").sum()),
).round(0)

cust_feat["Pending_Ratio"] = (cust_feat["Pending_Count"] /
                              cust_feat["Total_Invoices"]).round(2)
cust_feat.head()
"""))

C.append(md(r"""
### Practice 6
Build a per-**City** summary from `inv` containing: `Total_Invoices`, `Total_Amount`, `Avg_Amount`. Sort by `Total_Amount` (largest first).
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
city_feat = inv.groupby("City").agg(
    Total_Invoices = ("Invoice_No","count"),
    Total_Amount   = ("Amount_NPR","sum"),
    Avg_Amount     = ("Amount_NPR","mean"),
).round(0).sort_values("Total_Amount", ascending=False)
city_feat
"""))
C.append(md(r"""</details>"""))

# Mini project
C.append(md(r"""
## 9. Mini-Project — Customer Feature Set

Goal: prepare a **per-customer feature table** ready for the regression / classification notebooks.

Steps:
1. Load `data/invoices.csv` and parse the `Date` column.
2. For each customer build these features:
   - `Total_Invoices`
   - `Total_Amount`
   - `Avg_Amount`
   - `First_Invoice_Date`
   - `Last_Invoice_Date`
   - `Days_Active` = `Last - First` in days
   - `Pending_Ratio` (share of invoices not paid)
3. Bin `Total_Amount` into Small / Medium / Large buckets (decide your own cut-points).
4. Save the result as `customer_features.csv`.
"""))

C.append(code(r"""
df = pd.read_csv("data/invoices.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Your code here
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))

C.append(code(r"""
df = pd.read_csv("data/invoices.csv")
df["Date"] = pd.to_datetime(df["Date"])

cf = df.groupby("Customer").agg(
    Total_Invoices = ("Invoice_No","count"),
    Total_Amount   = ("Amount_NPR","sum"),
    Avg_Amount     = ("Amount_NPR","mean"),
    First_Invoice  = ("Date","min"),
    Last_Invoice   = ("Date","max"),
    Pending_Cnt    = ("Payment_Status", lambda s: (s != "Paid").sum()),
).round(0)

cf["Days_Active"]   = (cf["Last_Invoice"] - cf["First_Invoice"]).dt.days
cf["Pending_Ratio"] = (cf["Pending_Cnt"] / cf["Total_Invoices"]).round(2)
cf["Customer_Size"] = pd.cut(cf["Total_Amount"],
                              bins=[0, 1_000_000, 5_000_000, np.inf],
                              labels=["Small","Medium","Large"])

cf.to_csv("customer_features.csv")
cf.head()
"""))
C.append(md(r"""</details>"""))

C.append(md(r"""
---
### What's next?
You now know how to **shape** raw data into model-ready features.
In `06_Regression` we will use these features to **predict numbers** (like next month's revenue),
and in `07_Classification` we will **predict categories** (like loan default).
"""))

save_notebook(C, Path(__file__).parent / "05_Feature_Engineering.ipynb")
