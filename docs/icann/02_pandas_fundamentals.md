# Module 2: Pandas Fundamentals for Accountants
### Data Science for Chartered Accountants

---

## Learning Objectives
- Create DataFrames from financial data (CSV, dict, Excel)
- Filter, sort, and slice transaction data
- Use `groupby` for account-wise and period-wise summaries
- Merge DataFrames — the Python equivalent of VLOOKUP
- Create pivot tables for MIS reports
- Work with dates for aging and period analysis

---

> **CA Context:** Pandas is your digital accounts register. A DataFrame is like a tally ledger — rows are entries, columns are fields (date, party, amount, narration). Every operation you do in Tally or Excel can be replicated — and automated — in Pandas.


```python
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 120)
pd.set_option('display.float_format', '{:,.2f}'.format)
print('Pandas version:', pd.__version__)
```

    Pandas version: 2.3.2


---
## Section 1: Creating DataFrames

A **DataFrame** is a table — rows are observations, columns are attributes. Think of it as a sheet in Excel with superpowers.


```python
# ── 1.1 Ledger Entries from a Dictionary ─────────────────────────────────────
ledger_data = {
    'Date'      : pd.to_datetime(['2024-04-01','2024-04-03','2024-04-05','2024-04-07',
                                   '2024-04-10','2024-04-12','2024-04-15','2024-04-18',
                                   '2024-04-20','2024-04-22','2024-04-25','2024-04-28']),
    'Voucher_No': ['JV-001','PV-001','RV-001','PV-002','JV-002','RV-002',
                   'PV-003','JV-003','RV-003','PV-004','JV-004','RV-004'],
    'Party'     : ['ABC Ltd','Rent A/C','XYZ Traders','Salary A/C','DEF Corp',
                   'PQR Ltd','Office Exp','MNO Ltd','RST Co','Electric A/C',
                   'GHI Ltd','UVW Traders'],
    'Voucher_Type': ['Journal','Payment','Receipt','Payment','Journal','Receipt',
                     'Payment','Journal','Receipt','Payment','Journal','Receipt'],
    'Account_Head' : ['Sales','Rent','Sales','Salaries','Purchases','Sales',
                      'Office Exp','Purchases','Sales','Utilities','Purchases','Sales'],
    'Debit'     : [0,45000,0,1_20_000,3_50_000,0,18_500,2_80_000,0,8_500,1_95_000,0],
    'Credit'    : [5_25_000,0,3_10_000,0,0,2_80_000,0,0,4_15_000,0,0,1_95_000]
}

df_ledger = pd.DataFrame(ledger_data)
print('Shape:', df_ledger.shape, ' — (rows, columns)')
df_ledger
```

    Shape: (12, 7)  — (rows, columns)





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
      <th>Voucher_No</th>
      <th>Party</th>
      <th>Voucher_Type</th>
      <th>Account_Head</th>
      <th>Debit</th>
      <th>Credit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2024-04-01</td>
      <td>JV-001</td>
      <td>ABC Ltd</td>
      <td>Journal</td>
      <td>Sales</td>
      <td>0</td>
      <td>525000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2024-04-03</td>
      <td>PV-001</td>
      <td>Rent A/C</td>
      <td>Payment</td>
      <td>Rent</td>
      <td>45000</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2024-04-05</td>
      <td>RV-001</td>
      <td>XYZ Traders</td>
      <td>Receipt</td>
      <td>Sales</td>
      <td>0</td>
      <td>310000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2024-04-07</td>
      <td>PV-002</td>
      <td>Salary A/C</td>
      <td>Payment</td>
      <td>Salaries</td>
      <td>120000</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2024-04-10</td>
      <td>JV-002</td>
      <td>DEF Corp</td>
      <td>Journal</td>
      <td>Purchases</td>
      <td>350000</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2024-04-12</td>
      <td>RV-002</td>
      <td>PQR Ltd</td>
      <td>Receipt</td>
      <td>Sales</td>
      <td>0</td>
      <td>280000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2024-04-15</td>
      <td>PV-003</td>
      <td>Office Exp</td>
      <td>Payment</td>
      <td>Office Exp</td>
      <td>18500</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2024-04-18</td>
      <td>JV-003</td>
      <td>MNO Ltd</td>
      <td>Journal</td>
      <td>Purchases</td>
      <td>280000</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2024-04-20</td>
      <td>RV-003</td>
      <td>RST Co</td>
      <td>Receipt</td>
      <td>Sales</td>
      <td>0</td>
      <td>415000</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2024-04-22</td>
      <td>PV-004</td>
      <td>Electric A/C</td>
      <td>Payment</td>
      <td>Utilities</td>
      <td>8500</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2024-04-25</td>
      <td>JV-004</td>
      <td>GHI Ltd</td>
      <td>Journal</td>
      <td>Purchases</td>
      <td>195000</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2024-04-28</td>
      <td>RV-004</td>
      <td>UVW Traders</td>
      <td>Receipt</td>
      <td>Sales</td>
      <td>0</td>
      <td>195000</td>
    </tr>
  </tbody>
