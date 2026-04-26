# Module 6: Fraud Detection Basics
### Data Science for Chartered Accountants

---

## Learning Objectives
- Apply **Benford's Law** for advanced digit analysis (1st and 2nd digit)
- Detect **duplicate and split payments** in accounts payable
- Identify **ghost vendors** and unusual vendor patterns
- Flag **off-hours and holiday transactions** (control override indicators)
- Implement a **fraud risk scoring model** using multiple indicators
- Understand **journal entry analysis** for management override

---

> **CA Context:** SA 240 requires auditors to maintain **professional skepticism** and specifically look for fraud. These techniques are used in **forensic audits, FEMA reviews, corporate fraud investigations**, and are increasingly required in statutory audits of large companies.


```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(2024)
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', 15)
print('Fraud Detection Module — Loaded')
print('Note: All data is simulated for educational purposes.')
```

    Fraud Detection Module — Loaded
    Note: All data is simulated for educational purposes.


---
## Section 1: Building a Realistic Transaction Dataset with Embedded Fraud

We embed several fraud patterns into the dataset — your job (and the algorithms' job) is to find them.


```python
# ── Normal expense transactions ────────────────────────────────────────────────
n = 800
vendors_legit  = ['Office Depot', 'Bharat Gas', 'MSEB Power', 'Airtel Corp',
                   'Ravi Stationery', 'Hotel Gateway', 'SpiceJet', 'Ola Business',
                   'Amazon Business', 'Zomato Corporate']
departments    = ['Finance', 'Operations', 'Sales', 'HR', 'IT', 'Admin']
expense_cats   = ['Office Supplies', 'Utilities', 'Travel', 'Meals', 'IT Services', 'Repairs']

# Date range: full FY 2024-25, only weekdays
fy_weekdays = pd.bdate_range('2024-04-01', '2025-03-31')

transactions = pd.DataFrame({
    'Txn_ID'     : [f'EXP-{str(i).zfill(5)}' for i in range(1, n+1)],
    'Date'       : np.random.choice(fy_weekdays, n, replace=True),
    'Vendor'     : np.random.choice(vendors_legit, n),
    'Department' : np.random.choice(departments, n),
    'Category'   : np.random.choice(expense_cats, n),
    'Amount'     : np.round(np.random.lognormal(9.5, 1.0, n), -1),  # rounded
    'Employee_ID': np.random.choice([f'EMP-{i:03d}' for i in range(1, 31)], n),
    'Approved_By': np.random.choice(['MGR-001','MGR-002','MGR-003','DIR-001'], n, p=[0.35,0.35,0.20,0.10]),
})

# ── Embed Fraud Patterns ─────────────────────────────────────────────────────
fraud_records = []

# FRAUD 1: Ghost Vendor — new vendor, no PO, large amounts
for i in range(8):
    fraud_records.append({
        'Txn_ID': f'EXP-F{i+1:03d}', 'Date': np.random.choice(fy_weekdays),
        'Vendor': 'Phantom Services Pvt Ltd',  # ghost vendor
        'Department': 'Admin', 'Category': 'IT Services',
        'Amount': np.random.choice([85000, 90000, 95000, 99000]),  # just below limit
        'Employee_ID': 'EMP-007', 'Approved_By': 'MGR-002'
    })

# FRAUD 2: Split transactions — break one large expense into small ones
split_date = pd.Timestamp('2024-07-15')
for i in range(5):
    fraud_records.append({
        'Txn_ID': f'EXP-S{i+1:03d}', 'Date': split_date + timedelta(days=i),
        'Vendor': 'Sundry Repairs Co', 'Department': 'Operations',
        'Category': 'Repairs', 'Amount': 19800,  # 5 × ₹19,800 = ₹99,000 total
        'Employee_ID': 'EMP-012', 'Approved_By': 'MGR-001'
    })

# FRAUD 3: Weekend/holiday transactions
weekends = pd.date_range('2024-04-01', '2025-03-31', freq='W-SAT')
for i in range(6):
    fraud_records.append({
        'Txn_ID': f'EXP-W{i+1:03d}', 'Date': weekends[i*4],
        'Vendor': 'Weekend Supplies', 'Department': 'Finance',
        'Category': 'Office Supplies', 'Amount': np.random.randint(5000, 30000),
        'Employee_ID': 'EMP-019', 'Approved_By': 'MGR-003'
    })

# FRAUD 4: Round number clustering (fabricated)
for amt in [50000, 50000, 1_00_000, 1_00_000, 1_50_000]:
    fraud_records.append({
        'Txn_ID': f'EXP-R{len(fraud_records):03d}', 'Date': np.random.choice(fy_weekdays),
        'Vendor': 'Miscellaneous Vendor', 'Department': 'Finance',
        'Category': 'Office Supplies', 'Amount': amt,
        'Employee_ID': 'EMP-007', 'Approved_By': 'DIR-001'
    })

fraud_df = pd.DataFrame(fraud_records)
all_txns = pd.concat([transactions, fraud_df], ignore_index=True)
all_txns['Date'] = pd.to_datetime(all_txns['Date'])
all_txns['Amount'] = all_txns['Amount'].astype(float)

print(f'Total transactions: {len(all_txns)}')
print(f'Total amount: ₹{all_txns["Amount"].sum():,.0f}')
print(f'Embedded fraud records: {len(fraud_df)}')
all_txns.tail()
```

    Total transactions: 824
    Total amount: ₹20,025,542
    Embedded fraud records: 24





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
      <th>Txn_ID</th>
      <th>Date</th>
      <th>Vendor</th>
      <th>Department</th>
      <th>Category</th>
      <th>Amount</th>
      <th>Employee_ID</th>
      <th>Approved_By</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>819</th>
      <td>EXP-R019</td>
      <td>2024-06-04</td>
      <td>Miscellaneous Vendor</td>
      <td>Finance</td>
      <td>Office Supplies</td>
      <td>50,000.00</td>
      <td>EMP-007</td>
      <td>DIR-001</td>
    </tr>
    <tr>
      <th>820</th>
      <td>EXP-R020</td>
      <td>2024-12-20</td>
      <td>Miscellaneous Vendor</td>
      <td>Finance</td>
      <td>Office Supplies</td>
      <td>50,000.00</td>
      <td>EMP-007</td>
      <td>DIR-001</td>
    </tr>
    <tr>
      <th>821</th>
      <td>EXP-R021</td>
      <td>2024-10-22</td>
      <td>Miscellaneous Vendor</td>
      <td>Finance</td>
      <td>Office Supplies</td>
      <td>100,000.00</td>
      <td>EMP-007</td>
      <td>DIR-001</td>
    </tr>
    <tr>
      <th>822</th>
      <td>EXP-R022</td>
      <td>2024-12-05</td>
      <td>Miscellaneous Vendor</td>
      <td>Finance</td>
      <td>Office Supplies</td>
      <td>100,000.00</td>
      <td>EMP-007</td>
      <td>DIR-001</td>
    </tr>
    <tr>
      <th>823</th>
      <td>EXP-R023</td>
      <td>2025-01-27</td>
      <td>Miscellaneous Vendor</td>
      <td>Finance</td>
      <td>Office Supplies</td>
      <td>150,000.00</td>
      <td>EMP-007</td>
      <td>DIR-001</td>
    </tr>
  </tbody>
</table>
</div>



---
## Section 2: Benford's Law — First & Second Digit Analysis


```python
# ── First Digit Test ──────────────────────────────────────────────────────────
def get_first_digit(x):
    x = abs(x)
    while x >= 10: x /= 10
    while x < 1  : x *= 10
    return int(x)

def get_second_digit(x):
    x = abs(x)
    while x >= 100: x /= 10
    while x < 10  : x *= 10
    return int(x) % 10

expected_1d = {d: np.log10(1 + 1/d) * 100 for d in range(1, 10)}
expected_2d = {d: sum(np.log10(1 + 1/(10*k + d)) for k in range(1,10)) * 100 for d in range(0,10)}

amounts = all_txns['Amount'].dropna()
first_digits  = amounts.apply(get_first_digit)
second_digits = amounts.apply(get_second_digit)

fd_obs = first_digits.value_counts(normalize=True).sort_index() * 100
fd_exp = pd.Series(expected_1d)
fd_df  = pd.DataFrame({'Expected%': fd_exp, 'Observed%': fd_obs}).fillna(0)
fd_df['Deviation%'] = fd_df['Observed%'] - fd_df['Expected%']
fd_df['Z_Stat']     = (fd_df['Deviation%'] / 100) / np.sqrt(fd_exp/100 * (1 - fd_exp/100) / len(amounts)) / 100
fd_df['Flag']       = fd_df['Z_Stat'].abs().apply(lambda z: '⚠ SIGNIFICANT' if z > 1.96 else ('MODERATE' if z > 1.28 else 'OK'))

print('BENFORD\'S FIRST DIGIT TEST')
print(fd_df.round(2))
print(f'\nMAD: {fd_df["Deviation%"].abs().mean():.3f}%')
print(f'Flagged digits: {(fd_df["Flag"] == "⚠ SIGNIFICANT").sum()}')
```

    BENFORD'S FIRST DIGIT TEST
       Expected%  Observed%  Deviation%  Z_Stat Flag
    1      30.10      31.43        1.33    0.01   OK
    2      17.61      16.87       -0.74   -0.01   OK
    3      12.49      12.38       -0.12   -0.00   OK
    4       9.69       9.34       -0.35   -0.00   OK
    5       7.92       7.52       -0.39   -0.00   OK
    6       6.69       6.92        0.22    0.00   OK
    7       5.80       6.19        0.39    0.00   OK
    8       5.12       4.98       -0.14   -0.00   OK
    9       4.58       4.37       -0.21   -0.00   OK
    
    MAD: 0.432%
    Flagged digits: 0



```python
# ── Employee-wise Benford Test ────────────────────────────────────────────────
print('EMPLOYEE-WISE BENFORD ANALYSIS (First Digit MAD%)')
print(f'{"Employee ID":<14} {"Txn Count":>10} {"MAD%":>8} {"Risk Level":>12}')
print('-' * 50)

employee_risk = []
for emp, group in all_txns.groupby('Employee_ID'):
    if len(group) < 15: continue
    emp_digits = group['Amount'].apply(get_first_digit)
    emp_obs    = emp_digits.value_counts(normalize=True).reindex(range(1,10), fill_value=0).sort_index() * 100
    mad        = abs(emp_obs - fd_exp).mean()
    risk       = 'HIGH ⚠' if mad > 4 else 'MEDIUM' if mad > 2 else 'Low'
    employee_risk.append({'Employee': emp, 'Count': len(group), 'MAD%': mad, 'Risk': risk})
    print(f'{emp:<14} {len(group):>10}  {mad:>7.3f}%  {risk:>12}')

emp_risk_df = pd.DataFrame(employee_risk)
print(f'\nHigh risk employees: {(emp_risk_df["Risk"] == "HIGH ⚠").sum()}')
```

    EMPLOYEE-WISE BENFORD ANALYSIS (First Digit MAD%)
    Employee ID     Txn Count     MAD%   Risk Level
    --------------------------------------------------
    EMP-001                21    5.103%        HIGH ⚠
    EMP-002                25    4.665%        HIGH ⚠
    EMP-003                26    4.199%        HIGH ⚠
    EMP-004                32    1.929%           Low
    EMP-005                28    5.387%        HIGH ⚠
    EMP-006                29    3.975%        MEDIUM
    EMP-007                35    6.793%        HIGH ⚠
    EMP-008                18    4.843%        HIGH ⚠
    EMP-009                23    5.378%        HIGH ⚠
    EMP-010                31    2.862%        MEDIUM
    EMP-011                30    4.077%        HIGH ⚠
    EMP-012                33    4.886%        HIGH ⚠
    EMP-013                28    3.955%        MEDIUM
    EMP-014                26    4.782%        HIGH ⚠
    EMP-015                27    6.524%        HIGH ⚠
    EMP-016                30    3.144%        MEDIUM
    EMP-017                22    3.322%        MEDIUM
    EMP-018                17    6.220%        HIGH ⚠
    EMP-019                24    2.310%        MEDIUM
    EMP-020                39    2.450%        MEDIUM
    EMP-021                28    4.972%        HIGH ⚠
    EMP-022                18    5.403%        HIGH ⚠
    EMP-023                21    5.123%        HIGH ⚠
    EMP-024                36    3.867%        MEDIUM
    EMP-025                24    4.000%        MEDIUM
    EMP-026                36    4.435%        HIGH ⚠
    EMP-027                37    2.259%        MEDIUM
    EMP-028                24    3.286%        MEDIUM
    EMP-029                32    4.204%        HIGH ⚠
    EMP-030                24    4.838%        HIGH ⚠
    
    High risk employees: 18


---
## Section 3: Duplicate & Split Payment Detection


```python
# ── 3.1 Exact Duplicates ─────────────────────────────────────────────────────
exact_dups = all_txns[all_txns.duplicated(subset=['Vendor','Amount','Date'], keep=False)]
print(f'EXACT DUPLICATES: {len(exact_dups)} records ({len(exact_dups)//2} pairs)')
if not exact_dups.empty:
    print(exact_dups[['Txn_ID','Date','Vendor','Amount','Employee_ID','Approved_By']].to_string(index=False))

# ── 3.2 Same Vendor + Same Amount within 7 days ───────────────────────────────
sorted_txns = all_txns.sort_values(['Vendor','Amount','Date']).reset_index(drop=True)
near_dups = []
for i in range(len(sorted_txns) - 1):
    r1 = sorted_txns.iloc[i]
    r2 = sorted_txns.iloc[i+1]
    if (r1['Vendor'] == r2['Vendor'] and
        r1['Amount'] == r2['Amount'] and
        0 < abs((pd.Timestamp(r2['Date']) - pd.Timestamp(r1['Date'])).days) <= 7):
        near_dups.append({
            'Txn_1': r1['Txn_ID'], 'Txn_2': r2['Txn_ID'],
            'Vendor': r1['Vendor'], 'Amount': r1['Amount'],
            'Date_1': r1['Date'].strftime('%Y-%m-%d'),
            'Date_2': r2['Date'].strftime('%Y-%m-%d'),
            'Days_Apart': abs((pd.Timestamp(r2['Date']) - pd.Timestamp(r1['Date'])).days)
        })

near_dup_df = pd.DataFrame(near_dups)
print(f'\nNEAR-DUPLICATES (same vendor+amount, ≤7 days apart): {len(near_dup_df)}')
if not near_dup_df.empty:
    print(near_dup_df.head(10).to_string(index=False))
```

    EXACT DUPLICATES: 0 records (0 pairs)
    
    NEAR-DUPLICATES (same vendor+amount, ≤7 days apart): 5
        Txn_1     Txn_2            Vendor    Amount     Date_1     Date_2  Days_Apart
    EXP-00658 EXP-00477   Amazon Business  4,610.00 2024-09-13 2024-09-20           7
     EXP-S001  EXP-S002 Sundry Repairs Co 19,800.00 2024-07-15 2024-07-16           1
     EXP-S002  EXP-S003 Sundry Repairs Co 19,800.00 2024-07-16 2024-07-17           1
     EXP-S003  EXP-S004 Sundry Repairs Co 19,800.00 2024-07-17 2024-07-18           1
     EXP-S004  EXP-S005 Sundry Repairs Co 19,800.00 2024-07-18 2024-07-19           1



```python
# ── 3.3 Split Transaction Detection ──────────────────────────────────────────
# Detect: same vendor, same employee, multiple transactions in same week
# that together exceed an approval threshold
APPROVAL_LIMIT = 1_00_000  # ₹1 lakh

# Add week identifier
all_txns_copy = all_txns.copy()
all_txns_copy['Week'] = all_txns_copy['Date'].dt.to_period('W')

weekly_vendor = all_txns_copy.groupby(['Vendor','Employee_ID','Week']).agg(
    Count  = ('Amount','count'),
    Total  = ('Amount','sum'),
    Max    = ('Amount','max'),
    Txn_IDs= ('Txn_ID', lambda x: ', '.join(x.tolist()[:5]))
).reset_index()

# Flag: multiple small transactions that total above limit, each below limit
split_suspect = weekly_vendor[
    (weekly_vendor['Count'] >= 3) &          # at least 3 transactions
    (weekly_vendor['Total'] > APPROVAL_LIMIT) &   # combined > limit
    (weekly_vendor['Max']   < APPROVAL_LIMIT)      # each individual < limit
].sort_values('Total', ascending=False)

print(f'SPLIT TRANSACTION SUSPECTS: {len(split_suspect)}')
print(f'Approval Limit Used: ₹{APPROVAL_LIMIT:,.0f}')
if not split_suspect.empty:
    print(split_suspect[['Vendor','Employee_ID','Week','Count','Total','Max']].to_string(index=False))
```

    SPLIT TRANSACTION SUSPECTS: 0
    Approval Limit Used: ₹100,000


---
## Section 4: Temporal Anomalies — Off-Hours & Holiday Transactions

> **Red Flag:** Transactions on weekends, holidays, or at unusual hours (night/early morning) may indicate:
> - **Management override** of controls
> - **System access by unauthorized users**
> - Backdated entries


```python
# ── 4.1 Weekend & Holiday Analysis ────────────────────────────────────────────
all_txns['Day_of_Week'] = all_txns['Date'].dt.day_name()
all_txns['Is_Weekend']  = all_txns['Date'].dt.dayofweek >= 5

# Indian public holidays FY 2024-25 (partial list)
holidays = pd.to_datetime([
    '2024-04-14',  # Ambedkar Jayanti
    '2024-05-23',  # Buddha Purnima
    '2024-06-17',  # Eid ul-Adha
    '2024-08-15',  # Independence Day
    '2024-10-02',  # Gandhi Jayanti
    '2024-10-12',  # Dussehra
    '2024-11-01',  # Diwali
    '2024-11-15',  # Guru Nanak Jayanti
    '2024-12-25',  # Christmas
    '2025-01-26',  # Republic Day
    '2025-03-14',  # Holi
])
all_txns['Is_Holiday'] = all_txns['Date'].isin(holidays)
all_txns['Is_Suspicious_Date'] = all_txns['Is_Weekend'] | all_txns['Is_Holiday']

suspicious_temporal = all_txns[all_txns['Is_Suspicious_Date']]
print(f'TEMPORAL ANOMALIES:')
print(f'  Weekend transactions : {all_txns["Is_Weekend"].sum():>5}')
print(f'  Holiday transactions : {all_txns["Is_Holiday"].sum():>5}')
print(f'  Total suspicious     : {len(suspicious_temporal):>5}')
print(f'  Amount involved      : ₹{suspicious_temporal["Amount"].sum():>12,.0f}')

print('\nSuspicious temporal transactions by employee:')
print(suspicious_temporal.groupby('Employee_ID').agg(
    Count=('Amount','count'), Total=('Amount','sum')
).sort_values('Total', ascending=False).head(10))
```

    TEMPORAL ANOMALIES:
      Weekend transactions :     6
      Holiday transactions :    18
      Total suspicious     :    24
      Amount involved      : ₹     522,312
    
    Suspicious temporal transactions by employee:
                 Count     Total
    Employee_ID                 
    EMP-019          6 91,752.00
    EMP-023          3 86,230.00
    EMP-027          1 80,650.00
    EMP-022          1 74,380.00
    EMP-025          2 72,470.00
    EMP-028          2 43,150.00
    EMP-001          2 25,650.00
    EMP-012          1 16,370.00
    EMP-011          1  7,380.00
    EMP-030          1  6,670.00


---
## Section 5: Ghost Vendor Detection


```python
# ── 5.1 Vendor Profile Analysis ───────────────────────────────────────────────
vendor_profile = all_txns.groupby('Vendor').agg(
    Txn_Count   = ('Amount','count'),
    Total_Amount= ('Amount','sum'),
    Avg_Amount  = ('Amount','mean'),
    Employees   = ('Employee_ID', 'nunique'),  # how many employees transact with this vendor
    Approvers   = ('Approved_By','nunique'),
    First_Seen  = ('Date','min'),
    Last_Seen   = ('Date','max')
).reset_index()

vendor_profile['Days_Active'] = (vendor_profile['Last_Seen'] - vendor_profile['First_Seen']).dt.days + 1
vendor_profile['Txn_per_Day'] = vendor_profile['Txn_Count'] / vendor_profile['Days_Active'].clip(lower=1)

# Ghost vendor indicators:
# - Very few employees transact with them
# - Very few approvers (single approver)
# - Amounts clustering near thresholds
# - Short active period

vendor_profile['Ghost_Score'] = 0
vendor_profile['Ghost_Score'] += (vendor_profile['Employees'] == 1).astype(int)    # single employee
vendor_profile['Ghost_Score'] += (vendor_profile['Approvers'] == 1).astype(int)    # single approver
vendor_profile['Ghost_Score'] += (vendor_profile['Days_Active'] < 90).astype(int)  # new vendor
vendor_profile['Ghost_Score'] += (vendor_profile['Total_Amount'] > 3_00_000).astype(int)  # large amounts

high_risk_vendors = vendor_profile[vendor_profile['Ghost_Score'] >= 3].sort_values('Ghost_Score', ascending=False)
print(f'GHOST VENDOR RISK ANALYSIS')
print(f'Total vendors: {len(vendor_profile)}')
print(f'High risk (score ≥ 3): {len(high_risk_vendors)}')
print('\nHigh Risk Vendors:')
print(high_risk_vendors[['Vendor','Txn_Count','Total_Amount','Employees','Approvers','Ghost_Score']].to_string(index=False))
```

    GHOST VENDOR RISK ANALYSIS
    Total vendors: 14
    High risk (score ≥ 3): 3
    
    High Risk Vendors:
                      Vendor  Txn_Count  Total_Amount  Employees  Approvers  Ghost_Score
        Miscellaneous Vendor          5    450,000.00          1          1            3
    Phantom Services Pvt Ltd          8    762,000.00          1          1            3
           Sundry Repairs Co          5     99,000.00          1          1            3



```python
# ── 5.2 Round Number Analysis ─────────────────────────────────────────────────
# Natural amounts are rarely perfectly round. Round amounts suggest fabrication.
all_txns['Is_Round_1000']  = all_txns['Amount'] % 1000 == 0
all_txns['Is_Round_5000']  = all_txns['Amount'] % 5000 == 0
all_txns['Is_Round_10000'] = all_txns['Amount'] % 10000 == 0

print('ROUND NUMBER ANALYSIS:')
total = len(all_txns)
for col, label in [('Is_Round_1000','Multiples of ₹1,000'),
                    ('Is_Round_5000','Multiples of ₹5,000'),
                    ('Is_Round_10000','Multiples of ₹10,000')]:
    count = all_txns[col].sum()
    pct   = count / total * 100
    print(f'  {label:<25}: {count:>5} ({pct:.1f}%) — Expected ~10-15%')

# Round number breakdown by vendor
round_by_vendor = all_txns.groupby('Vendor').agg(
    Total_Txns  = ('Amount', 'count'),
    Round_Txns  = ('Is_Round_5000', 'sum')
)
round_by_vendor['Round_Pct'] = round_by_vendor['Round_Txns'] / round_by_vendor['Total_Txns'] * 100
high_round = round_by_vendor[round_by_vendor['Round_Pct'] > 50].sort_values('Round_Pct', ascending=False)
print('\nVendors with >50% round amounts (multiple of 5000):')
print(high_round)
```

    ROUND NUMBER ANALYSIS:
      Multiples of ₹1,000      :    22 (2.7%) — Expected ~10-15%
      Multiples of ₹5,000      :    12 (1.5%) — Expected ~10-15%
      Multiples of ₹10,000     :     7 (0.8%) — Expected ~10-15%
    
    Vendors with >50% round amounts (multiple of 5000):
                              Total_Txns  Round_Txns  Round_Pct
    Vendor                                                     
    Miscellaneous Vendor               5           5     100.00
    Phantom Services Pvt Ltd           8           5      62.50


---
## Section 6: Journal Entry Analysis — Management Override (SA 240)

**SA 240** specifically requires testing journal entries for management override. Key red flags:
- Journal entries posted by senior management directly
- Entries on last day of period (year-end manipulation)
- Unusual debit/credit combinations
- Round-number adjustments


```python
# ── Journal Entry Test Data ────────────────────────────────────────────────────
np.random.seed(99)
n_je = 300
accounts = ['Sales Revenue','COGS','Salary Exp','Rent Exp','Depreciation',
             'Interest Exp','Misc Income','Other Exp','Debtors','Creditors',
             'Cash','Bank','Provisions','Reserves']
je_users  = ['System','Accounts-1','Accounts-2','Finance-Mgr','CFO','IT-Admin']

je_dates = np.random.choice(pd.date_range('2024-04-01', '2025-03-31'), n_je)
# Add year-end rush entries
yearend_dates = pd.date_range('2025-03-28', '2025-03-31')
je_dates = np.concatenate([je_dates, np.random.choice(yearend_dates, 40)])

n_total_je = len(je_dates)
journal_entries = pd.DataFrame({
    'JE_No'       : [f'JE-{i:04d}' for i in range(1, n_total_je+1)],
    'Date'        : pd.to_datetime(je_dates),
    'Debit_Acct'  : np.random.choice(accounts, n_total_je),
    'Credit_Acct' : np.random.choice(accounts, n_total_je),
    'Amount'      : np.abs(np.random.normal(50000, 80000, n_total_je)).round(-3).clip(1000),
    'Posted_By'   : np.random.choice(je_users, n_total_je, p=[0.40, 0.25, 0.20, 0.08, 0.05, 0.02]),
    'Narration'   : np.random.choice(['Month-end closing','Accrual entry','Reversal',
                                       'Adjustment','Provision','Correction','Reclassification'], n_total_je)
})

# Flag same debit & credit account (circular entry)
journal_entries['Flag_Same_Acct']   = journal_entries['Debit_Acct'] == journal_entries['Credit_Acct']
# Flag manual posts by senior management
journal_entries['Flag_Sr_Mgmt']     = journal_entries['Posted_By'].isin(['CFO','Finance-Mgr'])
# Flag year-end (last 3 days of FY)
journal_entries['Flag_YearEnd']     = journal_entries['Date'] >= '2025-03-29'
# Flag round numbers
journal_entries['Flag_Round']       = journal_entries['Amount'] % 10000 == 0
# Flag high amount (Z > 2)
z = (journal_entries['Amount'] - journal_entries['Amount'].mean()) / journal_entries['Amount'].std()
journal_entries['Flag_Large']       = z > 2.0

flag_cols = ['Flag_Same_Acct','Flag_Sr_Mgmt','Flag_YearEnd','Flag_Round','Flag_Large']
journal_entries['JE_Risk_Score'] = journal_entries[flag_cols].sum(axis=1)

print('JOURNAL ENTRY RISK ANALYSIS')
print(f'Total JEs analysed: {len(journal_entries)}')
for col in flag_cols:
    c = journal_entries[col].sum()
    print(f'  {col:<22}: {c:>5} JEs')

high_risk_je = journal_entries[journal_entries['JE_Risk_Score'] >= 2]
print(f'\nHigh Risk JEs (score >= 2): {len(high_risk_je)}')
print('\nTop high-risk journal entries:')
print(high_risk_je[['JE_No','Date','Debit_Acct','Credit_Acct','Amount','Posted_By','JE_Risk_Score']].head(10).to_string(index=False))
```

    JOURNAL ENTRY RISK ANALYSIS
    Total JEs analysed: 340
      Flag_Same_Acct        :    26 JEs
      Flag_Sr_Mgmt          :    50 JEs
      Flag_YearEnd          :    31 JEs
      Flag_Round            :    31 JEs
      Flag_Large            :    15 JEs
    
    High Risk JEs (score >= 2): 22
    
    Top high-risk journal entries:
      JE_No       Date Debit_Acct  Credit_Acct     Amount   Posted_By  JE_Risk_Score
    JE-0016 2025-03-30  Other Exp Interest Exp 214,000.00      System              2
    JE-0061 2024-07-24       Cash    Creditors 150,000.00 Finance-Mgr              2
    JE-0079 2024-07-15   Rent Exp     Rent Exp 104,000.00         CFO              2
    JE-0120 2024-04-14       Cash     Rent Exp 200,000.00      System              2
    JE-0121 2024-11-27   Rent Exp  Misc Income 284,000.00 Finance-Mgr              2
    JE-0140 2024-06-19       Bank         Bank 209,000.00    IT-Admin              2
    JE-0148 2025-03-17   Reserves     Reserves  10,000.00      System              2
    JE-0198 2024-08-30  Other Exp      Debtors 214,000.00         CFO              2
    JE-0219 2025-02-05  Other Exp    Other Exp 143,000.00         CFO              2
    JE-0223 2024-10-16   Rent Exp     Rent Exp  50,000.00      System              2


---
## Section 7: Comprehensive Fraud Risk Score


```python
# ── Combined Fraud Scoring ────────────────────────────────────────────────────
fraud_report = all_txns.copy()
fraud_report['Date'] = pd.to_datetime(fraud_report['Date'])

# Z-Score per vendor (relative to vendor's own distribution)
fraud_report['Vendor_Z'] = fraud_report.groupby('Vendor')['Amount'].transform(
    lambda x: (x - x.mean()) / (x.std() + 1e-6)
)

# Flags
fraud_report['F_Round']    = fraud_report['Amount'] % 5000 == 0
fraud_report['F_Weekend']  = fraud_report['Date'].dt.dayofweek >= 5
fraud_report['F_Holiday']  = fraud_report['Date'].isin(holidays)
fraud_report['F_JustBelow']= fraud_report['Amount'].between(90_000, 99_999)
fraud_report['F_VendorZ']  = fraud_report['Vendor_Z'] > 2.5
fraud_report['F_NewVendor']= fraud_report['Vendor'].isin(
    vendor_profile[vendor_profile['Days_Active'] < 90]['Vendor']
)

score_cols = ['F_Round','F_Weekend','F_Holiday','F_JustBelow','F_VendorZ','F_NewVendor']
fraud_report['Fraud_Score'] = fraud_report[score_cols].astype(int).sum(axis=1)

high_fraud = fraud_report[fraud_report['Fraud_Score'] >= 3].sort_values('Fraud_Score', ascending=False)

print('FRAUD RISK SCORECARD')
print(f'Total transactions : {len(fraud_report)}')
print(f'High risk (≥3 flags): {len(high_fraud)} ({len(high_fraud)/len(fraud_report)*100:.1f}%)')
print(f'Amount under review: ₹{high_fraud["Amount"].sum():,.0f}')
print('\nFlag Distribution:')
for col in score_cols:
    c = fraud_report[col].sum()
    print(f'  {col:<15}: {c:>5} transactions')
print('\nTop 15 Highest Risk Transactions:')
print(high_fraud[['Txn_ID','Date','Vendor','Amount','Employee_ID','Fraud_Score'] + score_cols].head(15).to_string(index=False))
```

    FRAUD RISK SCORECARD
    Total transactions : 824
    High risk (≥3 flags): 0 (0.0%)
    Amount under review: ₹0
    
    Flag Distribution:
      F_Round        :    12 transactions
      F_Weekend      :     6 transactions
      F_Holiday      :    18 transactions
      F_JustBelow    :    14 transactions
      F_VendorZ      :    26 transactions
      F_NewVendor    :     5 transactions
    
    Top 15 Highest Risk Transactions:
    Empty DataFrame
    Columns: [Txn_ID, Date, Vendor, Amount, Employee_ID, Fraud_Score, F_Round, F_Weekend, F_Holiday, F_JustBelow, F_VendorZ, F_NewVendor]
    Index: []


---
## Practice Exercises

1. An employee submits 12 expense claims in one month, all for ₹4,800 each (just below ₹5,000 policy threshold). Write code to detect this pattern across all employees.

2. **Payroll fraud**: Find employees who appear in both the vendor master and the employee list (a common fraud indicator).

3. Apply the **second digit Benford's test** to the expense transactions. Which departments deviate most?

4. Build a **velocity analysis**: find employees whose total weekly expense claims jumped more than 3× compared to their own 4-week average.

5. Identify transactions where the narration is suspiciously generic (e.g., 'Misc', 'Adjustment') AND the amount is above ₹50,000.


```python
# ── Exercise Solutions ────────────────────────────────────────────────────────

# Exercise 1: Repeated threshold-just-below amounts by employee
threshold = 5000
just_below = all_txns[all_txns['Amount'].between(threshold * 0.9, threshold - 1)]
emp_just_below = just_below.groupby('Employee_ID').agg(
    Count  = ('Amount','count'),
    Total  = ('Amount','sum'),
    Amounts= ('Amount', lambda x: list(x.unique())[:5])
).sort_values('Count', ascending=False)

suspicious_employees = emp_just_below[emp_just_below['Count'] >= 3]
print('Ex 1 — Employees with repeated just-below-threshold claims:')
print(suspicious_employees)

# Exercise 5: Generic narration + high amount JEs
generic_narrations = ['Correction', 'Adjustment', 'Reclassification']
risky_je = journal_entries[
    journal_entries['Narration'].isin(generic_narrations) &
    (journal_entries['Amount'] > 50_000)
]
print(f'\nEx 5 — Generic narration + high amount JEs: {len(risky_je)}')
print(risky_je[['JE_No','Date','Debit_Acct','Credit_Acct','Amount','Posted_By','Narration']].head().to_string(index=False))
```

    Ex 1 — Employees with repeated just-below-threshold claims:
                 Count     Total                   Amounts
    Employee_ID                                           
    EMP-020          3 13,750.00  [4610.0, 4560.0, 4580.0]
    EMP-021          3 14,280.00  [4710.0, 4950.0, 4620.0]
    
    Ex 5 — Generic narration + high amount JEs: 112
      JE_No       Date    Debit_Acct  Credit_Acct     Amount  Posted_By        Narration
    JE-0001 2024-08-08     Creditors  Misc Income  97,000.00 Accounts-2       Correction
    JE-0003 2024-10-03 Sales Revenue  Misc Income 153,000.00 Accounts-2 Reclassification
    JE-0006 2024-11-19  Depreciation    Other Exp  92,000.00     System       Correction
    JE-0009 2024-10-15  Depreciation   Provisions  55,000.00 Accounts-1       Adjustment
    JE-0016 2025-03-30     Other Exp Interest Exp 214,000.00     System Reclassification

