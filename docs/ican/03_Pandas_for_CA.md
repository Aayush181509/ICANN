# 🐼 Pandas for CA Professionals
**From Raw Data to Financial Insight**

---

**Pre-requisite:** Module 2 (NumPy)  
**Estimated time:** 5–6 hours  
**Session structure:** Why Pandas → What is Pandas → Core Concepts → Hands-on Practice → Applications

---

## 📋 Table of Contents

| Part | Section | Topic |
|------|---------|-------|
| **Part 1: Why Pandas?** | 1 | The Limits of NumPy — What It Cannot Handle |
| | 2 | What is Pandas? — History & Design Philosophy |
| **Part 2: Fundamentals** | 3 | The Index — Pandas' Core Innovation |
| | 4 | Pandas Data Types (dtype) |
| | 5 | Series & DataFrame Architecture |
| **Part 3: Hands-on** | 6 | Installing & Importing Pandas |
| | 7 | Series — A Single Column |
| | 8 | DataFrame — The Full Spreadsheet |
| | 9 | Exploring Your Data |
| | 10 | Selecting Columns & Rows |
| | 11 | Filtering Data |
| | 12 | Sorting Data |
| | 13 | Calculated Columns |
| | 14 | GroupBy — Pivot Tables |
| | 15 | Handling Missing Values |
| | 16 | Merging DataFrames (VLOOKUP) |
| | 17 | Reading & Writing Excel / CSV |
| | 18 | String Operations |
| **Part 4: Practice** | 19 | Practice Exercises |

---

## Part 1: Why Pandas?

## Section 1: The Limits of NumPy — What It Cannot Handle

You have already learned NumPy — Python's fast numerical engine. So why do we need another library?

NumPy is outstanding for **pure mathematical computation**, but real-world financial data is messy:

| What real data looks like | NumPy's limitation |
|---------------------------|--------------------|
| A ledger has dates, names, amounts, GST codes | NumPy arrays are **homogeneous** — one data type per array |
| You want to say `ledger['Apr']` | NumPy uses only **positional** indexing — `array[3]` |
| Bank statements have blank cells | NumPy has no native **missing value** handling |
| VAT-401 has column headers (GSTIN, HSN, Rate…) | 2-D NumPy arrays have **no column names** |
| You need to join two tables (like VLOOKUP) | NumPy has **no built-in merge / join** |

### The NumPy wall — a concrete example

Imagine you receive a trial balance as a CSV with 500 rows and 8 columns:  
`Account | Type | Opening Dr | Opening Cr | Transactions Dr | Transactions Cr | Closing Dr | Closing Cr`

In NumPy you can only store this if you:
- Convert all text to numbers (losing meaning), OR
- Use a structured array (complex, rarely used in practice)

In **Pandas**, you simply call `pd.read_csv('trial_balance.csv')` — and you're done.

> **The rule of thumb:** Use NumPy when you have pure numbers and need maximum speed.  
> Use Pandas when you have real-world tabular data with mixed types, labels, and missing values.


```python
import numpy as np
import pandas as pd

# --- NumPy approach: storing a simple transaction table ---
# NumPy can only hold ONE data type. Mixing strings + numbers forces 'object' dtype
# and you lose ALL numeric speed advantages.

np_attempt = np.array([
    ['INV-001', 'Alpha Ltd',   '85000', '18', 'Paid'],
    ['INV-002', 'Beta Corp',   '42000', '12', 'Pending'],
    ['INV-003', 'Everest Imports Pvt. Ltd.',  '120000',  '5', 'Paid'],
])
print("NumPy mixed array dtype:", np_attempt.dtype)   # object — all converted to string!
print("Can we sum the Amount column?")
try:
    print(np_attempt[:, 2].sum())   # string concat, not addition!
except Exception as e:
    print("Error:", e)

# --- Pandas approach: same data, zero effort ---
df = pd.DataFrame({
    'Invoice': ['INV-001', 'INV-002', 'INV-003'],
    'Party':   ['Alpha Ltd', 'Beta Corp', 'Everest Imports Pvt. Ltd.'],
    'Amount':  [85000, 42000, 120000],          # stored as int64
    'Rate':    [18, 12, 5],                      # stored as int64
    'Status':  ['Paid', 'Pending', 'Paid'],      # stored as object (string)
})
print("\nPandas dtypes:")
print(df.dtypes)
print("\nTotal amount:", df['Amount'].sum())    # Works perfectly!
print("Pending invoices:")
print(df[df['Status'] == 'Pending'][['Invoice', 'Party', 'Amount']])
```

    NumPy mixed array dtype: <U25
    Can we sum the Amount column?
    Error: the resolved dtypes are not compatible with add.reduce. Resolved (dtype('<U25'), dtype('<U25'), dtype('<U50'))
    
    Pandas dtypes:
    Invoice    object
    Party      object
    Amount      int64
    Rate        int64
    Status     object
    dtype: object
    
    Total amount: 247000
    Pending invoices:
       Invoice      Party  Amount
    1  INV-002  Beta Corp   42000


## Section 2: What is Pandas? — History & Design Philosophy

### The Origin Story

In **2008**, Wes McKinney was working at **AQR Capital Management** — a quantitative hedge fund in Greenwich, Connecticut managing billions of dollars. His job was to analyse financial time-series data: stock prices, returns, correlations.

Excel was too slow for millions of rows. R's data frames were close, but Python had nothing.  
So he built one.

> *"I started pandas because I was frustrated"* — Wes McKinney, 2012

He open-sourced Pandas in **2009**. Today it has over **200 million downloads per month** and is the backbone of financial data analysis worldwide.

### What does the name mean?

**Pandas = Pan-el Data + Python**

"Panel data" is an economics term for data that tracks multiple subjects over time — like a company's quarterly financials across multiple years. That is exactly the kind of data Pandas was designed to handle.

### Where Pandas fits in the Python ecosystem

```
                    ┌─────────────────────────────────────────┐
   Your Python      │  Pandas   Matplotlib   Seaborn  Plotly  │  ← Analysis & Viz
   Analysis Stack   │           (all built on top of NumPy)   │
                    ├─────────────────────────────────────────┤
                    │               NumPy                      │  ← Numerical Engine
                    ├─────────────────────────────────────────┤
                    │            CPython / C                   │  ← Runtime
                    └─────────────────────────────────────────┘
```

### Who uses Pandas today?

| Sector | Use case |
|--------|----------|
| Accounting & Audit | Trial balance analysis, VAT Return reconciliation, variance reports |
| Investment Banking | Financial modelling, M&A data rooms |
| Central Banks | Monetary data aggregation, policy analysis |
| Big Four firms | Automated data extraction from ERP systems |
| Regulators (SEBON, NRB) | Market surveillance, filing analysis |

For a **CA professional**, Pandas is arguably the single most valuable Python library to learn.

## Part 2: Pandas Fundamentals

## Section 3: The Index — Pandas' Core Innovation

The single most important concept in Pandas — and the feature that makes it superior to plain NumPy for financial data — is **the Index**.

### What is an Index?

Every Pandas object (Series or DataFrame) has an **Index**: a set of labels attached to its rows.

| In Excel | In NumPy | In Pandas |
|----------|----------|-----------|
| Row 3 (position) | `array[2]` (position) | `df.loc['Apr']` **(label)** |

Think of the Index as a **register** — like a ledger folio number that lets you find any entry by name, not just by page count.

### Why does this matter for finance?

- Access monthly P&L data by **month name** (`'Apr'`, `'Mar'`) rather than position (0, 11)
- Work with **date-indexed** time series (stock prices, daily cash flow)
- **Align** two datasets automatically on their index — Pandas lines them up even if the rows are in different orders
- Perform **time-based resampling** (daily → monthly → quarterly) using the DatetimeIndex

### Types of Index