</table>
</div>




```python
# ── 1.2 Data Types & Summary ──────────────────────────────────────────────────
print('Column Data Types:')
print(df_ledger.dtypes)
print('\nNumerical Summary:')
df_ledger[['Debit','Credit']].describe().apply(lambda x: x.map('{:,.0f}'.format))
```

    Column Data Types:
    Date            datetime64[ns]
    Voucher_No              object
    Party                   object
    Voucher_Type            object
    Account_Head            object
    Debit                    int64
    Credit                   int64
    dtype: object
    
    Numerical Summary:





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
      <th>Debit</th>
      <th>Credit</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>12</td>
      <td>12</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>84,750</td>
      <td>143,750</td>
    </tr>
    <tr>
      <th>std</th>
      <td>124,160</td>
      <td>193,627</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>13,500</td>
      <td>0</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>138,750</td>
      <td>287,500</td>
    </tr>
    <tr>
      <th>max</th>
      <td>350,000</td>
      <td>525,000</td>
    </tr>
  </tbody>
</table>
</div>



---
## Section 2: Selecting & Filtering Data

| Task | Excel | Pandas |
|---|---|---|
| Select a column | Click column header | `df['Column']` |
| Filter rows | AutoFilter | Boolean indexing |
| Select row by index | Click row | `df.iloc[n]` or `df.loc[label]` |


```python
# ── 2.1 Select Columns ────────────────────────────────────────────────────────
print('--- Receipt Vouchers only ---')
receipts = df_ledger[df_ledger['Voucher_Type'] == 'Receipt']
print(receipts[['Date','Voucher_No','Party','Credit']])

print('\n--- Payments > ₹1 Lakh ---')
large_payments = df_ledger[(df_ledger['Voucher_Type'] == 'Payment') & (df_ledger['Debit'] > 1_00_000)]
print(large_payments[['Date','Voucher_No','Party','Account_Head','Debit']])
```

    --- Receipt Vouchers only ---
             Date Voucher_No        Party  Credit
    2  2024-04-05     RV-001  XYZ Traders  310000
    5  2024-04-12     RV-002      PQR Ltd  280000
    8  2024-04-20     RV-003       RST Co  415000
    11 2024-04-28     RV-004  UVW Traders  195000
    
    --- Payments > ₹1 Lakh ---
            Date Voucher_No       Party Account_Head   Debit
    3 2024-04-07     PV-002  Salary A/C     Salaries  120000



```python
# ── 2.2 Filtering by Date Range (useful for period-wise analysis) ─────────────
# Transactions in first 15 days
first_half = df_ledger[df_ledger['Date'] <= '2024-04-15']
print(f'Transactions in Apr 1-15: {len(first_half)}')

# Using .between() for date ranges
q1_data = df_ledger[df_ledger['Date'].between('2024-04-01', '2024-04-20')]
print(f'Transactions Apr 1-20   : {len(q1_data)}')

# ── 2.3 Filter with .isin() — useful for party/account filtering ──────────────
selected_parties = ['ABC Ltd', 'DEF Corp', 'GHI Ltd']
party_data = df_ledger[df_ledger['Party'].isin(selected_parties)]
print(f'\nEntries for selected parties: {len(party_data)}')
print(party_data[['Date','Party','Voucher_Type','Debit','Credit']])
```

    Transactions in Apr 1-15: 7
    Transactions Apr 1-20   : 9
    
    Entries for selected parties: 3
             Date     Party Voucher_Type   Debit  Credit
    0  2024-04-01   ABC Ltd      Journal       0  525000
    4  2024-04-10  DEF Corp      Journal  350000       0
    10 2024-04-25   GHI Ltd      Journal  195000       0



