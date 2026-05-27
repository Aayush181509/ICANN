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


```python
import pandas as pd
import numpy as np

inv = pd.read_csv("data/invoices_dirty.csv")
print("Shape:", inv.shape)
inv.head()
```

    Shape: (206, 11)





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Date</th>
      <th>Customer</th>
      <th>City</th>
      <th>Product</th>
      <th>Quantity</th>
      <th>Unit_Price</th>
      <th>Amount_NPR</th>
      <th>VAT_NPR</th>
      <th>Total_NPR</th>
      <th>Payment_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>INV-20810001</td>
      <td>2024-07-16</td>
      <td>Janakpur Wholesale</td>
      <td>Birgunj</td>
      <td>Food</td>
      <td>39</td>
      <td>1219.0</td>
      <td>NaN</td>
      <td>6180.33</td>
      <td>53721.33</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>1</th>
      <td>INV-20810002</td>
      <td>2024-07-18</td>
      <td>Kathmandu Distributors</td>
      <td>Kathmandu</td>
      <td>Food</td>
      <td>27</td>
      <td>1418.0</td>
      <td>38286.0</td>
      <td>4977.18</td>
      <td>43263.18</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>2</th>
      <td>INV-20810003</td>
      <td>2024-07-20</td>
      <td>Biratnagar Enterprise</td>
      <td>Butwal</td>
      <td>Stationery</td>
      <td>10</td>
      <td>1309.0</td>
      <td>13090.0</td>
      <td>1701.70</td>
      <td>14791.70</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>3</th>
      <td>INV-20810004</td>
      <td>2024-07-22</td>
      <td>Pokhara Mart</td>
      <td>Birgunj</td>
      <td>Food</td>
      <td>26</td>
      <td>5501.0</td>
      <td>143026.0</td>
      <td>18593.38</td>
      <td>161619.38</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>4</th>
      <td>INV-20810005</td>
      <td>2024-07-24</td>
      <td>Janakpur Wholesale</td>
      <td>NaN</td>
      <td>Food</td>
      <td>19</td>
      <td>1669.0</td>
      <td>31711.0</td>
      <td>4122.43</td>
      <td>35833.43</td>
      <td>Paid</td>
    </tr>
  </tbody>
</table>
</div>



## 2. Spotting missing values


```python
# True wherever a cell is missing
inv.isna().head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Date</th>
      <th>Customer</th>
      <th>City</th>
      <th>Product</th>
      <th>Quantity</th>
      <th>Unit_Price</th>
      <th>Amount_NPR</th>
      <th>VAT_NPR</th>
      <th>Total_NPR</th>
      <th>Payment_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>4</th>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>True</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>




```python
# How many missing per column?
inv.isna().sum()
```




    Invoice_No         0
    Date               0
    Customer           0
    City               8
    Product            0
    Quantity           0
    Unit_Price         0
    Amount_NPR        13
    VAT_NPR            0
    Total_NPR          0
    Payment_Status     0
    dtype: int64



### Practice 1
Find how many missing values each column of `inv` has, and what % of rows are missing in `Amount_NPR`.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print(inv.isna().sum())
pct = inv["Amount_NPR"].isna().mean() * 100
print(f"\nMissing in Amount_NPR: {pct:.2f}%")
```

    Invoice_No         0
    Date               0
    Customer           0
    City               8
    Product            0
    Quantity           0
    Unit_Price         0
    Amount_NPR        13
    VAT_NPR            0
    Total_NPR          0
    Payment_Status     0
    dtype: int64
    
    Missing in Amount_NPR: 6.31%


</details>

## 3. Handling missing values

You have three common choices:

| Approach   | When to use                                                   |
|------------|----------------------------------------------------------------|
| Drop rows  | A handful of rows missing in a critical column                |
| Fill with 0 | Missing means "no value" (e.g. no discount applied)          |
| Fill with mean / median | Missing because of bad entry, but the row is otherwise valid |


```python
# Method 1 — drop any row that has a missing value
clean1 = inv.dropna()
print("Rows before:", len(inv), "→ after drop:", len(clean1))
```

    Rows before: 206 → after drop: 185



```python
# Method 2 — fill missing Amount_NPR with the median (more robust than mean)
clean2 = inv.copy()
median_amt = clean2["Amount_NPR"].median()
clean2["Amount_NPR"] = clean2["Amount_NPR"].fillna(median_amt)

# Fill missing City with the string "Unknown"
clean2["City"] = clean2["City"].fillna("Unknown")

print("Missing after fill:")
print(clean2.isna().sum())
```

    Missing after fill:
    Invoice_No        0
    Date              0
    Customer          0
    City              0
    Product           0
    Quantity          0
    Unit_Price        0
    Amount_NPR        0
    VAT_NPR           0
    Total_NPR         0
    Payment_Status    0
    dtype: int64