| Index type | Example | Finance use case |
|------------|---------|-----------------|
| RangeIndex (default) | 0, 1, 2, 3… | General tabular data |
| StringIndex | 'Apr', 'May'… | Monthly reports |
| DatetimeIndex | 2025-04-01, 2025-04-02… | Daily price/transaction data |
| IntegerIndex | 1001, 1002, 1003… | Voucher numbers, GL codes |
| MultiIndex | (Q1, Apr), (Q1, May)… | Hierarchical financial statements |


```python
import pandas as pd

# --- Default RangeIndex (0, 1, 2...) ---
revenue_default = pd.Series([1250000, 1380000, 1120000])
print("Default index:")
print(revenue_default)

# --- Custom StringIndex: access by month name ---
revenue = pd.Series(
    data  = [1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
             1550000, 1420000, 1680000, 1910000, 2030000, 2150000],
    index = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar'],
    name  = 'Revenue (NPR )'
)
print("\nNamed index — access by month:")
print("April:", revenue['Apr'])          # label-based
print("Last month:", revenue.iloc[-1])   # still works positionally too

# --- Automatic alignment by index (NumPy cannot do this!) ---
revenue_fy25 = pd.Series([1250000, 1380000, 1120000], index=['Apr', 'May', 'Jun'])
revenue_fy26 = pd.Series([1450000, 1650000, 1210000], index=['May', 'Jun', 'Jul'])

# Pandas aligns on the shared index automatically — NaN for unmatched months
growth = revenue_fy26 - revenue_fy25
print("\nGrowth (auto-aligned by month name):")
print(growth)  # Apr=NaN (no FY26 Apr), May/Jun=difference, Jul=NaN (no FY 2082 BS Jul)
```

    Default index:
    0    1250000
    1    1380000
    2    1120000
    dtype: int64
    
    Named index — access by month:
    April: 1250000
    Last month: 2150000
    
    Growth (auto-aligned by month name):
    Apr         NaN
    Jul         NaN
    Jun    530000.0
    May     70000.0
    dtype: float64


## Section 4: Pandas Data Types (dtype)

Every column in a Pandas DataFrame has a **dtype** — the type of data it stores. Understanding dtypes is essential because:

