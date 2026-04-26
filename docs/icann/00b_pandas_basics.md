# Foundation 2: Pandas — From Zero to Confident
### Data Science for Chartered Accountants — Pre-Module

---

## What is this notebook about?

**Pandas** is the most important library for data analysis in Python. Think of it as a smarter, programmable Excel — but capable of handling millions of rows in seconds.

This notebook assumes:
- ✅ You know basic Python (variables, lists, dicts)
- ✅ You've done `00a_numpy_basics.ipynb` OR have basic NumPy awareness
- ❌ No prior Pandas knowledge required

## What will you learn?
1. Series — the 1D building block
2. DataFrame — the 2D table (like a spreadsheet)
3. Viewing and exploring data
4. Selecting rows and columns
5. Boolean filtering
6. Adding and modifying columns
7. Sorting
8. Handling missing values
9. Aggregation and GroupBy
10. Merging DataFrames (VLOOKUP equivalent)
11. Reading & writing files

---

> **If NumPy is a column of numbers, Pandas is the entire spreadsheet — with column names, row labels, and built-in analysis tools.**

---
## Section 1: Series — Pandas' 1D Data Structure


```python
import pandas as pd
import numpy as np

# ── A Series is like a NumPy array + labels (index) ───────────────────────────
monthly_revenue = pd.Series(
    data  = [80, 92, 75, 110, 105, 98, 120, 115, 130, 95, 108, 140],
    index = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
              'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],
    name  = 'Revenue (₹ Lakhs)'
)

print(monthly_revenue)
print('\nData type  :', monthly_revenue.dtype)
print('Index      :', list(monthly_revenue.index))
print('Name       :', monthly_revenue.name)
```


```python
# ── Accessing Series elements ─────────────────────────────────────────────────
print('April revenue  :', monthly_revenue['Apr'])      # by label
print('First month    :', monthly_revenue.iloc[0])     # by position
print('Q1 (Apr-Jun)   :\n', monthly_revenue.iloc[0:3])

# Series arithmetic
print('\nRevenue × 1.18 (inc. GST):\n', (monthly_revenue * 1.18).round(2))

# Statistics on a Series
print('\nStats:')
print(monthly_revenue.describe().round(2))
```

---
## Section 2: DataFrame — The 2D Table


```python
# ── Creating a DataFrame from a dict ─────────────────────────────────────────
# Each key becomes a column name; each list becomes the column's data

employees = pd.DataFrame({
    'emp_id'    : ['E001', 'E002', 'E003', 'E004', 'E005', 'E006'],
    'name'      : ['Rajesh Kumar', 'Priya Sharma', 'Amit Verma',
                   'Sunita Joshi', 'Vikram Nair', 'Pooja Mehta'],
    'department': ['Accounts', 'Audit', 'Tax', 'Accounts', 'Audit', 'Tax'],
    'grade'     : ['M', 'A', 'M', 'S', 'A', 'S'],
    'salary'    : [65000, 45000, 72000, 55000, 48000, 60000],
    'joining_yr': [2018, 2021, 2016, 2019, 2022, 2020],
})

print(employees)
```


```python
# ── Creating from a list of dicts ──────────────────────────────────────────────
# Each dict is one row
ledger = pd.DataFrame([
    {'date': '2024-04-01', 'head': 'Sales',       'dr': 0,      'cr': 5_00_000},
    {'date': '2024-04-02', 'head': 'Purchase',    'dr': 2_00_000,'cr': 0      },
    {'date': '2024-04-03', 'head': 'Bank',        'dr': 5_00_000,'cr': 0      },
    {'date': '2024-04-04', 'head': 'Cash',        'dr': 0,      'cr': 15_000  },
    {'date': '2024-04-05', 'head': 'Salary Exp',  'dr': 85_000, 'cr': 0      },
])
print(ledger)
```

---
## Section 3: Exploring a DataFrame


```python
# First look at any DataFrame
print('Shape:', employees.shape)           # (rows, columns)
print('\nColumn names:', employees.columns.tolist())
print('\nData types:')
print(employees.dtypes)
print('\nIndex:', employees.index.tolist())
```


```python
# Quick peek methods
print('First 3 rows:')
print(employees.head(3))

print('\nLast 2 rows:')
print(employees.tail(2))
```


```python
# .info() — types, missing values, memory
employees.info()
```


```python
# .describe() — statistical summary (numeric columns)
employees.describe()
```

---
## Section 4: Selecting Columns and Rows


```python
# ── Select a single column → returns a Series ─────────────────────────────────
salaries = employees['salary']
print(type(salaries))          # pd.Series
print(salaries)

print('\nAverage salary:', salaries.mean())
```