```python
# ── 2.4 Derived Columns ───────────────────────────────────────────────────────
df_ledger['Amount']   = df_ledger['Debit'] + df_ledger['Credit']  # net amount
df_ledger['Month']    = df_ledger['Date'].dt.strftime('%b %Y')
df_ledger['Day_Name'] = df_ledger['Date'].dt.day_name()
df_ledger['Is_Weekend'] = df_ledger['Date'].dt.dayofweek >= 5  # Sat=5, Sun=6

print('Ledger with derived columns:')
df_ledger[['Date','Voucher_No','Party','Amount','Month','Day_Name','Is_Weekend']].head(8)
```

    Ledger with derived columns:





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
      <th>Voucher_No</th>
      <th>Party</th>
      <th>Amount</th>
      <th>Month</th>
      <th>Day_Name</th>
      <th>Is_Weekend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2024-04-01</td>
      <td>JV-001</td>
      <td>ABC Ltd</td>
      <td>525000</td>
      <td>Apr 2024</td>
      <td>Monday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2024-04-03</td>
      <td>PV-001</td>
      <td>Rent A/C</td>
      <td>45000</td>
      <td>Apr 2024</td>
      <td>Wednesday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2024-04-05</td>
      <td>RV-001</td>
      <td>XYZ Traders</td>
      <td>310000</td>
      <td>Apr 2024</td>
      <td>Friday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2024-04-07</td>
      <td>PV-002</td>
      <td>Salary A/C</td>
      <td>120000</td>
      <td>Apr 2024</td>
      <td>Sunday</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2024-04-10</td>
      <td>JV-002</td>
      <td>DEF Corp</td>
      <td>350000</td>
      <td>Apr 2024</td>
      <td>Wednesday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2024-04-12</td>
      <td>RV-002</td>
      <td>PQR Ltd</td>
      <td>280000</td>
      <td>Apr 2024</td>
      <td>Friday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2024-04-15</td>
      <td>PV-003</td>
      <td>Office Exp</td>
      <td>18500</td>
      <td>Apr 2024</td>
      <td>Monday</td>
      <td>False</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2024-04-18</td>
      <td>JV-003</td>
      <td>MNO Ltd</td>
      <td>280000</td>
      <td>Apr 2024</td>
      <td>Thursday</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
</div>



---
## Section 3: GroupBy — Account-wise & Period-wise Summaries

**`groupby`** is like a Tally Summary report — it groups data and computes aggregates per group.

> It's the Python equivalent of Excel's **SUMIF** or **Pivot Table** but far more powerful.


```python
# ── 3.1 Account Head-wise Summary ─────────────────────────────────────────────
acct_summary = df_ledger.groupby('Account_Head').agg(
    Total_Debit  = ('Debit',  'sum'),
    Total_Credit = ('Credit', 'sum'),
    Transactions = ('Voucher_No', 'count')
).reset_index()

acct_summary['Net_Balance'] = acct_summary['Total_Credit'] - acct_summary['Total_Debit']
acct_summary = acct_summary.sort_values('Net_Balance', ascending=False)
print('Account Head Summary:')
print(acct_summary.to_string(index=False))
```

    Account Head Summary:
    Account_Head  Total_Debit  Total_Credit  Transactions  Net_Balance
           Sales            0       1725000             5      1725000
       Utilities         8500             0             1        -8500
      Office Exp        18500             0             1       -18500
            Rent        45000             0             1       -45000
        Salaries       120000             0             1      -120000
       Purchases       825000             0             3      -825000



```python
# ── 3.2 Voucher-Type wise Analysis ────────────────────────────────────────────
voucher_summary = df_ledger.groupby('Voucher_Type').agg(
    Count   = ('Amount', 'count'),
    Total   = ('Amount', 'sum'),
    Average = ('Amount', 'mean'),
    Maximum = ('Amount', 'max')
).round(0)

print('Voucher Type Summary:')
print(voucher_summary)

# ── 3.3 Party-wise Outstanding ────────────────────────────────────────────────
party_bal = df_ledger.groupby('Party').agg(
    Debit_Total  = ('Debit',  'sum'),
    Credit_Total = ('Credit', 'sum')
)
party_bal['Net'] = party_bal['Credit_Total'] - party_bal['Debit_Total']
print('\nParty-wise Net Position (positive = receivable, negative = payable):')
print(party_bal[party_bal['Net'] != 0].sort_values('Net', ascending=False))
```

    Voucher Type Summary:
                  Count    Total    Average  Maximum
    Voucher_Type                                    
    Journal           4  1350000 337,500.00   525000
    Payment           4   192000  48,000.00   120000
    Receipt           4  1200000 300,000.00   415000
    
    Party-wise Net Position (positive = receivable, negative = payable):
                  Debit_Total  Credit_Total     Net
    Party                                          
    ABC Ltd                 0        525000  525000
    RST Co                  0        415000  415000
    XYZ Traders             0        310000  310000
    PQR Ltd                 0        280000  280000
    UVW Traders             0        195000  195000
    Electric A/C         8500             0   -8500
    Office Exp          18500             0  -18500
    Rent A/C            45000             0  -45000
    Salary A/C         120000             0 -120000
    GHI Ltd            195000             0 -195000
    MNO Ltd            280000             0 -280000
    DEF Corp           350000             0 -350000