### Practice 2
Make a copy of `inv` called `inv2`. In `inv2`:

1. Fill missing `Amount_NPR` with the column's **mean**.
2. Fill missing `City` with the value `"Not Provided"`.
3. Confirm there are no missing values left.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
inv2 = inv.copy()
inv2["Amount_NPR"] = inv2["Amount_NPR"].fillna(inv2["Amount_NPR"].mean())
inv2["City"]       = inv2["City"].fillna("Not Provided")
print(inv2.isna().sum())
```

    Invoice_No        0
    Date              0
    Customer          0
    City              0
    Product           0
    Quantity          0
    Unit_Price        0
    Amount_NPR        0
    VAT_NPR           0
    Total_NPR         0
    Payment_Status    0
    dtype: int64


</details>

## 4. Removing duplicate rows

Duplicates can sneak in when invoices are re-uploaded or merged from two files.


```python
# Total duplicate rows
print("Duplicate rows:", inv.duplicated().sum())

# Drop them, keep the first occurrence
inv_dedup = inv.drop_duplicates()
print("After dedup    :", len(inv_dedup))
```

    Duplicate rows: 6
    After dedup    : 200



```python
# Often we only care about duplicates in a key column like Invoice_No
print("Duplicate Invoice_No:", inv.duplicated(subset=["Invoice_No"]).sum())
inv_unique_inv = inv.drop_duplicates(subset=["Invoice_No"])
print("After dedup by Invoice_No:", len(inv_unique_inv))
```

    Duplicate Invoice_No: 6
    After dedup by Invoice_No: 200


### Practice 3
1. How many rows in `inv` have a **duplicate `Invoice_No`**?
2. Keep only the **first** occurrence and store the result in `inv_clean`.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print("Duplicate Invoice_No:", inv.duplicated(subset=["Invoice_No"]).sum())
inv_clean = inv.drop_duplicates(subset=["Invoice_No"], keep="first")
print("Final rows:", len(inv_clean))
```

    Duplicate Invoice_No: 6
    Final rows: 200


</details>

## 5. Cleaning text columns

Text is the most common source of subtle bugs — `" Himalayan Traders "` and `"HIMALAYAN TRADERS"` look the same to us, but Pandas treats them as **different customers**.


```python
# Look — same customer, three different versions
print(inv["Customer"].value_counts().head(8))
```

    Customer
    Janakpur Wholesale       27
    Biratnagar Enterprise    22
    Himalayan Traders        22
    Pokhara Mart             20
    Annapurna Stores         20
    Nepalgunj Goods          20
    Birgunj Cargo            18
    Everest Suppliers        18
    Name: count, dtype: int64



```python
# Standard recipe: strip spaces + put in title-case
inv["Customer"] = inv["Customer"].str.strip().str.title()
print(inv["Customer"].value_counts().head(8))
```

    Customer
    Janakpur Wholesale       27
    Himalayan Traders        27
    Biratnagar Enterprise    22
    Everest Suppliers        21
    Pokhara Mart             20
    Annapurna Stores         20
    Nepalgunj Goods          20
    Birgunj Cargo            18
    Name: count, dtype: int64


### Practice 4
Notice that some `Customer` values are still capitalised differently (e.g. `"Everest Suppliers"` vs `"EVEREST SUPPLIERS"`). Confirm they are all consistent **now** using `.unique()`.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print(inv["Customer"].unique())
print("Distinct customers:", inv["Customer"].nunique())
```

    <StringArray>
    [    'Janakpur Wholesale', 'Kathmandu Distributors',  'Biratnagar Enterprise',
               'Pokhara Mart',          'Birgunj Cargo',       'Annapurna Stores',
            'Lumbini Imports',      'Everest Suppliers',      'Himalayan Traders',
            'Nepalgunj Goods']
    Length: 10, dtype: str
    Distinct customers: 10


</details>

## 6. Fixing data types

A common headache: **numbers that came in as text**, or **dates that are just strings**.


```python
print(inv.dtypes)
```

    Invoice_No            str
    Date                  str
    Customer              str
    City                  str
    Product               str
    Quantity            int64
    Unit_Price        float64
    Amount_NPR        float64
    VAT_NPR           float64
    Total_NPR         float64
    Payment_Status        str
    dtype: object



```python
# Convert Date column from string → real datetime
inv["Date"] = pd.to_datetime(inv["Date"])

# Now we can extract year, month, weekday, etc.
inv["Year"]    = inv["Date"].dt.year
inv["Month"]   = inv["Date"].dt.month
inv["Weekday"] = inv["Date"].dt.day_name()