1. Wrong dtype → wrong results (e.g., amounts stored as text can't be summed)
2. Right dtype → better memory efficiency and faster operations
3. Pandas operations behave differently depending on dtype

### The Pandas dtype table

| dtype | What it stores | Memory | Finance example |
|-------|---------------|--------|-----------------|
| `int64` | Whole numbers | 8 bytes | Voucher numbers, quantities |
| `float64` | Decimal numbers | 8 bytes | Amounts, GST rates, percentages |
| `object` | Strings / mixed | Variable | Party names, account codes, GSTIN |
| `bool` | True / False | 1 byte | Paid? Audited? Flagged? |
| `datetime64[ns]` | Dates and times | 8 bytes | Invoice dates, due dates, FY periods |
| `category` | Fixed set of values | Low | GST slabs, account types, quarters |

### The most common mistake in financial data

When you import a CSV from Tally or SAP, amounts are often read as **`object`** (string) because of formatting:  
`"NPR 1,25,000"` → Pandas cannot sum this until you clean and cast it to `float64`.

### The `category` dtype — a hidden gem

If a column has only a few repeating values ('Q1','Q2','Q3','Q4' or 'Asset','Liability','Income','Expense'), store it as `category`:
- Uses **5–10× less memory** than `object`
- Sorting respects the **logical order** you define (Apr before May, not alphabetical)


```python
import pandas as pd
import numpy as np

# --- Checking dtypes ---
trial_balance = pd.DataFrame({
    'Account':   ['Cash','Trade Debtors','Fixed Assets','Creditors','Sales'],
    'Type':      ['Asset','Asset','Asset','Liability','Income'],
    'Quarter':   ['Q4','Q4','Q4','Q4','Q4'],
    'Debit':     [485000, 1250000, 8500000, 0, 0],
    'Credit':    [0, 0, 0, 980000, 5200000],
    'Date':      ['2025-03-31']*5,
})

print("Default dtypes after DataFrame creation:")
print(trial_balance.dtypes)

# --- Type conversion ---
# Convert Date string → datetime64
trial_balance['Date'] = pd.to_datetime(trial_balance['Date'])

# Convert Type and Quarter → category (saves memory, enables proper sorting)
trial_balance['Type']    = trial_balance['Type'].astype('category')
trial_balance['Quarter'] = trial_balance['Quarter'].astype('category')

print("\nAfter conversion:")
print(trial_balance.dtypes)

# --- Memory comparison ---
n = 50000  # simulate a large ledger
large_df = pd.DataFrame({'Type': np.random.choice(['Asset','Liability','Income','Expense'], n)})
mem_object   = large_df['Type'].astype('object').memory_usage(deep=True)
mem_category = large_df['Type'].astype('category').memory_usage(deep=True)
print(f"\nMemory for 50,000 account-type rows:")
print(f"  object dtype:   {mem_object:,} bytes")
print(f"  category dtype: {mem_category:,} bytes  ({mem_object/mem_category:.0f}x smaller!)")

# --- The common import problem: amount as string ---
messy = pd.Series(['1,25,000', 'NPR 82,000', '45000', '1,20,000'])
print("\nAmount column as imported (object):", messy.dtype)
cleaned = messy.str.replace('[NPR ,]', '', regex=True).astype(float)
print("After cleaning (float64):", cleaned.dtype)
print("Sum:", cleaned.sum())
```

    Default dtypes after DataFrame creation:
    Account    object
    Type       object
    Quarter    object
    Debit       int64
    Credit      int64
    Date       object
    dtype: object
    
    After conversion:
    Account            object
    Type             category
    Quarter          category
    Debit               int64
    Credit              int64
    Date       datetime64[ns]
    dtype: object
    
    Memory for 50,000 account-type rows:
      object dtype:   3,187,540 bytes
      category dtype: 50,555 bytes  (63x smaller!)
    
    Amount column as imported (object): object
    After cleaning (float64): float64
    Sum: 372000.0


## Section 5: Series & DataFrame Architecture

Before we dive into hands-on work, let's understand exactly what a **Series** and a **DataFrame** are — structurally.

### Series: A Labeled Column

A **Series** is a one-dimensional labeled array. Think of it as a **single column from a ledger** — with row labels (the Index) and values.

```
  Index  │  Values
─────────┼──────────
   Apr   │  1,250,000   ←── one row
   May   │  1,380,000
   Jun   │  1,120,000
         │
   name: Revenue (NPR )
   dtype: int64
```

A Series has exactly two attributes that define it: **index** + **values** (+ a name).

### DataFrame: A Labeled Table

A **DataFrame** is a collection of **Series that share the same Index**. Think of it as a **complete spreadsheet** — rows identified by the Index, columns identified by column names.

```
  Index  │  Month │  Revenue  │  COGS   │  Net_Profit
─────────┼────────┼───────────┼─────────┼───────────
    0    │  Apr   │ 1,250,000 │ 750,000 │   197,000
    1    │  May   │ 1,380,000 │ 828,000 │   229,000
    2    │  Jun   │ 1,120,000 │ 672,000 │   185,000
         │        │           │         │
         │ object │   int64   │  int64  │    int64    ←── each column has its own dtype
```

**Key relationships:**
- `df['Revenue']` → returns a **Series** (one column)
- `df[['Revenue', 'COGS']]` → returns a **DataFrame** (subset of columns)
- `df.loc[0]` → returns a **Series** (one row)

### The CA Analogy

| Pandas object | CA equivalent |
|---------------|---------------|
| Index | Folio / Row reference number |
| Series | A single column in a ledger (e.g., "Credit" column) |
| DataFrame | The complete ledger / trial balance / VAT-401 table |
| Column dtype | The data validation rule for that column |

With this foundation, every operation you do in Pandas — filtering, grouping, merging — makes intuitive sense. You are always working with **labeled rows and columns**.

## Part 3: Hands-on with Pandas

## Section 6: Installing & Importing Pandas


```python
# Install if needed (run once)
# !pip install pandas openpyxl

import pandas as pd    # pd is the universal shorthand
import numpy as np     # Often used alongside pandas

print('Pandas version:', pd.__version__)
print('Ready!')
```

    Pandas version: 2.3.2
    Ready!


## Section 7: Series — A Single Column

A **Series** is the simplest Pandas object — it's like **one column** of a spreadsheet.  
It has an **index** (row label) and **values** (the data).


```python
# Creating a Series — monthly revenue
monthly_revenue = pd.Series(
    data  = [1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
             1550000, 1420000, 1680000, 1910000, 2030000, 2150000],
    index = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
             'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],
    name  = 'Revenue (NPR )'
)

print(monthly_revenue)
print('\nType:', type(monthly_revenue))
```

    Apr    1250000
    May    1380000
    Jun    1120000
    Jul    1450000
    Aug    1620000
    Sep    1780000
    Oct    1550000
    Nov    1420000
    Dec    1680000
    Jan    1910000
    Feb    2030000
    Mar    2150000
    Name: Revenue (NPR ), dtype: int64
    
    Type: <class 'pandas.core.series.Series'>



```python
# Series operations — all vectorized like NumPy
print('Total:  NPR ', monthly_revenue.sum())
print('Mean:   NPR ', round(monthly_revenue.mean(), 2))
print('Max:    NPR ', monthly_revenue.max(), '(', monthly_revenue.idxmax(), ')')
print('Min:    NPR ', monthly_revenue.min(), '(', monthly_revenue.idxmin(), ')')
print()

# Access by label (like looking up a row in Excel)
print('April Revenue:', monthly_revenue['Apr'])
print('Q4 Revenue:')
print(monthly_revenue[['Jan', 'Feb', 'Mar']])

# Filtering — months where revenue exceeded NPR 17 lakhs
print('\nHigh revenue months (>NPR 17L):')
print(monthly_revenue[monthly_revenue > 1700000])
```

    Total:  NPR  19340000
    Mean:   NPR  1611666.67
    Max:    NPR  2150000 ( Mar )
    Min:    NPR  1120000 ( Jun )
    
    April Revenue: 1250000
    Q4 Revenue:
    Jan    1910000
    Feb    2030000
    Mar    2150000
    Name: Revenue (NPR ), dtype: int64
    
    High revenue months (>NPR 17L):
    Sep    1780000
    Jan    1910000
    Feb    2030000
    Mar    2150000
    Name: Revenue (NPR ), dtype: int64


## Section 3 & 4: DataFrame — The Full Spreadsheet

A **DataFrame** is Pandas' main object — think of it as a **complete Excel worksheet**.  
It has rows (indexed), columns (named), and can hold different data types in different columns.

### Creating a DataFrame


```python
# Method 1: From a dictionary (most common)
# Each key = column name, each value = list of column data

ledger_data = {
    'Date':        ['01-Apr-2025', '03-Apr-2025', '05-Apr-2025', '08-Apr-2025',
                    '10-Apr-2025', '12-Apr-2025', '15-Apr-2025', '18-Apr-2025'],
    'Voucher_No':  ['SV-001', 'PV-101', 'SV-002', 'PV-102', 'SV-003', 'PV-103', 'PV-104', 'SV-004'],
    'Description': ['Sales - Client A', 'Office Rent', 'Sales - Client B', 'Electricity Bill',
                    'Sales - Client C', 'Salaries Paid', 'Vendor Payment', 'Sales - Client D'],
    'Category':    ['Revenue', 'Expense', 'Revenue', 'Expense',
                    'Revenue', 'Expense', 'Expense', 'Revenue'],
    'Debit':       [0, 45000, 0, 12000, 0, 180000, 95000, 0],
    'Credit':      [320000, 0, 185000, 0, 420000, 0, 0, 275000],
}

df = pd.DataFrame(ledger_data)
print(df)
```

              Date Voucher_No       Description Category   Debit  Credit
    0  01-Apr-2025     SV-001  Sales - Client A  Revenue       0  320000
    1  03-Apr-2025     PV-101       Office Rent  Expense   45000       0
    2  05-Apr-2025     SV-002  Sales - Client B  Revenue       0  185000
    3  08-Apr-2025     PV-102  Electricity Bill  Expense   12000       0
    4  10-Apr-2025     SV-003  Sales - Client C  Revenue       0  420000
    5  12-Apr-2025     PV-103     Salaries Paid  Expense  180000       0
    6  15-Apr-2025     PV-104    Vendor Payment  Expense   95000       0
    7  18-Apr-2025     SV-004  Sales - Client D  Revenue       0  275000


## Section 10: Exploring Your Data

When you receive a financial data file, the first step is always to **understand what's in it**.  
Pandas has several built-in functions for this.


```python
# Create a larger sample dataset — Monthly P&L (FY 2081-82 BS)
import numpy as np
np.random.seed(42)

months = ['Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush',
          'Magh', 'Falgun', 'Chaitra', 'Baishakh', 'Jestha', 'Ashadh']

# Nepal FY quarters: Q1=Shrawan-Ashwin, Q2=Kartik-Poush, Q3=Magh-Chaitra, Q4=Baishakh-Ashadh
quarters = ['Q1','Q1','Q1', 'Q2','Q2','Q2', 'Q3','Q3','Q3', 'Q4','Q4','Q4']

revenue      = np.random.randint(800000, 2000000, 12)
cogs         = revenue * np.random.uniform(0.35, 0.55, 12)
gross_profit = revenue - cogs
opex         = gross_profit * np.random.uniform(0.20, 0.40, 12)
net_profit   = gross_profit - opex

pl_df = pd.DataFrame({
    'Month':        months,
    'Quarter':      quarters,
    'Revenue':      revenue.round(-3).astype(int),
    'COGS':         cogs.round(-3).astype(int),
    'Gross_Profit': gross_profit.round(-3).astype(int),
    'Opex':         opex.round(-3).astype(int),
    'Net_Profit':   net_profit.round(-3).astype(int),
})

pl_df['Margin_Pct'] = (pl_df['Net_Profit'] / pl_df['Revenue'] * 100).round(2)

print(f'Monthly P&L Dataset — FY 2081-82 BS ({pl_df.shape[0]} months)')
print(pl_df.head())
```

    Monthly P&L Dataset — FY 2081-82 BS (12 months)
         Month Quarter  Revenue    COGS  Gross_Profit    Opex  Net_Profit  \
    0  Shrawan      Q1   922000  349000        573000  160000      413000   
    1   Bhadra      Q1  1471000  706000        765000  160000      605000   
    2   Ashwin      Q1   932000  337000        595000  235000      360000   
    3   Kartik      Q2  1059000  524000        536000  132000      403000   
    4  Mangsir      Q2   910000  489000        421000   92000      329000   
    
       Margin_Pct  
    0       44.79  
    1       41.13  
    2       38.63  
    3       38.05  
    4       36.15  



```python
print('--- Last 3 rows (tail) ---')
print(pl_df.tail(3))

print('\n--- Dataset Dimensions ---')
print('Rows x Columns:', pl_df.shape)

print('\n--- Column Names ---')
print(pl_df.columns.tolist())

print('\n--- Data Types of Each Column ---')
print(pl_df.dtypes)
```

    --- Last 3 rows (tail) ---
           Month Quarter  Revenue    COGS  Gross_Profit    Opex  Net_Profit  \
    9   Baishakh      Q4  1936000  680000       1256000  467000      789000   
    10    Jestha      Q4  1713000  607000       1105000  371000      734000   
    11    Ashadh      Q4   975000  444000        532000  154000      377000   
    
        Margin_Pct  
    9        40.75  
    10       42.85  
    11       38.67  
    
    --- Dataset Dimensions ---
    Rows x Columns: (12, 8)
    
    --- Column Names ---
    ['Month', 'Quarter', 'Revenue', 'COGS', 'Gross_Profit', 'Opex', 'Net_Profit', 'Margin_Pct']
    
    --- Data Types of Each Column ---
    Month            object
    Quarter          object
    Revenue           int64
    COGS              int64
    Gross_Profit      int64
    Opex              int64
    Net_Profit        int64
    Margin_Pct      float64
    dtype: object



```python
# describe() — the most useful single command for financial data
# Gives count, mean, std, min, max, quartiles for all numeric columns

print('--- Statistical Summary ---')
print(pl_df[['Revenue', 'COGS', 'Gross_Profit', 'Net_Profit', 'Margin_Pct']].describe().round(2))
```

    --- Statistical Summary ---
              Revenue        COGS  Gross_Profit  Net_Profit  Margin_Pct
    count       12.00       12.00         12.00       12.00       12.00
    mean   1340833.33   584250.00     756916.67   522833.33       38.89
    std     424008.33   208294.43     272493.36   175512.67        4.09
    min     910000.00   337000.00     421000.00   298000.00       31.80
    25%     935750.00   444000.00     535000.00   372750.00       37.00
    50%    1265000.00   530500.00     680000.00   509000.00       38.65
    75%    1734750.00   686500.00     961500.00   671500.00       41.56
    max    1936000.00  1044000.00    1256000.00   789000.00       44.79


## Section 11: Selecting Columns & Rows

### Selecting columns


```python
# Select a single column — returns a Series
print('Revenue column:')
print(pl_df['Revenue'])

print('\n--- Select multiple columns — returns a DataFrame ---')
print(pl_df[['Month', 'Revenue', 'Net_Profit', 'Margin_Pct']])
```

    Revenue column:
    0      922000
    1     1471000
    2      932000
    3     1059000
    4      910000
    5     1532000
    6     1903000
    7      937000
    8     1800000
    9     1936000
    10    1713000
    11     975000
    Name: Revenue, dtype: int64
    
    --- Select multiple columns — returns a DataFrame ---
           Month  Revenue  Net_Profit  Margin_Pct
    0    Shrawan   922000      413000       44.79
    1     Bhadra  1471000      605000       41.13
    2     Ashwin   932000      360000       38.63
    3     Kartik  1059000      403000       38.05
    4    Mangsir   910000      329000       36.15
    5      Poush  1532000      673000       43.93
    6       Magh  1903000      622000       32.69
    7     Falgun   937000      298000       31.80
    8    Chaitra  1800000      671000       37.28
    9   Baishakh  1936000      789000       40.75
    10    Jestha  1713000      734000       42.85
    11    Ashadh   975000      377000       38.67



```python
# Selecting rows using .loc[] (label-based) and .iloc[] (position-based)

# .iloc[] — by row NUMBER (like Excel row number, starts from 0)
print('First row (iloc[0]):')
print(pl_df.iloc[0])

print('\nRows 0 to 2 (iloc[0:3]):')
print(pl_df.iloc[0:3])

print('\nLast row:')
print(pl_df.iloc[-1])
```

    First row (iloc[0]):
    Month           Shrawan
    Quarter              Q1
    Revenue          922000
    COGS             349000
    Gross_Profit     573000
    Opex             160000
    Net_Profit       413000
    Margin_Pct        44.79
    Name: 0, dtype: object
    
    Rows 0 to 2 (iloc[0:3]):
         Month Quarter  Revenue    COGS  Gross_Profit    Opex  Net_Profit  \
    0  Shrawan      Q1   922000  349000        573000  160000      413000   
    1   Bhadra      Q1  1471000  706000        765000  160000      605000   
    2   Ashwin      Q1   932000  337000        595000  235000      360000   
    
       Margin_Pct  
    0       44.79  
    1       41.13  
    2       38.63  
    
    Last row:
    Month           Ashadh
    Quarter             Q4
    Revenue         975000
    COGS            444000
    Gross_Profit    532000
    Opex            154000
    Net_Profit      377000
    Margin_Pct       38.67
    Name: 11, dtype: object


## Section 12: Filtering Data — Like Excel AutoFilter


```python
# Filter rows where Revenue > NPR 15 lakhs
high_revenue = pl_df[pl_df['Revenue'] > 1500000]
print('Months with revenue > NPR 15L:')
print(high_revenue[['Month', 'Revenue', 'Net_Profit']].to_string(index=False))
```

    Months with revenue > NPR 15L:
       Month  Revenue  Net_Profit
       Poush  1532000      673000
        Magh  1903000      622000
     Chaitra  1800000      671000
    Baishakh  1936000      789000
      Jestha  1713000      734000



```python
# Multiple conditions — using & (and) and | (or)

# Months where revenue > NPR 15L AND profit margin > 13%
strong_months = pl_df[(pl_df['Revenue'] > 1500000) & (pl_df['Margin_Pct'] > 13)]
print('Strong months (Revenue >NPR 15L AND Margin >13%):')
print(strong_months[['Month', 'Revenue', 'Margin_Pct']].to_string(index=False))

# Filter by text — Q1 months only
q1_data = pl_df[pl_df['Quarter'] == 'Q1']
print('\nQ1 Data:')
print(q1_data[['Month', 'Quarter', 'Revenue', 'Net_Profit']].to_string(index=False))

# isin() — filter where value is in a list (like Excel's multiple AutoFilter)
selected_quarters = pl_df[pl_df['Quarter'].isin(['Q1', 'Q4'])]
print('\nQ1 and Q4 data:')
print(selected_quarters[['Month', 'Quarter', 'Revenue']].to_string(index=False))
```

    Strong months (Revenue >NPR 15L AND Margin >13%):
       Month  Revenue  Margin_Pct
       Poush  1532000       43.93
        Magh  1903000       32.69
     Chaitra  1800000       37.28
    Baishakh  1936000       40.75
      Jestha  1713000       42.85
    
    Q1 Data:
      Month Quarter  Revenue  Net_Profit
    Shrawan      Q1   922000      413000
     Bhadra      Q1  1471000      605000
     Ashwin      Q1   932000      360000
    
    Q1 and Q4 data:
       Month Quarter  Revenue
     Shrawan      Q1   922000
      Bhadra      Q1  1471000
      Ashwin      Q1   932000
    Baishakh      Q4  1936000
      Jestha      Q4  1713000
      Ashadh      Q4   975000


## Section 13: Sorting Data


```python
# Sort by a column
sorted_by_revenue = pl_df.sort_values('Revenue', ascending=False)
print('Months ranked by Revenue (highest first):')
print(sorted_by_revenue[['Month', 'Revenue', 'Net_Profit', 'Margin_Pct']].to_string(index=False))
```

    Months ranked by Revenue (highest first):
       Month  Revenue  Net_Profit  Margin_Pct
    Baishakh  1936000      789000       40.75
        Magh  1903000      622000       32.69
     Chaitra  1800000      671000       37.28
      Jestha  1713000      734000       42.85
       Poush  1532000      673000       43.93
      Bhadra  1471000      605000       41.13
      Kartik  1059000      403000       38.05
      Ashadh   975000      377000       38.67
      Falgun   937000      298000       31.80
      Ashwin   932000      360000       38.63
     Shrawan   922000      413000       44.79
     Mangsir   910000      329000       36.15



```python
# Create a transaction dataset for more realistic examples
transactions = pd.DataFrame({
    'Txn_ID':      ['T001','T002','T003','T004','T005','T006','T007','T008','T009','T010'],
    'Date':        ['05-Shrawan','12-Shrawan','18-Shrawan','25-Shrawan','02-Bhadra','08-Bhadra','15-Bhadra','22-Bhadra','28-Bhadra','03-Ashwin'],
    'Party':       ['Himalayan Traders Pvt. Ltd.','Annapurna Enterprises Pvt. Ltd.','Sagarmatha Trading Pvt. Ltd.','Himalayan Traders Pvt. Ltd.','Everest Imports Pvt. Ltd.','Annapurna Enterprises Pvt. Ltd.','Barahi Industries Ltd.','Sagarmatha Trading Pvt. Ltd.','Himalayan Traders Pvt. Ltd.','Everest Imports Pvt. Ltd.'],
    'Type':        ['Sale','Sale','Purchase','Sale','Sale','Sale','Purchase','Purchase','Sale','Sale'],
    'Amount':      [85000, 42000, 67000, 115000, 78000, 93000, 54000, 38000, 127000, 65000],
    'VAT_Rate': [13, 0, 13, 13, 0, 13, 13, 0, 13, 13],
    'Status':      ['Paid','Pending','Paid','Paid','Pending','Paid','Paid','Pending','Paid','Pending'],
})
transactions['VAT_Amount'] = (transactions['Amount'] * transactions['VAT_Rate'] / 100).round(2)
transactions['Total']      = transactions['Amount'] + transactions['VAT_Amount']

print(transactions.to_string(index=False))
```

    Txn_ID       Date                           Party     Type  Amount  VAT_Rate  Status  VAT_Amount    Total
      T001 05-Shrawan     Himalayan Traders Pvt. Ltd.     Sale   85000        13    Paid     11050.0  96050.0
      T002 12-Shrawan Annapurna Enterprises Pvt. Ltd.     Sale   42000         0 Pending         0.0  42000.0
      T003 18-Shrawan    Sagarmatha Trading Pvt. Ltd. Purchase   67000        13    Paid      8710.0  75710.0
      T004 25-Shrawan     Himalayan Traders Pvt. Ltd.     Sale  115000        13    Paid     14950.0 129950.0
      T005  02-Bhadra       Everest Imports Pvt. Ltd.     Sale   78000         0 Pending         0.0  78000.0
      T006  08-Bhadra Annapurna Enterprises Pvt. Ltd.     Sale   93000        13    Paid     12090.0 105090.0
      T007  15-Bhadra          Barahi Industries Ltd. Purchase   54000        13    Paid      7020.0  61020.0
      T008  22-Bhadra    Sagarmatha Trading Pvt. Ltd. Purchase   38000         0 Pending         0.0  38000.0
      T009  28-Bhadra     Himalayan Traders Pvt. Ltd.     Sale  127000        13    Paid     16510.0 143510.0
      T010  03-Ashwin       Everest Imports Pvt. Ltd.     Sale   65000        13 Pending      8450.0  73450.0


## Section 14: Adding Calculated Columns

Just like adding a formula column in Excel — but applied to the entire column instantly.


```python
# Add new computed columns
transactions['Effective_Rate'] = (transactions['VAT_Amount'] / transactions['Amount'] * 100).round(1)

# Conditional column using np.where() — like Excel IF()
transactions['Risk_Flag'] = np.where(transactions['Amount'] > 100000, 'High Value', 'Normal')

# Using apply() for complex logic — applies a function to each row/column
def classify_status(row):
    if row['Status'] == 'Pending' and row['Amount'] > 80000:
        return 'URGENT FOLLOW-UP'
    elif row['Status'] == 'Pending':
        return 'Follow-up'
    else:
        return 'Cleared'

transactions['Action'] = transactions.apply(classify_status, axis=1)

print(transactions[['Txn_ID', 'Party', 'Amount', 'Status', 'Risk_Flag', 'Action']].to_string(index=False))
```

    Txn_ID                           Party  Amount  Status  Risk_Flag    Action
      T001     Himalayan Traders Pvt. Ltd.   85000    Paid     Normal   Cleared
      T002 Annapurna Enterprises Pvt. Ltd.   42000 Pending     Normal Follow-up
      T003    Sagarmatha Trading Pvt. Ltd.   67000    Paid     Normal   Cleared
      T004     Himalayan Traders Pvt. Ltd.  115000    Paid High Value   Cleared
      T005       Everest Imports Pvt. Ltd.   78000 Pending     Normal Follow-up
      T006 Annapurna Enterprises Pvt. Ltd.   93000    Paid     Normal   Cleared
      T007          Barahi Industries Ltd.   54000    Paid     Normal   Cleared
      T008    Sagarmatha Trading Pvt. Ltd.   38000 Pending     Normal Follow-up
      T009     Himalayan Traders Pvt. Ltd.  127000    Paid High Value   Cleared
      T010       Everest Imports Pvt. Ltd.   65000 Pending     Normal Follow-up


## Section 15: GroupBy — Like a Pivot Table

`groupby()` is one of Pandas' most powerful features. It is the equivalent of Excel's **Pivot Table**.

**Concept:** Split the data into groups → Apply a function to each group → Combine results

Think: *"Total sales by party"*, *"Average invoice by GST rate"*, *"Count of pending vs paid"*


```python
# Group by Party — total business with each party
party_summary = transactions.groupby('Party')['Amount'].sum().sort_values(ascending=False)
print('Total Business by Party:')
print(party_summary)

print()
# Group by Type (Sale/Purchase) — net position
type_summary = transactions.groupby('Type')[['Amount', 'VAT_Amount', 'Total']].sum()
print('Summary by Transaction Type:')
print(type_summary)
```

    Total Business by Party:
    Party
    Himalayan Traders Pvt. Ltd.        327000
    Everest Imports Pvt. Ltd.          143000
    Annapurna Enterprises Pvt. Ltd.    135000
    Sagarmatha Trading Pvt. Ltd.       105000
    Barahi Industries Ltd.              54000
    Name: Amount, dtype: int64
    
    Summary by Transaction Type:
              Amount  VAT_Amount     Total
    Type                                  
    Purchase  159000     15730.0  174730.0
    Sale      605000     63050.0  668050.0



```python
# Multiple aggregations at once — like Excel Pivot Table with multiple Value fields
party_detail = transactions.groupby('Party').agg(
    Transaction_Count = ('Txn_ID', 'count'),
    Total_Amount      = ('Amount', 'sum'),
    Average_Amount    = ('Amount', 'mean'),
    Max_Transaction   = ('Amount', 'max'),
    Total_GST         = ('VAT_Amount', 'sum')
).round(2)

print('Detailed Party-wise Analysis:')
print(party_detail.to_string())
```

    Detailed Party-wise Analysis:
                                     Transaction_Count  Total_Amount  Average_Amount  Max_Transaction  Total_GST
    Party                                                                                                       
    Annapurna Enterprises Pvt. Ltd.                  2        135000         67500.0            93000    12090.0
    Barahi Industries Ltd.                           1         54000         54000.0            54000     7020.0
    Everest Imports Pvt. Ltd.                        2        143000         71500.0            78000     8450.0
    Himalayan Traders Pvt. Ltd.                      3        327000        109000.0           127000    42510.0
    Sagarmatha Trading Pvt. Ltd.                     2        105000         52500.0            67000     8710.0



```python
# GroupBy with pivot table — GST liability by rate and type
gst_pivot = transactions.pivot_table(
    values  = 'VAT_Amount',
    index   = 'VAT_Rate',
    columns = 'Type',
    aggfunc = 'sum',
    fill_value = 0
)

print('VAT Summary by Rate and Type:')
print(gst_pivot)
print()

# GST payable = Output GST (Sales) - Input GST (Purchases)
gst_pivot['Net_GST_Payable'] = gst_pivot.get('Sale', 0) - gst_pivot.get('Purchase', 0)
print('Net GST Payable:')
print(gst_pivot)
```

    VAT Summary by Rate and Type:
    Type      Purchase     Sale
    VAT_Rate                   
    0              0.0      0.0
    13         15730.0  63050.0
    
    Net GST Payable:
    Type      Purchase     Sale  Net_GST_Payable
    VAT_Rate                                    
    0              0.0      0.0              0.0
    13         15730.0  63050.0          47320.0



```python
# Monthly P&L grouped by Quarter — like a quarterly summary pivot table
quarterly = pl_df.groupby('Quarter').agg(
    Total_Revenue    = ('Revenue', 'sum'),
    Total_Expenses   = ('Opex', 'sum'),
    Total_Net_Profit = ('Net_Profit', 'sum'),
    Avg_Margin       = ('Margin_Pct', 'mean')
).round(2)

quarterly['Revenue_Share_%'] = (quarterly['Total_Revenue'] / quarterly['Total_Revenue'].sum() * 100).round(1)

print('Quarterly P&L Summary:')
print(quarterly.to_string())
print(f"\nFull Year Net Profit: NPR {quarterly['Total_Net_Profit'].sum():,.0f}")
```

    Quarterly P&L Summary:
             Total_Revenue  Total_Expenses  Total_Net_Profit  Avg_Margin  Revenue_Share_%
    Quarter                                                                              
    Q1             3325000          555000           1378000       41.52             20.7
    Q2             3501000          546000           1405000       39.38             21.8
    Q3             4640000          713000           1591000       33.92             28.8
    Q4             4624000          992000           1900000       40.76             28.7
    
    Full Year Net Profit: NPR 6,274,000


## Section 16: Handling Missing Values

Real-world financial data is almost always incomplete — missing values are a fact of life.  
Pandas uses `NaN` (Not a Number) to represent missing data.


```python
# Create a DataFrame with missing values (typical in imported data)
incomplete_data = pd.DataFrame({
    'Invoice_No': ['INV-001', 'INV-002', 'INV-003', 'INV-004', 'INV-005', 'INV-006'],
    'Party':      ['Alpha Ltd', None, 'Everest Imports Pvt. Ltd.', 'Delta Corp', None, 'Zeta Co'],
    'Amount':     [45000, 82000, None, 67000, 92000, None],
    'VAT_Rate':   [18, 12, 18, None, 5, 18],
    'Due_Date':   ['30-Apr', '15-May', None, '01-Jun', '10-May', '25-Jun'],
})

print('Raw data with missing values:')
print(incomplete_data)

print('\nMissing value count per column:')
print(incomplete_data.isnull().sum())

print('\nAny missing values?', incomplete_data.isnull().any().any())
```

    Raw data with missing values:
      Invoice_No                      Party   Amount  VAT_Rate Due_Date
    0    INV-001                  Alpha Ltd  45000.0      18.0   30-Apr
    1    INV-002                       None  82000.0      12.0   15-May
    2    INV-003  Everest Imports Pvt. Ltd.      NaN      18.0     None
    3    INV-004                 Delta Corp  67000.0       NaN   01-Jun
    4    INV-005                       None  92000.0       5.0   10-May
    5    INV-006                    Zeta Co      NaN      18.0   25-Jun
    
    Missing value count per column:
    Invoice_No    0
    Party         2
    Amount        2
    VAT_Rate      1
    Due_Date      1
    dtype: int64
    
    Any missing values? True



```python
# Strategies to handle missing values
df_clean = incomplete_data.copy()

# Strategy 1: Fill with a specific value
df_clean['Party']    = df_clean['Party'].fillna('UNKNOWN')
df_clean['VAT_Rate'] = df_clean['VAT_Rate'].fillna(13)  # Default to 13% (Nepal standard VAT)
df_clean['Due_Date'] = df_clean['Due_Date'].fillna('TBD')

# Strategy 2: Fill with the column average
df_clean['Amount']   = df_clean['Amount'].fillna(df_clean['Amount'].mean())

# Strategy 3: Drop rows with any remaining missing values
# df_clean = df_clean.dropna()   # Use this if you want to remove incomplete rows

print('After cleaning:')
print(df_clean)
print('\nMissing values remaining:', df_clean.isnull().sum().sum())
```

    After cleaning:
      Invoice_No                      Party   Amount  VAT_Rate Due_Date
    0    INV-001                  Alpha Ltd  45000.0      18.0   30-Apr
    1    INV-002                    UNKNOWN  82000.0      12.0   15-May
    2    INV-003  Everest Imports Pvt. Ltd.  71500.0      18.0      TBD
    3    INV-004                 Delta Corp  67000.0      13.0   01-Jun
    4    INV-005                    UNKNOWN  92000.0       5.0   10-May
    5    INV-006                    Zeta Co  71500.0      18.0   25-Jun
    
    Missing values remaining: 0


## Section 17: Merging DataFrames — Like VLOOKUP

**VLOOKUP** in Excel pulls data from one table into another using a matching key.  
In Pandas, `merge()` does the same — and handles millions of rows instantly.


```python
# Table 1: Invoice Register
invoices = pd.DataFrame({
    'Invoice_No':  ['INV-001', 'INV-002', 'INV-003', 'INV-004', 'INV-005'],
    'Client_ID':   ['C001', 'C003', 'C002', 'C001', 'C004'],
    'Amount':      [85000, 42000, 120000, 67000, 95000],
    'Date':        ['05-Shrawan', '08-Shrawan', '12-Shrawan', '18-Shrawan', '22-Shrawan'],
})

# Table 2: Client Master (like a lookup table)
clients = pd.DataFrame({
    'Client_ID':   ['C001', 'C002', 'C003', 'C004'],
    'Client_Name': ['Sunrise Manufacturing', 'Blue Ocean Pvt Ltd', 'Alpha Traders', 'Tech Solutions'],
    'City':        ['Kathmandu', 'Lalitpur', 'Pokhara', 'Kathmandu'],
    'VAT_Rate': [13, 0, 13, 13],  # 0% for exempt, 13% standard Nepal VAT
})

print('Invoice Table:')
print(invoices)
print('\nClient Master:')
print(clients)
```

    Invoice Table:
      Invoice_No Client_ID  Amount        Date
    0    INV-001      C001   85000  05-Shrawan
    1    INV-002      C003   42000  08-Shrawan
    2    INV-003      C002  120000  12-Shrawan
    3    INV-004      C001   67000  18-Shrawan
    4    INV-005      C004   95000  22-Shrawan
    
    Client Master:
      Client_ID            Client_Name       City  VAT_Rate
    0      C001  Sunrise Manufacturing  Kathmandu        13
    1      C002     Blue Ocean Pvt Ltd   Lalitpur         0
    2      C003          Alpha Traders    Pokhara        13
    3      C004         Tech Solutions  Kathmandu        13



```python
# MERGE — joins the two tables on Client_ID (like VLOOKUP using Client_ID)
# how='left' means: keep ALL rows from invoices, add matching data from clients
merged = invoices.merge(clients, on='Client_ID', how='left')

# Calculate GST using the rate from client master
merged['VAT_Amount'] = (merged['Amount'] * merged['VAT_Rate'] / 100).round(2)
merged['Total']      = merged['Amount'] + merged['VAT_Amount']

print('Enriched Invoice Register (after merge):')
print(merged[['Invoice_No', 'Client_Name', 'City', 'Amount', 'VAT_Rate', 'VAT_Amount', 'Total']].to_string(index=False))
```

    Enriched Invoice Register (after merge):
    Invoice_No           Client_Name      City  Amount  VAT_Rate  VAT_Amount    Total
       INV-001 Sunrise Manufacturing Kathmandu   85000        13     11050.0  96050.0
       INV-002         Alpha Traders   Pokhara   42000        13      5460.0  47460.0
       INV-003    Blue Ocean Pvt Ltd  Lalitpur  120000         0         0.0 120000.0
       INV-004 Sunrise Manufacturing Kathmandu   67000        13      8710.0  75710.0
       INV-005        Tech Solutions Kathmandu   95000        13     12350.0 107350.0


## Section 18: Reading & Writing Excel / CSV Files

In practice, you will almost always **import data from Excel or CSV** rather than typing it manually.  
Pandas makes this effortless.


```python
# First, let's save our DataFrame to files

# Save as CSV
pl_df.to_csv('pl_data.csv', index=False)      # index=False prevents writing row numbers
print('Saved pl_data.csv')

# Save as Excel (requires openpyxl: pip install openpyxl)
pl_df.to_excel('pl_data.xlsx', sheet_name='P&L', index=False)
print('Saved pl_data.xlsx')

# Save multiple sheets in one Excel file
with pd.ExcelWriter('financial_report.xlsx', engine='openpyxl') as writer:
    pl_df.to_excel(writer, sheet_name='Monthly P&L', index=False)
    transactions.to_excel(writer, sheet_name='Transactions', index=False)
    quarterly.to_excel(writer, sheet_name='Quarterly Summary')
print('Saved financial_report.xlsx (3 sheets)')
```

    Saved pl_data.csv
    Saved pl_data.xlsx
    Saved financial_report.xlsx (3 sheets)



```python
# Reading back the files

# Read CSV
df_from_csv = pd.read_csv('pl_data.csv')
print('Read from CSV — shape:', df_from_csv.shape)
print(df_from_csv.head(3))

# Read Excel
df_from_excel = pd.read_excel('pl_data.xlsx', sheet_name='P&L')
print('\nRead from Excel — shape:', df_from_excel.shape)
```

    Read from CSV — shape: (12, 8)
         Month Quarter  Revenue    COGS  Gross_Profit    Opex  Net_Profit  \
    0  Shrawan      Q1   922000  349000        573000  160000      413000   
    1   Bhadra      Q1  1471000  706000        765000  160000      605000   
    2   Ashwin      Q1   932000  337000        595000  235000      360000   
    
       Margin_Pct  
    0       44.79  
    1       41.13  
    2       38.63  
    
    Read from Excel — shape: (12, 8)



```python
# Common read_csv / read_excel options you'll use in practice

# Skip first 2 rows (e.g., if Excel has a title in row 1)
# df = pd.read_csv('file.csv', skiprows=2)

# Read only specific columns
# df = pd.read_csv('file.csv', usecols=['Date', 'Amount', 'Party'])

# Parse date columns automatically
# df = pd.read_csv('file.csv', parse_dates=['Date'])

# Handle encoding issues (common with Indian data files)
# df = pd.read_csv('file.csv', encoding='latin-1')

print('Common read options demonstrated above (commented out).')
print('Uncomment and adapt for your actual files.')
```

    Common read options demonstrated above (commented out).
    Uncomment and adapt for your actual files.


## Section 19: String Operations on Columns

Pandas has powerful text processing via `.str` accessor — extremely useful for cleaning imported data.


```python
# Simulating messy imported data (very common in practice)
raw_data = pd.DataFrame({
    'Party_Name': ['  ALPHA LTD  ', 'beta corp', 'GAMMA INC.', '  Delta Pvt Ltd', 'ZETA CO'],
    'PAN':        ['aaact0001a', 'BBBBB0002B', 'ccccc0003c', 'DDDDD0004d', 'eeeee0005E'],
    'City':       ['KATHMANDU', 'lalitpur', 'Pokhara', 'BIRATNAGAR', 'Biratnagar'],
    'Amount_str': ['NPR 45,000', 'NPR 82,000', 'NPR 1,20,000', 'NPR 67,500', 'NPR 95,000'],  # Amount as text!
})

print('Raw (messy) data:')
print(raw_data)
print()

# Clean it up using .str accessor
raw_data['Party_Name'] = raw_data['Party_Name'].str.strip().str.title()    # Remove spaces, proper case
raw_data['PAN']        = raw_data['PAN'].str.upper()                        # PAN must be uppercase
raw_data['City']       = raw_data['City'].str.title()                       # Proper case

# Convert amount string to number
raw_data['Amount'] = raw_data['Amount_str'].str.replace('NPR ', '').str.replace(',', '').astype(int)
raw_data = raw_data.drop('Amount_str', axis=1)   # Remove old column

print('Cleaned data:')
print(raw_data)
```

    Raw (messy) data:
            Party_Name         PAN        City    Amount_str
    0      ALPHA LTD    aaact0001a   KATHMANDU    NPR 45,000
    1        beta corp  BBBBB0002B    lalitpur    NPR 82,000
    2       GAMMA INC.  ccccc0003c     Pokhara  NPR 1,20,000
    3    Delta Pvt Ltd  DDDDD0004d  BIRATNAGAR    NPR 67,500
    4          ZETA CO  eeeee0005E  Biratnagar    NPR 95,000
    
    Cleaned data:
          Party_Name         PAN        City  Amount
    0      Alpha Ltd  AAACT0001A   Kathmandu   45000
    1      Beta Corp  BBBBB0002B    Lalitpur   82000
    2     Gamma Inc.  CCCCC0003C     Pokhara  120000
    3  Delta Pvt Ltd  DDDDD0004D  Biratnagar   67500
    4        Zeta Co  EEEEE0005E  Biratnagar   95000



```python
# More string operations useful in audit/finance
parties = pd.Series(['Nepal Telecom (NTC)', 'Nabil Bank Ltd.',
                     'CG Corp Global', 'Yomari Digital Services', 'Nepal Life Insurance Co. Ltd.'])

# Check if string contains something
print('Contains "Ltd":')
print(parties[parties.str.contains('Ltd', case=False)])

# Extract first word (could be group name)
print('\nFirst word of each name:')
print(parties.str.split().str[0].tolist())

# Count characters
print('\nName lengths:', parties.str.len().tolist())
```

    Contains "Ltd":
    1                  Nabil Bank Ltd.
    4    Nepal Life Insurance Co. Ltd.
    dtype: object
    
    First word of each name:
    ['Nepal', 'Nabil', 'CG', 'Yomari', 'Nepal']
    
    Name lengths: [19, 15, 14, 23, 29]


## Section 20: Practice Exercises

---

#### 🏋️ Exercise 1 — GST VAT-401 Summary

You have an invoice register. Create a VAT-401 style summary showing:
- Total taxable value, VAT, VAT_Local, and total invoice value by GST rate slab
- The top 3 clients by invoice value
- All pending (unpaid) invoices over NPR 50,000


```python
import pandas as pd
import numpy as np

invoice_register = pd.DataFrame({
    'Invoice_No': ['INV-001','INV-002','INV-003','INV-004','INV-005',
                   'INV-006','INV-007','INV-008','INV-009','INV-010'],
    'Client':     ['Alpha Ltd','Beta Corp','Alpha Ltd','Everest Imports Pvt. Ltd.','Delta Pvt',
                   'Beta Corp','Everest Imports Pvt. Ltd.','Alpha Ltd','Delta Pvt','Beta Corp'],
    'Date':       ['05-Shrawan','08-Shrawan','12-Shrawan','15-Shrawan','18-Shrawan',
                   '22-Shrawan','25-Shrawan','28-Shrawan','01-Bhadra','05-Bhadra'],
    'Taxable_Value': [85000, 42000, 120000, 67000, 95000,
                      55000, 145000, 38000, 82000, 110000],
    'VAT_Rate': [13, 0, 13, 13, 0, 13, 13, 0, 13, 13],
    'Status':     ['Paid','Pending','Paid','Paid','Pending',
                   'Paid','Pending','Paid','Paid','Pending'],
})

# Write your VAT-401 analysis here


```

#### 🏋️ Exercise 2 — Trial Balance Validation

A trial balance should always balance: **Total Debits = Total Credits**.

From the data below:
1. Check if the trial balance is balanced
2. Identify accounts with unusually high balances (> NPR 10 lakhs)
3. Summarise totals by account type (Assets, Liabilities, Income, Expenses)
4. Export a clean formatted Excel file named `trial_balance_clean.xlsx`


```python
import pandas as pd

trial_balance = pd.DataFrame({
    'Account':  ['Cash & Bank','Trade Debtors','Inventory','Fixed Assets',
                 'Trade Creditors','Loans Payable','Share Capital','Retained Earnings',
                 'Sales Revenue','Other Income','COGS','Salaries','Rent','Depreciation','Finance Cost'],
    'Type':     ['Asset','Asset','Asset','Asset',
                 'Liability','Liability','Liability','Liability',
                 'Income','Income','Expense','Expense','Expense','Expense','Expense'],
    'Debit':    [485000, 1250000, 2100000, 8500000,
                 0, 0, 0, 0,
                 0, 0, 1800000, 960000, 420000, 240000, 150000],
    'Credit':   [0, 0, 0, 0,
                 980000, 2500000, 5000000, 650000,
                 5200000, 325000, 0, 0, 0, 0, 0],
})

# Write your trial balance analysis here


```

---
### 💡 Solutions


```python
# SOLUTION — Exercise 1: VAT-401 Summary
import pandas as pd
import numpy as np

invoice_register = pd.DataFrame({
    'Invoice_No':    ['INV-001','INV-002','INV-003','INV-004','INV-005',
                      'INV-006','INV-007','INV-008','INV-009','INV-010'],
    'Client':        ['Alpha Ltd','Beta Corp','Alpha Ltd','Everest Imports Pvt. Ltd.','Delta Pvt',
                      'Beta Corp','Everest Imports Pvt. Ltd.','Alpha Ltd','Delta Pvt','Beta Corp'],
    'Taxable_Value': [85000, 42000, 120000, 67000, 95000, 55000, 145000, 38000, 82000, 110000],
    'VAT_Rate': [13, 0, 13, 13, 0, 13, 13, 0, 13, 13],
    'Status':        ['Paid','Pending','Paid','Paid','Pending','Paid','Pending','Paid','Paid','Pending'],
})

invoice_register['VAT_Amount'] = invoice_register['Taxable_Value'] * invoice_register['VAT_Rate'] / 100
invoice_register['VAT']       = invoice_register['VAT_Amount'] / 2
invoice_register['VAT_Local']       = invoice_register['VAT_Amount'] / 2
invoice_register['Total']      = invoice_register['Taxable_Value'] + invoice_register['VAT_Amount']

# VAT-401 by rate
gstr1 = invoice_register.groupby('VAT_Rate').agg(
    Taxable_Value = ('Taxable_Value','sum'),
    VAT          = ('VAT','sum'),
    VAT_Local          = ('VAT_Local','sum'),
    Total         = ('Total','sum')
)
print('VAT-401 Summary by VAT Rate:')
print(gstr1)

# Top 3 clients
print('\nTop 3 Clients by Invoice Value:')
print(invoice_register.groupby('Client')['Total'].sum().nlargest(3))

# Pending over NPR 50K
print('\nPending Invoices > NPR 50,000:')
pending = invoice_register[(invoice_register['Status']=='Pending') & (invoice_register['Taxable_Value']>50000)]
print(pending[['Invoice_No','Client','Taxable_Value','Status']].to_string(index=False))
```

    VAT-401 Summary by VAT Rate:
              Taxable_Value      VAT  VAT_Local     Total
    VAT_Rate                                             
    0                175000      0.0        0.0  175000.0
    13               664000  43160.0    43160.0  750320.0
    
    Top 3 Clients by Invoice Value:
    Client
    Alpha Ltd                    269650.0
    Everest Imports Pvt. Ltd.    239560.0
    Beta Corp                    228450.0
    Name: Total, dtype: float64
    
    Pending Invoices > NPR 50,000:
    Invoice_No                    Client  Taxable_Value  Status
       INV-005                 Delta Pvt          95000 Pending
       INV-007 Everest Imports Pvt. Ltd.         145000 Pending
       INV-010                 Beta Corp         110000 Pending



```python
# SOLUTION — Exercise 2: Trial Balance Validation
import pandas as pd

trial_balance = pd.DataFrame({
    'Account':  ['Cash & Bank','Trade Debtors','Inventory','Fixed Assets',
                 'Trade Creditors','Loans Payable','Share Capital','Retained Earnings',
                 'Sales Revenue','Other Income','COGS','Salaries','Rent','Depreciation','Finance Cost'],
    'Type':     ['Asset','Asset','Asset','Asset','Liability','Liability','Liability','Liability',
                 'Income','Income','Expense','Expense','Expense','Expense','Expense'],
    'Debit':    [485000,1250000,2100000,8500000,0,0,0,0,0,0,1800000,960000,420000,240000,150000],
    'Credit':   [0,0,0,0,980000,2500000,5000000,650000,5200000,325000,0,0,0,0,0],
})

trial_balance['Balance'] = trial_balance['Debit'] - trial_balance['Credit']

# Check balance
total_debit  = trial_balance['Debit'].sum()
total_credit = trial_balance['Credit'].sum()
print(f'Total Debits:  NPR {total_debit:>12,}')
print(f'Total Credits: NPR {total_credit:>12,}')
print(f'Difference:    NPR {total_debit - total_credit:>12,}')
print('Balanced?', 'YES ✓' if total_debit == total_credit else 'NO ✗ — Check data!')

# High balance accounts
print('\nAccounts with Balance > NPR 10 Lakhs:')
high_bal = trial_balance[abs(trial_balance['Balance']) > 1000000]
print(high_bal[['Account', 'Type', 'Debit', 'Credit', 'Balance']].to_string(index=False))

# By type
print('\nSummary by Account Type:')
type_summary = trial_balance.groupby('Type')[['Debit','Credit']].sum()
print(type_summary)

# Export
trial_balance.to_excel('trial_balance_clean.xlsx', index=False)
print('\nExported to trial_balance_clean.xlsx')
```

    Total Debits:  NPR   15,905,000
    Total Credits: NPR   14,655,000
    Difference:    NPR    1,250,000
    Balanced? NO ✗ — Check data!
    
    Accounts with Balance > NPR 10 Lakhs:
          Account      Type   Debit  Credit  Balance
    Trade Debtors     Asset 1250000       0  1250000
        Inventory     Asset 2100000       0  2100000
     Fixed Assets     Asset 8500000       0  8500000
    Loans Payable Liability       0 2500000 -2500000
    Share Capital Liability       0 5000000 -5000000
    Sales Revenue    Income       0 5200000 -5200000
             COGS   Expense 1800000       0  1800000
    
    Summary by Account Type:
                  Debit   Credit
    Type                        
    Asset      12335000        0
    Expense     3570000        0
    Income            0  5525000
    Liability         0  9130000
    
    Exported to trial_balance_clean.xlsx


---
## 🎉 Module 3 Complete!

### What you've learned
| Concept | Real-world Use |
|---------|----------------|
| Series & DataFrame | Working with financial tables |
| Exploring data | Understanding imported files quickly |
| Filtering | Transaction sampling, audit selection |
| GroupBy | VAT-401, party-wise summary, P&L by segment |
| Pivot tables | Quarterly dashboards |
| Missing values | Cleaning imported data |
| Merge | VLOOKUP replacement |
| Read/Write Excel | Real workflow automation |
| String operations | Data standardisation |

**Next up → Module 4: Matplotlib** — Visualise all this data with professional charts!

---
*Python for CA Professionals — Module 3: Pandas*