---
## Section 4: Merging DataFrames — Python's VLOOKUP

| Merge Type | Excel Equivalent | Use Case |
|---|---|---|
| `inner` | VLOOKUP (exact match) | Matched records only |
| `left` | VLOOKUP with IFERROR | All from left, match if found |
| `outer` | Full join | All records, NaN for no match |

> **CA Use-Case:** Match purchase invoices with GRN (Goods Receipt Notes), or match GSTR-2A with purchase register.


```python
# ── 4.1 Vendor Master ────────────────────────────────────────────────────────
vendor_master = pd.DataFrame({
    'Party'     : ['ABC Ltd','XYZ Traders','DEF Corp','PQR Ltd','MNO Ltd','RST Co',
                   'GHI Ltd','UVW Traders','New Vendor'],
    'PAN'       : ['AAAA1234A','BBBB5678B','CCCC9012C','DDDD3456D','EEEE7890E',
                   'FFFF1234F','GGGG5678G','HHHH9012H','IIII3456I'],
    'GSTIN'     : ['29AAAA1234A1Z5','29BBBB5678B1Z5','29CCCC9012C1Z5','29DDDD3456D1Z5',
                   '29EEEE7890E1Z5','29FFFF1234F1Z5','29GGGG5678G1Z5','29HHHH9012H1Z5',
                   '29IIII3456I1Z5'],
    'Category'  : ['Customer','Customer','Supplier','Customer','Supplier','Customer',
                   'Supplier','Customer','Supplier'],
    'Credit_Days': [30, 45, 30, 60, 45, 30, 30, 45, 30]
})

# ── 4.2 Merge ledger with vendor master ──────────────────────────────────────
df_merged = df_ledger.merge(vendor_master[['Party','PAN','GSTIN','Category','Credit_Days']],
                             on='Party', how='left')
print(f'Matched records: {df_merged["PAN"].notna().sum()} / {len(df_merged)}')
print('\nEnriched Ledger:')
df_merged[['Date','Party','Voucher_Type','Amount','Category','Credit_Days','GSTIN']].head(8)
```

    Matched records: 8 / 12
    
    Enriched Ledger:





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
      <th>Party</th>
      <th>Voucher_Type</th>
      <th>Amount</th>
      <th>Category</th>
      <th>Credit_Days</th>
      <th>GSTIN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2024-04-01</td>
      <td>ABC Ltd</td>
      <td>Journal</td>
      <td>525000</td>
      <td>Customer</td>
      <td>30.00</td>
      <td>29AAAA1234A1Z5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2024-04-03</td>
      <td>Rent A/C</td>
      <td>Payment</td>
      <td>45000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2024-04-05</td>
      <td>XYZ Traders</td>
      <td>Receipt</td>
      <td>310000</td>
      <td>Customer</td>
      <td>45.00</td>
      <td>29BBBB5678B1Z5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2024-04-07</td>
      <td>Salary A/C</td>
      <td>Payment</td>
      <td>120000</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2024-04-10</td>
      <td>DEF Corp</td>
      <td>Journal</td>
      <td>350000</td>
      <td>Supplier</td>
      <td>30.00</td>
      <td>29CCCC9012C1Z5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2024-04-12</td>
      <td>PQR Ltd</td>
      <td>Receipt</td>
      <td>280000</td>
      <td>Customer</td>
      <td>60.00</td>
      <td>29DDDD3456D1Z5</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2024-04-15</td>
      <td>Office Exp</td>
      <td>Payment</td>
      <td>18500</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2024-04-18</td>
      <td>MNO Ltd</td>
      <td>Journal</td>
      <td>280000</td>
      <td>Supplier</td>
      <td>45.00</td>
      <td>29EEEE7890E1Z5</td>
    </tr>
  </tbody>
</table>
</div>