inv[["Date", "Year", "Month", "Weekday"]].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Year</th>
      <th>Month</th>
      <th>Weekday</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2024-07-16</td>
      <td>2024</td>
      <td>7</td>
      <td>Tuesday</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2024-07-18</td>
      <td>2024</td>
      <td>7</td>
      <td>Thursday</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2024-07-20</td>
      <td>2024</td>
      <td>7</td>
      <td>Saturday</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2024-07-22</td>
      <td>2024</td>
      <td>7</td>
      <td>Monday</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2024-07-24</td>
      <td>2024</td>
      <td>7</td>
      <td>Wednesday</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 5
Suppose someone gives you this Series of amounts where the values are stored as **strings with commas**:
`["1,250", "3,400", "12,800", "5,000"]`

Convert it into a real numeric Series and find the total.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
s = pd.Series(["1,250", "3,400", "12,800", "5,000"])
nums = s.str.replace(",", "").astype(int)
print(nums)
print("Total:", nums.sum())
```

    0     1250
    1     3400
    2    12800
    3     5000
    dtype: int64
    Total: 22450


</details>

## 7. Detecting outliers — the IQR method

The **IQR (Inter-Quartile Range) method** is a standard, safe way to flag suspicious values:

1. `Q1` = 25th percentile.
2. `Q3` = 75th percentile.
3. `IQR = Q3 − Q1`.
4. Anything below `Q1 − 1.5·IQR` or above `Q3 + 1.5·IQR` is considered an **outlier**.


```python
amt = inv["Amount_NPR"].dropna()

q1, q3 = amt.quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr

print(f"Q1 = {q1:,.0f}   Q3 = {q3:,.0f}   IQR = {iqr:,.0f}")
print(f"Acceptable range: {low:,.0f}  →  {high:,.0f}")

outliers = inv[(inv["Amount_NPR"] < low) | (inv["Amount_NPR"] > high)]
print(f"\nOutlier rows: {len(outliers)}")
outliers[["Invoice_No", "Customer", "Amount_NPR"]].head()
```

    Q1 = 33,024   Q3 = 138,120   IQR = 105,096
    Acceptable range: -124,620  →  295,764
    
    Outlier rows: 7





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Customer</th>
      <th>Amount_NPR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>27</th>
      <td>INV-20810028</td>
      <td>Annapurna Stores</td>
      <td>352755.0</td>
    </tr>
    <tr>
      <th>39</th>
      <td>INV-20810040</td>
      <td>Everest Suppliers</td>
      <td>300377.0</td>
    </tr>
    <tr>
      <th>96</th>
      <td>INV-20810097</td>
      <td>Nepalgunj Goods</td>
      <td>387590.0</td>
    </tr>
    <tr>
      <th>132</th>
      <td>INV-20810133</td>
      <td>Annapurna Stores</td>
      <td>359325.0</td>
    </tr>
    <tr>
      <th>149</th>
      <td>INV-20810150</td>
      <td>Nepalgunj Goods</td>
      <td>306636.0</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 6
Use the IQR method on `Quantity` to find unusually high quantity invoices. Print their count and the rows.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
q = inv["Quantity"]
q1, q3 = q.quantile([0.25, 0.75])
iqr = q3 - q1
high = q3 + 1.5 * iqr
out = inv[inv["Quantity"] > high]
print("Outlier rows:", len(out))
out[["Invoice_No","Product","Quantity"]].head()
```

    Outlier rows: 0





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Product</th>
      <th>Quantity</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



</details>

## 8. Renaming columns

Good column names = self-documenting analysis.


```python
inv = inv.rename(columns={
    "Amount_NPR": "Amount",
    "VAT_NPR":    "VAT",
    "Total_NPR":  "Total",
})
inv.columns
```




    Index(['Invoice_No', 'Date', 'Customer', 'City', 'Product', 'Quantity',
           'Unit_Price', 'Amount', 'VAT', 'Total', 'Payment_Status', 'Year',
           'Month', 'Weekday'],
          dtype='str')



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


```python
# Your code here
df = pd.read_csv("data/invoices_dirty.csv")
print("Before:", df.shape)
```

    Before: (206, 11)


<details><summary>Show solution</summary>


```python
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
```

    Loaded: (206, 11)
    After dedup: (200, 11)
    Missing after fill:
     Invoice_No        0
    Date              0
    Customer          0
    City              0
    Product           0
    Quantity          0
    Unit_Price        0
    Amount_NPR        0
    VAT_NPR           0
    Total_NPR         0
    Payment_Status    0
    dtype: int64
    
    Saved invoices_clean.csv with shape: (200, 14)
    Outliers flagged: 11


</details>

---
### What's next?
With clean data in hand we can build new, useful columns from existing ones —
in `05_Feature_Engineering` we'll create ratios, date features, customer-level aggregates
and ready our data for machine-learning models.