```python
# ── Select multiple columns → returns a DataFrame ────────────────────────────
subset = employees[['name', 'department', 'salary']]
print(type(subset))            # pd.DataFrame
print(subset)
```


```python
# ── .loc[]: label-based row selection ─────────────────────────────────────────
# format: df.loc[row_label_or_condition, column_name_or_list]

print('Row at index 2:')
print(employees.loc[2])

print('\nRows 1 to 3, columns name & salary:')
print(employees.loc[1:3, ['name', 'salary']])
```


```python
# ── .iloc[]: integer-position based ───────────────────────────────────────────
# Useful when you don't know the labels, just the position

print('First row (position 0):')
print(employees.iloc[0])

print('\nRows 0-2, first 3 columns:')
print(employees.iloc[0:3, 0:3])

print('\nLast 2 rows, last 2 columns:')
print(employees.iloc[-2:, -2:])
```

---
## Section 5: Boolean Filtering


```python
# ── Filter rows by condition ───────────────────────────────────────────────────
# Step 1: condition creates a boolean Series
high_earners_mask = employees['salary'] > 60000
print('Mask:')
print(high_earners_mask)

# Step 2: apply mask to DataFrame
high_earners = employees[high_earners_mask]
print('\nHigh earners (>60,000):')
print(high_earners[['name', 'department', 'salary']])
```


```python
# ── Filter by text ────────────────────────────────────────────────────────────
audit_team = employees[employees['department'] == 'Audit']
print('Audit team:')
print(audit_team[['name', 'grade', 'salary']])

# Filter for multiple values using .isin()
senior_grades = employees[employees['grade'].isin(['M', 'S'])]
print('\nManager + Senior grade employees:')
print(senior_grades[['name', 'grade', 'salary']])
```


```python
# ── Combining conditions ───────────────────────────────────────────────────────
# Use & (AND), | (OR), ~ (NOT) with parentheses around each condition

# Accounts dept AND salary > 55000
result = employees[(employees['department'] == 'Accounts') & (employees['salary'] > 55000)]
print('Accounts dept, salary > 55K:')
print(result[['name', 'department', 'salary']])

# NOT in Audit
non_audit = employees[~(employees['department'] == 'Audit')]
print('\nNon-Audit employees:')
print(non_audit[['name', 'department']])
```

---
## Section 6: Adding and Modifying Columns


```python
df = employees.copy()   # always work on a copy so original is safe

# ── Add a computed column ─────────────────────────────────────────────────────
df['annual_ctc'] = df['salary'] * 12
df['pf_deduction'] = df['salary'] * 0.12          # PF = 12% of salary
df['net_salary']   = df['salary'] - df['pf_deduction']
df['years_exp']    = 2024 - df['joining_yr']

print(df[['name', 'salary', 'pf_deduction', 'net_salary', 'years_exp']])
```


```python
# ── Conditional column using np.where ─────────────────────────────────────────
df['senior'] = np.where(df['years_exp'] >= 5, 'Senior', 'Junior')

# ── Conditional column using pd.cut (bins) ────────────────────────────────────
df['salary_band'] = pd.cut(
    df['salary'],
    bins   = [0, 50_000, 65_000, 1_00_000],
    labels = ['Band A', 'Band B', 'Band C']
)

# ── Rename a column ───────────────────────────────────────────────────────────
df = df.rename(columns={'emp_id': 'ID', 'joining_yr': 'joined'})

print(df[['ID', 'name', 'salary', 'senior', 'salary_band', 'years_exp']])
```

---
## Section 7: Sorting


```python
# ── sort_values ───────────────────────────────────────────────────────────────
df_sorted = df.sort_values('salary', ascending=False)  # highest first
print('Sorted by salary (desc):')
print(df_sorted[['name', 'department', 'salary']])

# Sort by multiple columns
df_multi = df.sort_values(['department', 'salary'], ascending=[True, False])
print('\nSorted by dept (asc) then salary (desc):')
print(df_multi[['name', 'department', 'salary']])

# Reset index after sorting (optional but clean)
df_sorted = df_sorted.reset_index(drop=True)
print('\nTop earner (index 0):', df_sorted.loc[0, 'name'], df_sorted.loc[0, 'salary'])
```

---
## Section 8: Handling Missing Values


```python
# Create a DataFrame with missing values (NaN = Not a Number)
import numpy as np

dirty = pd.DataFrame({
    'name'     : ['Aarav', 'Bhavna', None, 'Deepika', 'Eshaan'],
    'amount'   : [5000, np.nan, 8000, np.nan, 12000],
    'category' : ['Sales', 'Tax', 'Sales', None, 'Tax'],
    'days_due' : [30, 45, np.nan, 60, 15],
})

print('DataFrame with missing values:')
print(dirty)
print('\nMissing value count per column:')
print(dirty.isna().sum())
```