```python
# ── 4.3 Identifying Unmatched Records ──────────────────────────────────────────
unmatched = df_merged[df_merged['PAN'].isna()]
if not unmatched.empty:
    print('WARNING: These entries have no vendor master record:')
    print(unmatched[['Date','Party','Voucher_Type','Amount']])
else:
    print('All entries matched to vendor master.')

# ── 4.4 Find vendors in master but not in ledger (inactive vendors) ───────────
active_parties = set(df_ledger['Party'].unique())
master_parties = set(vendor_master['Party'].unique())
inactive = master_parties - active_parties
print(f'\nVendors in master but no transactions this month: {inactive}')
```

    WARNING: These entries have no vendor master record:
            Date         Party Voucher_Type  Amount
    1 2024-04-03      Rent A/C      Payment   45000
    3 2024-04-07    Salary A/C      Payment  120000
    6 2024-04-15    Office Exp      Payment   18500
    9 2024-04-22  Electric A/C      Payment    8500
    
    Vendors in master but no transactions this month: {'New Vendor'}


---
## Section 5: Pivot Tables for MIS Reports

Pandas `pivot_table` replicates Excel's Pivot Table — essential for generating MIS reports from raw transaction data.


```python
# ── 5.1 Generate a larger dataset for meaningful pivoting ─────────────────────
np.random.seed(10)
n = 200
departments = ['Sales', 'Operations', 'Finance', 'HR', 'IT']
expense_types = ['Travel', 'Printing', 'Communication', 'Repairs', 'Misc']
quarters = ['Q1', 'Q1', 'Q1', 'Q2', 'Q2', 'Q2', 'Q3', 'Q3', 'Q3', 'Q4', 'Q4', 'Q4']
months_list = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']

expense_df = pd.DataFrame({
    'Month'      : np.random.choice(months_list, n),
    'Quarter'    : np.random.choice(['Q1','Q2','Q3','Q4'], n),
    'Department' : np.random.choice(departments, n),
    'Expense_Type': np.random.choice(expense_types, n),
    'Amount'     : np.random.randint(5000, 80000, n)
})

# ── 5.2 Pivot: Department × Quarter ─────────────────────────────────────────
dept_quarter_pivot = pd.pivot_table(
    expense_df,
    values='Amount',
    index='Department',
    columns='Quarter',
    aggfunc='sum',
    margins=True,         # adds row and column totals (like Grand Total in Excel)
    margins_name='Total',
    fill_value=0
)
print('Expense Report — Department × Quarter (₹)')
dept_quarter_pivot.applymap(lambda x: f'{x:,.0f}')
```

    Expense Report — Department × Quarter (₹)


    /var/folders/kp/mytrwq8157q9s1tmw7r79fkm0000gn/T/ipykernel_83488/3600192578.py:29: FutureWarning: DataFrame.applymap has been deprecated. Use DataFrame.map instead.
      dept_quarter_pivot.applymap(lambda x: f'{x:,.0f}')





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
      <th>Quarter</th>
      <th>Q1</th>
      <th>Q2</th>
      <th>Q3</th>
      <th>Q4</th>
      <th>Total</th>
    </tr>
    <tr>
      <th>Department</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Finance</th>
      <td>351,252</td>
      <td>707,305</td>
      <td>401,151</td>
      <td>431,342</td>
      <td>1,891,050</td>
    </tr>
    <tr>
      <th>HR</th>
      <td>465,700</td>
      <td>276,984</td>
      <td>337,447</td>
      <td>331,502</td>
      <td>1,411,633</td>
    </tr>
    <tr>
      <th>IT</th>
      <td>327,892</td>
      <td>218,002</td>
      <td>327,664</td>
      <td>391,677</td>
      <td>1,265,235</td>
    </tr>
    <tr>
      <th>Operations</th>
      <td>318,681</td>
      <td>499,678</td>
      <td>284,430</td>
      <td>540,733</td>
      <td>1,643,522</td>
    </tr>
    <tr>
      <th>Sales</th>
      <td>617,090</td>
      <td>334,209</td>
      <td>547,921</td>
      <td>404,259</td>
      <td>1,903,479</td>
    </tr>
    <tr>
      <th>Total</th>
      <td>2,080,615</td>
      <td>2,036,178</td>
      <td>1,898,613</td>
      <td>2,099,513</td>
      <td>8,114,919</td>
    </tr>
  </tbody>
</table>
</div>




```python
# ── 5.3 Pivot: Expense Type × Department (count of transactions) ─────────────
count_pivot = pd.pivot_table(
    expense_df,
    values='Amount',
    index='Expense_Type',
    columns='Department',
    aggfunc='count',
    fill_value=0
)
print('Transaction Count — Expense Type × Department')
print(count_pivot)
```

    Transaction Count — Expense Type × Department
    Department     Finance  HR  IT  Operations  Sales
    Expense_Type                                     
    Communication        7   7   8           9     10
    Misc                12   6   6           7      9
    Printing             9   6   6          10     13
    Repairs              6   8   4          10      3
    Travel              15   6   8           7      8


---
## Section 6: Date Operations — Aging & Period Analysis

Date intelligence is critical in accounting: invoice aging, overdue payments, year-end cutoffs, GST period matching.


```python
# ── 6.1 Accounts Receivable Aging ─────────────────────────────────────────────
ar_data = pd.DataFrame({
    'Invoice_No' : [f'INV-{i:04d}' for i in range(1, 16)],
    'Customer'   : ['Alpha Corp','Beta Ltd','Gamma Inc','Alpha Corp','Delta Co',
                    'Beta Ltd','Epsilon Ltd','Zeta Corp','Alpha Corp','Eta Inc',
                    'Beta Ltd','Theta Ltd','Iota Corp','Kappa Ltd','Alpha Corp'],
    'Invoice_Date': pd.to_datetime([
        '2024-01-05','2024-01-15','2024-01-25','2024-02-01','2024-02-10',
        '2024-02-20','2024-03-01','2024-03-10','2024-03-20','2024-03-28',
        '2024-04-05','2024-04-10','2024-04-15','2024-04-18','2024-04-22'
    ]),
    'Amount'     : [85000,1_20_000,65000,2_30_000,95000,1_80_000,75000,
                    3_50_000,1_10_000,60000,2_40_000,88000,1_50_000,45000,2_80_000],
    'Credit_Days': [30,45,30,30,60,45,30,30,30,60,45,30,30,45,30]
})

report_date = pd.Timestamp('2024-04-30')
ar_data['Due_Date']  = ar_data['Invoice_Date'] + pd.to_timedelta(ar_data['Credit_Days'], unit='D')
ar_data['Days_Outstanding'] = (report_date - ar_data['Invoice_Date']).dt.days
ar_data['Days_Overdue']     = (report_date - ar_data['Due_Date']).dt.days.clip(lower=0)

# Aging Bucket
def aging_bucket(days):
    if days <= 30:   return '0-30 Days'
    elif days <= 60: return '31-60 Days'
    elif days <= 90: return '61-90 Days'
    else:            return '> 90 Days'

ar_data['Aging_Bucket'] = ar_data['Days_Outstanding'].apply(aging_bucket)
print('AR Aging Report:')
print(ar_data[['Invoice_No','Customer','Amount','Invoice_Date','Due_Date','Days_Outstanding','Days_Overdue','Aging_Bucket']].to_string(index=False))
```

    AR Aging Report:
    Invoice_No    Customer  Amount Invoice_Date   Due_Date  Days_Outstanding  Days_Overdue Aging_Bucket
      INV-0001  Alpha Corp   85000   2024-01-05 2024-02-04               116            86    > 90 Days
      INV-0002    Beta Ltd  120000   2024-01-15 2024-02-29               106            61    > 90 Days
      INV-0003   Gamma Inc   65000   2024-01-25 2024-02-24                96            66    > 90 Days
      INV-0004  Alpha Corp  230000   2024-02-01 2024-03-02                89            59   61-90 Days
      INV-0005    Delta Co   95000   2024-02-10 2024-04-10                80            20   61-90 Days
      INV-0006    Beta Ltd  180000   2024-02-20 2024-04-05                70            25   61-90 Days
      INV-0007 Epsilon Ltd   75000   2024-03-01 2024-03-31                60            30   31-60 Days
      INV-0008   Zeta Corp  350000   2024-03-10 2024-04-09                51            21   31-60 Days
      INV-0009  Alpha Corp  110000   2024-03-20 2024-04-19                41            11   31-60 Days
      INV-0010     Eta Inc   60000   2024-03-28 2024-05-27                33             0   31-60 Days
      INV-0011    Beta Ltd  240000   2024-04-05 2024-05-20                25             0    0-30 Days
      INV-0012   Theta Ltd   88000   2024-04-10 2024-05-10                20             0    0-30 Days
      INV-0013   Iota Corp  150000   2024-04-15 2024-05-15                15             0    0-30 Days
      INV-0014   Kappa Ltd   45000   2024-04-18 2024-06-02                12             0    0-30 Days
      INV-0015  Alpha Corp  280000   2024-04-22 2024-05-22                 8             0    0-30 Days