```python
# ── Option 1: fillna — fill with a specific value ────────────────────────────
filled = dirty.copy()
filled['amount']   = filled['amount'].fillna(0)              # fill amount with 0
filled['days_due'] = filled['days_due'].fillna(filled['days_due'].mean())  # fill with mean
filled['category'] = filled['category'].fillna('Unknown')    # fill text with label
print('After fillna:')
print(filled)

# ── Option 2: dropna — drop rows with any missing value ──────────────────────
clean = dirty.dropna()
print('\nAfter dropna (rows with ANY missing removed):')
print(clean)

# Drop only if ALL values in the row are missing
# dirty.dropna(how='all')
```

---
## Section 9: Aggregation and GroupBy


```python
# ── Simple aggregation ────────────────────────────────────────────────────────
print('Total salary bill:', df['salary'].sum())
print('Average salary   :', df['salary'].mean().round(0))
print('Salary range     :', df['salary'].min(), '—', df['salary'].max())

# Count unique departments
print('Unique depts     :', df['department'].nunique())
print('Value counts:')
print(df['department'].value_counts())
```


```python
# ── GroupBy: split → apply → combine ─────────────────────────────────────────
# Q: What is the total and average salary by department?

dept_summary = (
    df
    .groupby('department')['salary']
    .agg(
        Headcount = 'count',
        Total_CTC = 'sum',
        Avg_Salary = 'mean',
        Min_Salary = 'min',
        Max_Salary = 'max'
    )
    .round(0)
    .sort_values('Total_CTC', ascending=False)
)
print('Department-wise salary analysis:')
print(dept_summary)
```


```python
# ── GroupBy on multiple columns ───────────────────────────────────────────────
# Total salary by department AND grade

multi_group = (
    employees
    .groupby(['department', 'grade'])['salary']
    .agg(['count', 'sum', 'mean'])
    .rename(columns={'count': 'headcount', 'sum': 'total', 'mean': 'avg'})
    .round(0)
)
print(multi_group)
```

---
## Section 10: Merging DataFrames (VLOOKUP Equivalent)


```python
# Imagine: a transaction table and a master table

# Master: Party details
party_master = pd.DataFrame({
    'party_code': ['P001', 'P002', 'P003', 'P004'],
    'party_name': ['ABC Traders', 'XYZ Suppliers', 'PQR Services', 'LMN Corp'],
    'credit_limit': [5_00_000, 10_00_000, 2_50_000, 8_00_000],
    'payment_terms': ['Net30', 'Net45', 'Net30', 'Net60'],
})

# Transactions: purchases this month
transactions = pd.DataFrame({
    'inv_no'    : ['INV001', 'INV002', 'INV003', 'INV004', 'INV005'],
    'party_code': ['P002', 'P001', 'P003', 'P002', 'P004'],
    'amount'    : [1_50_000, 85_000, 45_000, 3_20_000, 2_10_000],
    'date'      : ['2024-04-05', '2024-04-07', '2024-04-10', '2024-04-12', '2024-04-15'],
})

print('Party Master:')
print(party_master)
print('\nTransactions:')
print(transactions)
```


```python
# ── pd.merge = VLOOKUP ────────────────────────────────────────────────────────
# how='left'  → keep all rows from left (like VLOOKUP, no match = NaN)
# how='inner' → only matching rows from both
# how='outer' → all rows from both

enriched = pd.merge(
    left   = transactions,
    right  = party_master,
    on     = 'party_code',
    how    = 'left'
)

print('Enriched transactions (with party details):')
print(enriched[['inv_no', 'party_name', 'amount', 'credit_limit', 'payment_terms']])

# Useful check: is any amount > credit limit?
over_limit = enriched[enriched['amount'] > enriched['credit_limit']]
print('\nInvoices exceeding credit limit:')
print(over_limit[['inv_no', 'party_name', 'amount', 'credit_limit']])
```

---
## Section 11: Pivot Tables


```python
# Create a richer dataset
np.random.seed(7)
months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
depts  = ['Sales', 'Purchase', 'Admin']

txn_data = pd.DataFrame({
    'month'  : np.random.choice(months, 30),
    'dept'   : np.random.choice(depts, 30),
    'amount' : np.random.randint(10_000, 5_00_000, 30),
    'type'   : np.random.choice(['Expense', 'Income'], 30),
})

# ── pd.pivot_table ─────────────────────────────────────────────────────────────
pivot = txn_data.pivot_table(
    values  = 'amount',
    index   = 'month',
    columns = 'dept',
    aggfunc = 'sum',
    fill_value = 0,
    margins    = True,   # adds row/column totals
    margins_name = 'Total'
)
print('Monthly Amount by Department:')
print(pivot)
```