```python
# ── 6.2 Aging Summary ────────────────────────────────────────────────────────
aging_summary = ar_data.groupby('Aging_Bucket').agg(
    Invoices = ('Invoice_No', 'count'),
    Amount   = ('Amount', 'sum')
).reindex(['0-30 Days','31-60 Days','61-90 Days','> 90 Days'])

aging_summary['% of Total'] = (aging_summary['Amount'] / aging_summary['Amount'].sum() * 100).round(1)
print('AR Aging Summary:')
print(aging_summary)
print(f'\nTotal Receivables: ₹{ar_data["Amount"].sum():,.0f}')

# Customer-wise overdue
overdue = ar_data[ar_data['Days_Overdue'] > 0].groupby('Customer')['Amount'].sum()
print(f'\nCustomers with overdue amounts:')
print(overdue.sort_values(ascending=False))
```

    AR Aging Summary:
                  Invoices  Amount  % of Total
    Aging_Bucket                              
    0-30 Days            5  803000       37.00
    31-60 Days           4  595000       27.40
    61-90 Days           3  505000       23.20
    > 90 Days            3  270000       12.40
    
    Total Receivables: ₹2,173,000
    
    Customers with overdue amounts:
    Customer
    Alpha Corp     425000
    Zeta Corp      350000
    Beta Ltd       300000
    Delta Co        95000
    Epsilon Ltd     75000
    Gamma Inc       65000
    Name: Amount, dtype: int64


---
## Section 7: Reading & Writing Files

In practice, your data comes from Tally exports (CSV/Excel) or ERP systems.


```python
import io, os

# ── 7.1 Simulating a CSV read (as if from Tally export) ──────────────────────
csv_data = """Invoice_No,Date,Party,Amount,GST_Rate,GSTIN
INV-001,2024-04-01,Alpha Corp,100000,18,29AAAA1234A1Z5
INV-002,2024-04-03,Beta Ltd,250000,12,29BBBB5678B1Z5
INV-003,2024-04-05,Gamma Inc,75000,18,29CCCC9012C1Z5
INV-004,2024-04-08,Alpha Corp,180000,5,29AAAA1234A1Z5
INV-005,2024-04-12,Delta Co,320000,18,29DDDD3456D1Z5"""

df_csv = pd.read_csv(io.StringIO(csv_data), parse_dates=['Date'])
df_csv['GST_Amount']  = df_csv['Amount'] * df_csv['GST_Rate'] / 100
df_csv['Total_Invoice'] = df_csv['Amount'] + df_csv['GST_Amount']

print('Sales Register (from CSV):')
print(df_csv[['Invoice_No','Party','Amount','GST_Rate','GST_Amount','Total_Invoice']])
print(f'\nTotal Taxable Value : ₹{df_csv["Amount"].sum():>12,.0f}')
print(f'Total GST Collected : ₹{df_csv["GST_Amount"].sum():>12,.0f}')
print(f'Total Invoice Value : ₹{df_csv["Total_Invoice"].sum():>12,.0f}')
```

    Sales Register (from CSV):
      Invoice_No       Party  Amount  GST_Rate  GST_Amount  Total_Invoice
    0    INV-001  Alpha Corp  100000        18   18,000.00     118,000.00
    1    INV-002    Beta Ltd  250000        12   30,000.00     280,000.00
    2    INV-003   Gamma Inc   75000        18   13,500.00      88,500.00
    3    INV-004  Alpha Corp  180000         5    9,000.00     189,000.00
    4    INV-005    Delta Co  320000        18   57,600.00     377,600.00
    
    Total Taxable Value : ₹     925,000
    Total GST Collected : ₹     128,100
    Total Invoice Value : ₹   1,053,100



```python
# ── 7.2 Exporting Results ────────────────────────────────────────────────────
output_path = '/tmp/ar_aging_report.csv'
ar_data.to_csv(output_path, index=False)
print(f'AR Aging report saved to: {output_path}')

# Export with formatting (multiple sheets)
excel_path = '/tmp/financial_reports.xlsx'
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_ledger.to_excel(writer, sheet_name='Ledger',         index=False)
    ar_data.to_excel(writer,   sheet_name='AR_Aging',       index=False)
    acct_summary.to_excel(writer, sheet_name='Acct_Summary', index=False)
print(f'Excel file saved to: {excel_path}')
```

    AR Aging report saved to: /tmp/ar_aging_report.csv
    Excel file saved to: /tmp/financial_reports.xlsx


---
## Section 8: Handling Missing & Dirty Data

Real-world accounting data from ERP exports often has missing values, extra spaces, and inconsistent formats — just like a messy Tally export.


```python
# ── 8.1 Dirty data simulation ────────────────────────────────────────────────
dirty_data = pd.DataFrame({
    'Party'   : ['ABC Ltd ', '  XYZ Traders', 'abc ltd', 'PQR LTD', None, 'DEF Corp'],
    'Amount'  : [50000, None, 75000, 30000, 120000, None],
    'Invoice' : ['INV001', 'INV002', 'INV001', 'INV003', 'INV004', 'INV005'],
    'GSTIN'   : ['29AAAA1234a1z5', '29BBBB5678B1Z5', None, '29CCCC9012C1Z5', 'INVALID', '29DDDD3456D1Z5']
})

print('Before cleaning:')
print(dirty_data)

# ── 8.2 Clean the data ────────────────────────────────────────────────────────
cleaned = dirty_data.copy()
# Strip and standardize party names
cleaned['Party']  = cleaned['Party'].str.strip().str.title()
# Fill missing amounts with 0
cleaned['Amount'] = cleaned['Amount'].fillna(0)
# Standardize GSTIN to uppercase
cleaned['GSTIN']  = cleaned['GSTIN'].str.upper().str.strip()
# Validate GSTIN format (basic: 15 characters)
cleaned['GSTIN_Valid'] = cleaned['GSTIN'].str.len() == 15
# Flag missing party
cleaned['Party_Missing'] = cleaned['Party'].isna()

print('\nAfter cleaning:')
print(cleaned)
print(f'\nInvalid GSTINs: {(~cleaned["GSTIN_Valid"] & cleaned["GSTIN"].notna()).sum()}')
print(f'Missing amounts filled: {(dirty_data["Amount"].isna()).sum()}')
```

    Before cleaning:
               Party     Amount Invoice           GSTIN
    0       ABC Ltd   50,000.00  INV001  29AAAA1234a1z5
    1    XYZ Traders        NaN  INV002  29BBBB5678B1Z5
    2        abc ltd  75,000.00  INV001            None
    3        PQR LTD  30,000.00  INV003  29CCCC9012C1Z5
    4           None 120,000.00  INV004         INVALID
    5       DEF Corp        NaN  INV005  29DDDD3456D1Z5
    
    After cleaning:
             Party     Amount Invoice           GSTIN  GSTIN_Valid  Party_Missing
    0      Abc Ltd  50,000.00  INV001  29AAAA1234A1Z5        False          False
    1  Xyz Traders       0.00  INV002  29BBBB5678B1Z5        False          False
    2      Abc Ltd  75,000.00  INV001            None        False          False
    3      Pqr Ltd  30,000.00  INV003  29CCCC9012C1Z5        False          False
    4         None 120,000.00  INV004         INVALID        False           True
    5     Def Corp       0.00  INV005  29DDDD3456D1Z5        False          False
    
    Invalid GSTINs: 5
    Missing amounts filled: 2


---
## Practice Exercises

1. From the `df_ledger` DataFrame, find all transactions where the amount exceeds ₹2 lakhs. Count them by Voucher_Type.

2. Create a DataFrame of 50 random purchase invoices with dates across FY 2024-25. Group by month and compute monthly purchase totals.

3. Using the AR data, find all customers with outstanding balances older than 60 days. Create a collection priority list sorted by overdue amount.

4. Merge the expense_df with a department budget DataFrame (create it with budgets for each dept). Calculate under/over-spend for each department.

5. Using `pivot_table`, create an expense summary showing the average transaction amount by Department and Expense_Type.


```python
# ── Exercise Solutions ────────────────────────────────────────────────────────

# Exercise 1
large_txns = df_ledger[df_ledger['Amount'] > 2_00_000]
print('Ex 1 — Large transactions by type:')
print(large_txns.groupby('Voucher_Type').size())

# Exercise 3 — Collection Priority
overdue_60 = ar_data[ar_data['Days_Outstanding'] > 60].copy()
overdue_60 = overdue_60.sort_values('Days_Outstanding', ascending=False)
print('\nEx 3 — Collection Priority List (>60 days):')
print(overdue_60[['Customer','Invoice_No','Amount','Days_Outstanding','Days_Overdue']].to_string(index=False))
```

    Ex 1 — Large transactions by type:
    Voucher_Type
    Journal    3
    Receipt    3
    dtype: int64
    
    Ex 3 — Collection Priority List (>60 days):
      Customer Invoice_No  Amount  Days_Outstanding  Days_Overdue
    Alpha Corp   INV-0001   85000               116            86
      Beta Ltd   INV-0002  120000               106            61
     Gamma Inc   INV-0003   65000                96            66
    Alpha Corp   INV-0004  230000                89            59
      Delta Co   INV-0005   95000                80            20
      Beta Ltd   INV-0006  180000                70            25



```python

```