---
## Section 12: Reading & Writing Files


```python
# ── Write to CSV ──────────────────────────────────────────────────────────────
employees.to_csv('/tmp/employees.csv', index=False)  # index=False: don't save the row numbers
print('CSV saved!')

# ── Read from CSV ──────────────────────────────────────────────────────────────
df_from_csv = pd.read_csv('/tmp/employees.csv')
print('Read back from CSV:')
print(df_from_csv.head(3))
```


```python
# ── Write to Excel ────────────────────────────────────────────────────────────
# Requires: pip install openpyxl
try:
    with pd.ExcelWriter('/tmp/hr_data.xlsx', engine='openpyxl') as writer:
        employees.to_excel(writer, sheet_name='Employees', index=False)
        dept_summary.to_excel(writer, sheet_name='Dept Summary')
    print('Excel file written to /tmp/hr_data.xlsx')
except ImportError:
    print('Install openpyxl: pip install openpyxl')

# ── Read from Excel ───────────────────────────────────────────────────────────
# df_excel = pd.read_excel('my_file.xlsx', sheet_name='Sheet1')
```

---
## Section 13: Quick Reference Summary

```python
import pandas as pd

# Create
pd.Series([1,2,3], index=['a','b','c'])
pd.DataFrame({'col1': [...], 'col2': [...]})
pd.read_csv('file.csv')            # read CSV
pd.read_excel('file.xlsx')         # read Excel

# Explore
df.shape      # (rows, cols)
df.columns    # column names
df.dtypes     # data types
df.head(n)    # first n rows
df.tail(n)    # last n rows
df.info()     # summary incl. nulls
df.describe() # stats for numerics

# Select
df['col']              # single column (Series)
df[['c1','c2']]        # multiple columns (DataFrame)
df.loc[row, col]       # by label
df.iloc[row, col]      # by position

# Filter
df[df['col'] > val]
df[df['col'].isin([v1, v2])]
df[(cond1) & (cond2)]

# Modify
df['new'] = df['a'] + df['b']          # new column
df.rename(columns={'old': 'new'})
df.drop(columns=['col'])

# Aggregation
df['col'].sum() / .mean() / .count()
df.groupby('col').agg({'col2': 'sum'})
df.pivot_table(values, index, columns, aggfunc)

# Missing
df.isna().sum()        # count missing
df.fillna(value)       # fill
df.dropna()            # drop

# Merge (VLOOKUP)
pd.merge(left, right, on='key', how='left')

# Sort
df.sort_values('col', ascending=False)

# Write
df.to_csv('file.csv', index=False)
df.to_excel('file.xlsx', sheet_name='Sheet1', index=False)
```

---
## Practice Exercises

1. Create a DataFrame for 5 vendors with columns: `vendor_id`, `vendor_name`, `city`, `outstanding_balance`, `days_overdue`. Filter vendors with balance > ₹50,000 AND days overdue > 30.

2. Add a column `penalty` = 2% of `outstanding_balance` if `days_overdue` > 45, else 0.

3. Group the vendor DataFrame by `city` and compute total outstanding per city.

4. Create two DataFrames — one with invoice numbers + amounts, another with invoice numbers + party names. Merge them to get a combined view.

5. Create a pivot table from a 20-row transaction dataset showing total amount by month and transaction type.


```python
# ── Exercise Solutions ─────────────────────────────────────────────────────────

# Exercise 1 & 2: Vendor analysis
vendors = pd.DataFrame({
    'vendor_id'  : ['V01', 'V02', 'V03', 'V04', 'V05'],
    'vendor_name': ['Sunrise Trading', 'Metro Supplies', 'Galaxy Corp',
                    'Omega Services', 'Zenith Ltd'],
    'city'       : ['Mumbai', 'Delhi', 'Mumbai', 'Pune', 'Delhi'],
    'outstanding': [80_000, 30_000, 1_20_000, 15_000, 90_000],
    'days_overdue': [45, 20, 60, 10, 50],
})

# Filter: balance > 50K AND overdue > 30 days
risky = vendors[(vendors['outstanding'] > 50_000) & (vendors['days_overdue'] > 30)]
print('Risky vendors:')
print(risky[['vendor_name', 'outstanding', 'days_overdue']])

# Penalty column
vendors['penalty'] = np.where(vendors['days_overdue'] > 45,
                               vendors['outstanding'] * 0.02, 0)
print('\nWith penalty:')
print(vendors[['vendor_name', 'outstanding', 'days_overdue', 'penalty']])

# Group by city
city_summary = vendors.groupby('city')['outstanding'].agg(['count', 'sum'])
print('\nCity-wise outstanding:')
print(city_summary)
```
