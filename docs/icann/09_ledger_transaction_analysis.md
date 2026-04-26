# Module 9: Ledger & Transaction Analysis
### Data Science for Chartered Accountants

---

## Learning Objectives

By the end of this module you will be able to:

1. **Validate a Trial Balance** — debit/credit equality, duplicate accounts
2. **Analyse journal entries** — round-amount entries, entries by unusual users, period-end clustering
3. **AR Aging** — customer-wise aging buckets (30/60/90/120+ days)
4. **AP Aging** — vendor-wise overdue analysis, early payment discount detection
5. **Bank Reconciliation** — match bank statement to cash book, identify uncleared items
6. **Ledger scrutiny** — narration analysis, unusual debit/credit patterns
7. **Period-end accrual analysis** — large entries near cut-off dates

---

**Company:** Meridian Consulting & Services Pvt. Ltd. 
**Period:** FY 2024-25 (April 2024 – March 2025) 
**Standards:** SA 520 (Analytical Procedures), SA 240 (Fraud), SA 315 (Risk Assessment)

> All amounts in ₹ (Indian Rupees). Lakhs = 1,00,000.


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import date, timedelta
import warnings
warnings.filterwarnings('ignore')

%matplotlib inline
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.05)
plt.rcParams['figure.figsize'] = (12, 5)

np.random.seed(2024)
REPORT_DATE = date(2025, 3, 31)   # Balance sheet date

print('Environment ready.')
print(f'Report date: {REPORT_DATE}')
```

---
## Part 1: Trial Balance Validation

The trial balance lists every account with its closing debit or credit balance.

**Audit checks:**
- Sum of all debits = Sum of all credits (fundamental accounting equation)
- No duplicate account codes
- No accounts with both debit AND credit balances
- Unexpected zero-balance accounts


```python
# ── Trial Balance Data ────────────────────────────────────────────────────────
tb_data = [
    # Assets
    ('1001', 'Cash & Cash Equivalents',   'Asset',       12_50_000,        0),
    ('1002', 'Bank — HDFC Current A/c',   'Asset',      1_85_40_000,       0),
    ('1003', 'Bank — Axis Savings A/c',   'Asset',       18_20_000,        0),
    ('1010', 'Accounts Receivable',        'Asset',      2_42_60_000,       0),
    ('1011', 'Advance to Suppliers',       'Asset',       15_00_000,        0),
    ('1020', 'Inventory',                  'Asset',       45_80_000,        0),
    ('1030', 'Prepaid Expenses',           'Asset',        4_20_000,        0),
    ('1040', 'TDS Receivable',             'Asset',        8_75_000,        0),
    ('1050', 'Advance Tax Paid',           'Asset',       22_00_000,        0),
    ('2001', 'Plant & Machinery (Gross)',  'Asset',      5_60_00_000,       0),
    ('2002', 'Acc. Depreciation — P&M',   'Asset',              0,  2_24_00_000),
    ('2003', 'Furniture & Fixtures',       'Asset',       28_50_000,        0),
    ('2004', 'Acc. Depreciation — F&F',   'Asset',              0,   11_40_000),
    ('2005', 'Computer Equipment',         'Asset',       42_00_000,        0),
    ('2006', 'Acc. Depreciation — Comp',  'Asset',              0,   25_20_000),
    # Liabilities
    ('3001', 'Share Capital',              'Equity',             0,  1_00_00_000),
    ('3002', 'Retained Earnings',          'Equity',             0,  2_18_50_000),
    ('3010', 'Accounts Payable',           'Liability',          0,  1_42_30_000),
    ('3011', 'Advance from Customers',     'Liability',          0,   12_00_000),
    ('3020', 'Bank Loan — Term',           'Liability',          0,  1_50_00_000),
    ('3021', 'Bank Loan — Working Capital','Liability',          0,   80_00_000),
    ('3030', 'GST Payable',                'Liability',          0,    9_80_000),
    ('3031', 'TDS Payable',                'Liability',          0,    3_20_000),
    ('3032', 'Salary Payable',             'Liability',          0,   18_50_000),
    ('3033', 'Provision for Expenses',     'Liability',          0,   14_00_000),
    # Income
    ('4001', 'Sales — Consulting',         'Revenue',            0,  6_80_00_000),
    ('4002', 'Sales — Products',           'Revenue',            0,  1_20_00_000),
    ('4003', 'Other Income',               'Revenue',            0,    8_50_000),
    # Expenses
    ('5001', 'Cost of Services',           'Expense',   3_80_00_000,        0),
    ('5002', 'Salaries & Wages',           'Expense',   1_62_00_000,        0),
    ('5003', 'Rent Expense',               'Expense',    24_00_000,         0),
    ('5004', 'Depreciation',               'Expense',    26_06_000,         0),  # intentional mismatch for demo
    ('5005', 'Interest Expense',           'Expense',    18_50_000,         0),
    ('5006', 'Marketing & Advertising',    'Expense',    12_00_000,         0),
    ('5007', 'Professional Fees',          'Expense',     8_40_000,         0),
    ('5008', 'Travelling Expenses',        'Expense',     6_20_000,         0),
    ('5009', 'Office Expenses',            'Expense',     4_80_000,         0),
    ('5010', 'Provision for Bad Debts',    'Expense',     5_00_000,         0),
    ('5011', 'Income Tax Expense',         'Expense',    28_50_000,         0),
    ('5012', 'Miscellaneous Expenses',     'Expense',     1_20_000,         0),
]

tb = pd.DataFrame(tb_data, columns=['acc_code', 'acc_name', 'type', 'debit', 'credit'])
print(f'Trial Balance — {len(tb)} accounts loaded')
tb.head(8)
```


```python
# ── Check 1: Debit = Credit ───────────────────────────────────────────────────
total_dr = tb['debit'].sum()
total_cr = tb['credit'].sum()
diff     = total_dr - total_cr

print('=== TRIAL BALANCE VALIDATION ===')
print(f'Total Debits  : ₹{total_dr:>15,.0f}')
print(f'Total Credits : ₹{total_cr:>15,.0f}')
print(f'Difference    : ₹{diff:>15,.0f}  ← Should be ₹0')
print(f'Balanced      : {"✅ YES" if abs(diff) < 1 else "❌ NO — INVESTIGATE!"}')

if abs(diff) > 0:
    print(f'\n⚠️  Difference of ₹{diff:,.0f} detected!')
    print('   Check: recent journal entries, data import, rounding differences.')
```


```python
# ── Check 2: Duplicate account codes ─────────────────────────────────────────
dup_codes = tb[tb.duplicated('acc_code', keep=False)]
print('Check 2 — Duplicate account codes:')
if dup_codes.empty:
    print('  ✅ No duplicate codes found')
else:
    print('  ❌ Duplicates detected!')
    print(dup_codes[['acc_code', 'acc_name']])

# ── Check 3: Accounts with both Dr and Cr balances ───────────────────────────
both_sides = tb[(tb['debit'] > 0) & (tb['credit'] > 0)]
print('\nCheck 3 — Accounts with both Debit AND Credit balance:')
if both_sides.empty:
    print('  ✅ No accounts with dual balances')
else:
    print('  ⚠️ These accounts need review:')
    print(both_sides[['acc_code', 'acc_name', 'debit', 'credit']])

# ── Check 4: Zero balance accounts ───────────────────────────────────────────
zero_bal = tb[(tb['debit'] == 0) & (tb['credit'] == 0)]
print(f'\nCheck 4 — Zero balance accounts: {len(zero_bal)}')
if not zero_bal.empty:
    print('  (These are OK if dormant, but verify)')
    print(zero_bal[['acc_code', 'acc_name']])

# ── Summary by type ───────────────────────────────────────────────────────────
print('\n=== BALANCE SHEET SUMMARY ===')
tb_summary = tb.groupby('type').agg({'debit': 'sum', 'credit': 'sum'})
tb_summary['net'] = tb_summary['debit'] - tb_summary['credit']
print(tb_summary.map(lambda x: f'₹{x:>12,.0f}'))
```

---
## Part 2: Journal Entry Analysis

**SA 240** requires auditors to test journal entries for:
- Round amounts (possible estimates or manipulations)
- Entries by unusual users or on unusual dates
- Entries posted at period-end (cut-off risk)
- Entries to unusual accounts


```python
# ── Generate journal entries dataset ─────────────────────────────────────────
def random_dates(start, end, n):
    delta = (end - start).days
    offsets = np.random.randint(0, delta, n)
    return [start + timedelta(days=int(d)) for d in offsets]

fy_start = date(2024, 4, 1)
fy_end   = date(2025, 3, 31)

users    = ['rajesh.k', 'priya.s', 'amit.v', 'admin', 'system', 'sunita.j', 'vikram.n']
acc_dr   = ['5001', '5002', '5003', '1010', '1002', '5006', '5007', '5010', '5008']
acc_cr   = ['3010', '3032', '1002', '4001', '3011', '3030', '1002', '1002', '3010']
narrations = [
    'Cost accrual for services rendered',
    'Salary payment for the month',
    'Rent payment — office premises',
    'Revenue recognition — project delivery',
    'Payment to vendor — purchase invoice',
    'Marketing campaign expenses',
    'Professional fees — legal services',
    'Provision for bad debts — AR review',
    'Travel reimbursement — sales team',
]

n_normal = 450
normal_dates    = random_dates(fy_start, fy_end, n_normal)
normal_amounts  = np.random.lognormal(mean=10.5, sigma=1.2, size=n_normal).round(-2)
normal_amounts  = np.clip(normal_amounts, 500, 20_00_000)

jv_df = pd.DataFrame({
    'je_number'  : [f'JV-{i:04d}' for i in range(1, n_normal + 1)],
    'date'       : normal_dates,
    'user'       : np.random.choice(users[:4], n_normal, p=[0.30, 0.30, 0.25, 0.15]),
    'dr_account' : np.random.choice(acc_dr, n_normal),
    'cr_account' : np.random.choice(acc_cr, n_normal),
    'amount'     : normal_amounts,
    'narration'  : np.random.choice(narrations, n_normal),
})

# ── Inject anomalies ─────────────────────────────────────────────────────────
# 1. Round-amount entries (suspicious)
round_entries = pd.DataFrame({
    'je_number'  : [f'JV-{i:04d}' for i in range(451, 461)],
    'date'       : random_dates(date(2025, 3, 25), date(2025, 3, 31), 10),
    'user'       : ['admin'] * 10,
    'dr_account' : ['5012'] * 10,
    'cr_account' : ['1002'] * 10,
    'amount'     : [5_00_000, 10_00_000, 2_50_000, 7_50_000, 1_00_000,
                    3_00_000, 15_00_000, 50_000, 20_00_000, 4_00_000],
    'narration'  : ['Year-end adjustment'] * 10,
})

# 2. Weekend entries
weekend_dates = [date(2024, 6, 29), date(2024, 8, 4), date(2024, 11, 9),
                 date(2025, 1, 5), date(2025, 2, 15)]
weekend_entries = pd.DataFrame({
    'je_number'  : [f'JV-{i:04d}' for i in range(461, 466)],
    'date'       : weekend_dates,
    'user'       : ['vikram.n', 'admin', 'priya.s', 'admin', 'vikram.n'],
    'dr_account' : ['5007', '5012', '5001', '5009', '5006'],
    'cr_account' : ['1002', '1002', '3010', '1002', '3010'],
    'amount'     : [1_80_000, 2_50_000, 85_000, 1_20_000, 95_000],
    'narration'  : ['Emergency vendor payment', 'Year-end misc write-off',
                    'Service receipt posting', 'Office setup', 'Urgent campaign cost'],
})

jv_df = pd.concat([jv_df, round_entries, weekend_entries], ignore_index=True)
jv_df['date']   = pd.to_datetime(jv_df['date'])
jv_df['amount'] = jv_df['amount'].astype(float)
jv_df['weekday']= jv_df['date'].dt.day_name()
jv_df['month']  = jv_df['date'].dt.strftime('%b-%Y')

print(f'Journal entries loaded: {len(jv_df):,}')
print(f'Total value: ₹{jv_df["amount"].sum():,.0f}')
jv_df.head()
```


```python
# ── JE Test 1: Round-amount entries ──────────────────────────────────────────
# Entries that are multiples of 50,000 are suspicious
threshold = 50_000
round_mask = (jv_df['amount'] % threshold == 0) & (jv_df['amount'] >= threshold)
round_je   = jv_df[round_mask].copy()

print(f'JE Test 1 — Round amount entries (multiples of ₹{threshold:,})')
print(f'  Count : {len(round_je):,} ({len(round_je)/len(jv_df)*100:.1f}% of total)')
print(f'  Value : ₹{round_je["amount"].sum():,.0f}')
print()
print('Sample round entries:')
print(round_je[['je_number', 'date', 'user', 'amount', 'narration']]
      .sort_values('amount', ascending=False).head(8).to_string(index=False))
```


```python
# ── JE Test 2: Weekend / holiday entries ─────────────────────────────────────
weekend_je = jv_df[jv_df['weekday'].isin(['Saturday', 'Sunday'])]

print('JE Test 2 — Entries posted on weekends')
print(f'  Count : {len(weekend_je)}')
print()
print(weekend_je[['je_number', 'date', 'weekday', 'user', 'amount', 'narration']]
      .to_string(index=False))
```


```python
# ── JE Test 3: Period-end concentration ──────────────────────────────────────
# Entries in last 5 days of the year
cutoff = pd.Timestamp('2025-03-27')
period_end_je = jv_df[jv_df['date'] >= cutoff]

print(f'JE Test 3 — Entries in last 5 days (from {cutoff.date()})')
print(f'  Count : {len(period_end_je)}')
print(f'  Value : ₹{period_end_je["amount"].sum():,.0f}')
print(f'  As % of total value: {period_end_je["amount"].sum()/jv_df["amount"].sum()*100:.1f}%')
print()
print(period_end_je[['je_number', 'date', 'user', 'dr_account', 'cr_account', 'amount', 'narration']]
      .sort_values('amount', ascending=False).to_string(index=False))
```


```python
# ── JE Test 4: User activity analysis ────────────────────────────────────────
user_summary = (
    jv_df.groupby('user')['amount']
    .agg(count='count', total='sum', avg='mean', max_entry='max')
    .sort_values('total', ascending=False)
    .round(0)
)
print('JE Test 4 — Journal entry activity by user:')
print(user_summary.map(lambda x: f'₹{x:>12,.0f}' if x > 100 else str(x)))

# Flag: 'admin' entries (generic user = high risk)
admin_je = jv_df[jv_df['user'] == 'admin']
print(f'\n⚠️  Admin user entries: {len(admin_je)} (Value: ₹{admin_je["amount"].sum():,.0f})')
print('   Generic user IDs mask individual accountability — SA 240 risk factor')
```


```python
# ── Visualise: JE monthly volume and value ────────────────────────────────────
monthly_je = (
    jv_df.groupby(jv_df['date'].dt.to_period('M'))
    .agg(count=('je_number','count'), total_value=('amount','sum'))
    .reset_index()
)
monthly_je['period_str'] = monthly_je['date'].astype(str)

fig, axes = plt.subplots(2, 1, figsize=(13, 8), sharex=True)

axes[0].bar(monthly_je['period_str'], monthly_je['count'], color='steelblue')
axes[0].set_title('Monthly Journal Entry Count', fontweight='bold')
axes[0].set_ylabel('Number of JEs')
axes[0].axhline(monthly_je['count'].mean(), color='red', linestyle='--', label='Average')
axes[0].legend()

axes[1].bar(monthly_je['period_str'], monthly_je['total_value']/1e5, color='coral')
axes[1].set_title('Monthly Journal Entry Value (₹ Lakhs)', fontweight='bold')
axes[1].set_ylabel('₹ Lakhs')
axes[1].axhline(monthly_je['total_value'].mean()/1e5, color='red', linestyle='--', label='Average')
axes[1].tick_params(axis='x', rotation=45)
axes[1].legend()

plt.suptitle('Journal Entry Analysis — FY 2024-25', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()
```

---
## Part 3: Accounts Receivable Aging


```python
# ── AR Dataset ───────────────────────────────────────────────────────────────
customers = [
    'Infosys BPO Ltd', 'Tech Mahindra Ltd', 'Wipro Technologies', 'HCL Services',
    'TCS Consulting', 'Cognizant India', 'Mphasis Ltd', 'Hexaware Technologies',
    'Cyient Ltd', 'NIIT Technologies', 'Zensar Technologies', 'Persistent Systems',
    'KPIT Tech', 'Tata Elxsi', 'Sasken Technologies', 'Sonata Software',
]

np.random.seed(99)
n_ar = 120
invoice_dates_ar = [REPORT_DATE - timedelta(days=int(d))
                    for d in np.random.randint(1, 200, n_ar)]
due_dates_ar     = [inv + timedelta(days=np.random.choice([30, 45, 60]))
                    for inv in invoice_dates_ar]

ar_df = pd.DataFrame({
    'customer'     : np.random.choice(customers, n_ar),
    'invoice_no'   : [f'INV-{i:04d}' for i in range(1, n_ar+1)],
    'invoice_date' : invoice_dates_ar,
    'due_date'     : due_dates_ar,
    'amount'       : np.random.lognormal(11, 1, n_ar).round(-3).clip(5000, 50_00_000),
    'currency'     : 'INR',
})

ar_df['invoice_date'] = pd.to_datetime(ar_df['invoice_date'])
ar_df['due_date']     = pd.to_datetime(ar_df['due_date'])
ar_df['days_outstanding'] = (pd.Timestamp(REPORT_DATE) - ar_df['invoice_date']).dt.days
ar_df['days_overdue']     = (pd.Timestamp(REPORT_DATE) - ar_df['due_date']).dt.days
ar_df['days_overdue']     = ar_df['days_overdue'].clip(lower=0)  # 0 if not yet due

print(f'AR Ledger: {len(ar_df)} open invoices')
print(f'Total AR : ₹{ar_df["amount"].sum()/1e5:.2f} Lakhs')
ar_df.head()
```


```python
# ── Aging bucket function ─────────────────────────────────────────────────────
def aging_bucket(days_outstanding):
    if days_outstanding <= 30:   return '0-30 days'
    elif days_outstanding <= 60: return '31-60 days'
    elif days_outstanding <= 90: return '61-90 days'
    elif days_outstanding <= 120:return '91-120 days'
    else:                        return '>120 days'

ar_df['aging_bucket'] = ar_df['days_outstanding'].apply(aging_bucket)

# Provision rate per bucket (standard provisioning policy)
provision_rates = {
    '0-30 days'  : 0.00,
    '31-60 days' : 0.05,
    '61-90 days' : 0.15,
    '91-120 days': 0.30,
    '>120 days'  : 0.50,
}
ar_df['provision_rate'] = ar_df['aging_bucket'].map(provision_rates)
ar_df['provision_amt']  = ar_df['amount'] * ar_df['provision_rate']

# ── Aging Summary ─────────────────────────────────────────────────────────────
bucket_order = ['0-30 days', '31-60 days', '61-90 days', '91-120 days', '>120 days']

aging_summary = (
    ar_df.groupby('aging_bucket')
    .agg(
        invoices    = ('invoice_no', 'count'),
        gross_amount= ('amount', 'sum'),
        provision   = ('provision_amt', 'sum')
    )
    .reindex(bucket_order)
    .assign(net_realizable = lambda d: d['gross_amount'] - d['provision'])
)

aging_summary['% of total'] = aging_summary['gross_amount'] / aging_summary['gross_amount'].sum() * 100

print('=== ACCOUNTS RECEIVABLE AGING ANALYSIS ===')
print(f'As at: {REPORT_DATE}')
print()
print(aging_summary.map(lambda x: f'{x:>12,.0f}' if isinstance(x, float) and x > 1 else x))
```


```python
# ── Customer-wise Aging ───────────────────────────────────────────────────────
customer_aging = (
    ar_df.pivot_table(
        values='amount', index='customer', columns='aging_bucket',
        aggfunc='sum', fill_value=0
    )
    .reindex(columns=bucket_order, fill_value=0)
)
customer_aging['Total']    = customer_aging.sum(axis=1)
customer_aging['Provision']= (ar_df.groupby('customer')['provision_amt'].sum())
customer_aging = customer_aging.sort_values('Total', ascending=False)

print('Customer-wise AR Aging (₹):')
print(customer_aging.head(10).map(lambda x: f'₹{x:>10,.0f}' if pd.notna(x) else '—'))

# Highlight high-risk customers
ar_df['high_risk'] = ar_df['days_outstanding'] > 90
high_risk_cust = (
    ar_df[ar_df['high_risk']]
    .groupby('customer')['amount']
    .agg(invoices='count', overdue_amount='sum')
    .sort_values('overdue_amount', ascending=False)
)
print('\n⚠️ High-risk customers (>90 days outstanding):')
print(high_risk_cust.head(5).map(lambda x: f'₹{x:>10,.0f}' if x > 100 else str(x)))
```


```python
# ── Visualise AR Aging ────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart — amount by bucket
colours = ['#4CAF50', '#8BC34A', '#FF9800', '#FF5722', '#B71C1C']
axes[0].bar(bucket_order, aging_summary['gross_amount']/1e5, color=colours)
axes[0].set_title('AR Outstanding by Aging Bucket (₹ Lakhs)', fontweight='bold')
axes[0].set_ylabel('₹ Lakhs')
axes[0].tick_params(axis='x', rotation=15)
for i, (bucket, row) in enumerate(aging_summary.iterrows()):
    axes[0].text(i, row['gross_amount']/1e5 + 0.5, f'{row["%  of total"]:.1f}%',
                 ha='center', fontsize=9)

# Stacked bar — customer top 8 breakdown
top8_customers = customer_aging.head(8).drop(columns=['Total', 'Provision'])
top8_customers = top8_customers / 1e5  # convert to Lakhs
top8_customers.plot(kind='barh', stacked=True, color=colours, ax=axes[1])
axes[1].set_title('Top 8 Customers: AR by Aging Bucket (₹ Lakhs)', fontweight='bold')
axes[1].set_xlabel('₹ Lakhs')
axes[1].legend(title='Bucket', fontsize=8, loc='lower right')

plt.tight_layout()
plt.show()
```

---
## Part 4: Accounts Payable Aging


```python
# ── AP Dataset ───────────────────────────────────────────────────────────────
vendors = [
    'Microsoft India', 'AWS India Pvt Ltd', 'Salesforce India', 'Cisco Systems',
    'HP India Sales', 'Oracle India', 'SAP India', 'Lenovo India',
    'Dell Technologies', 'Accenture Services',
]

np.random.seed(77)
n_ap = 80
inv_dates_ap = [REPORT_DATE - timedelta(days=int(d))
                for d in np.random.randint(1, 150, n_ap)]
payment_terms_ap = np.random.choice([30, 45, 60], n_ap)
due_dates_ap     = [inv + timedelta(days=int(pt))
                    for inv, pt in zip(inv_dates_ap, payment_terms_ap)]

ap_df = pd.DataFrame({
    'vendor'         : np.random.choice(vendors, n_ap),
    'invoice_no'     : [f'PIN-{i:04d}' for i in range(1, n_ap+1)],
    'invoice_date'   : pd.to_datetime(inv_dates_ap),
    'due_date'       : pd.to_datetime(due_dates_ap),
    'amount'         : np.random.lognormal(11.5, 0.9, n_ap).round(-3).clip(5000, 1_00_00_000),
    'payment_terms'  : payment_terms_ap,
})

ap_df['days_since_invoice'] = (pd.Timestamp(REPORT_DATE) - ap_df['invoice_date']).dt.days
ap_df['days_overdue']       = (pd.Timestamp(REPORT_DATE) - ap_df['due_date']).dt.days
ap_df['overdue']            = ap_df['days_overdue'] > 0
ap_df['days_overdue_pos']   = ap_df['days_overdue'].clip(lower=0)
ap_df['aging_bucket']       = ap_df['days_since_invoice'].apply(aging_bucket)

# Penalty for late payment (typically 18% p.a. per vendor contracts)
ap_df['late_payment_charge'] = np.where(
    ap_df['overdue'],
    ap_df['amount'] * 0.18 * ap_df['days_overdue_pos'] / 365,
    0
).round(0)

print(f'AP Ledger: {len(ap_df)} open invoices')
print(f'Total AP : ₹{ap_df["amount"].sum()/1e5:.2f} Lakhs')
print(f'Overdue  : {ap_df["overdue"].sum()} invoices  (₹{ap_df[ap_df["overdue"]]["amount"].sum()/1e5:.1f}L)')

ap_summary = (
    ap_df.groupby('aging_bucket')
    .agg(
        invoices=('invoice_no','count'),
        gross_amount=('amount','sum'),
        late_charge=('late_payment_charge','sum')
    )
    .reindex(bucket_order)
)
print('\nAP Aging Summary:')
print(ap_summary.map(lambda x: f'₹{x:>12,.0f}' if isinstance(x, float) else str(x)))
```

---
## Part 5: Bank Reconciliation


```python
# ── Bank Statement and Cash Book ─────────────────────────────────────────────
# In a BRS: Cash Book = company records; Bank Statement = bank's records
# Differences arise due to: timing, errors, bank charges, uncleared cheques

np.random.seed(55)
march_start = date(2025, 3, 1)

def gen_bank_date(n):
    return [march_start + timedelta(days=int(d)) for d in np.random.randint(0, 30, n)]

# Cash Book entries (company's ledger)
n_cb = 60
cash_book = pd.DataFrame({
    'cb_ref'  : [f'CB-{i:04d}' for i in range(1, n_cb+1)],
    'date'    : gen_bank_date(n_cb),
    'narration': np.random.choice([
        'Customer payment received', 'Vendor payment made',
        'Salary transfer', 'Tax payment', 'Expenses paid'
    ], n_cb),
    'dr'      : np.where(np.random.rand(n_cb) > 0.4,
                         np.random.lognormal(10.5, 1, n_cb).round(-2), 0),
    'cr'      : 0,
})
# Assign credit entries to rows that don't have debits
cash_book.loc[cash_book['dr'] == 0, 'cr'] = \
    np.random.lognormal(10.2, 0.9, (cash_book['dr']==0).sum()).round(-2)

cash_book['amount']      = cash_book['dr'] - cash_book['cr']
cb_closing = cash_book['amount'].sum()

# Bank Statement (bank's records)
# Most entries match, but some are timing differences
# Generate bank entries: ~85% overlap + 15% unique
n_matched    = 51   # 85% of 60
n_bank_only  = 6    # bank charges, direct credits not in CB

bank_stmt = pd.DataFrame({
    'bs_ref'   : [f'BS-{i:04d}' for i in range(1, n_matched + n_bank_only + 1)],
    'date'     : gen_bank_date(n_matched + n_bank_only),
    'narration': np.concatenate([
        cash_book.iloc[:n_matched]['narration'].values,
        ['Bank charges', 'RTGS inward', 'Interest credit', 'NEFT charge',
         'Cheque return charge', 'Direct deposit']
    ]),
    'dr'       : np.concatenate([cash_book.iloc[:n_matched]['dr'].values,
                                  [500, 0, 0, 250, 800, 0]]),
    'cr'       : np.concatenate([cash_book.iloc[:n_matched]['cr'].values,
                                  [0, 2_50_000, 18_500, 0, 0, 75_000]]),
})
bank_stmt['amount']  = bank_stmt['dr'] - bank_stmt['cr']
bs_closing           = bank_stmt['amount'].sum()

# Uncleared cheques (CB has them but bank doesn't yet)
uncleared_cheques = cash_book.iloc[n_matched:n_matched+5].copy()
uncleared_value   = uncleared_cheques['cr'].sum()  # payments issued but not cleared

print('=== BANK RECONCILIATION STATEMENT ===')
print(f'Month: March 2025')
print(f'Account: HDFC Bank — Current A/c No. XXXX1234')
print()
print(f'Cash Book Closing Balance  : ₹{cb_closing:>15,.0f}')
print(f'Bank Statement Balance     : ₹{bs_closing:>15,.0f}')
print(f'Gross Difference           : ₹{cb_closing - bs_closing:>15,.0f}')
```


```python
# ── Formal BRS ────────────────────────────────────────────────────────────────
bank_stmt_balance = bs_closing

# Adjustments to bank statement to arrive at cash book balance
uncleared_chqs  = -uncleared_value           # cheques issued not yet presented
bank_only_items = -(2_50_000 + 18_500 + 75_000 - 500 - 250 - 800)  # bank entries not in CB

print('BANK RECONCILIATION STATEMENT')
print('As at 31 March 2025')
print('='*55)
print(f'Balance as per Bank Statement       : ₹{bank_stmt_balance:>12,.0f}')
print()
print('ADD: Cheques issued but not cleared')
for _, row in uncleared_cheques.iterrows():
    print(f'  {row["cb_ref"]}  {row["narration"][:25]:<25}  ₹{row["cr"]:>10,.0f}')
print(f'  Sub-total                           ₹{uncleared_value:>12,.0f}')
print()
print('LESS: Deposits in Bank not in CB')
print(f'  RTGS inward credit                  ₹{2_50_000:>12,.0f}')
print(f'  Interest credited by bank           ₹{18_500:>12,.0f}')
print(f'  Direct deposit received             ₹{75_000:>12,.0f}')
print()
print('ADD: Bank charges not in CB')
print(f'  Bank charges + NEFT + Cheque return ₹{1_550:>12,.0f}')

adjusted_balance = bank_stmt_balance + uncleared_value - (2_50_000 + 18_500 + 75_000) + 1_550
print('='*55)
print(f'Adjusted Balance (= Cash Book Balance): ₹{cb_closing:>12,.0f}')
print(f'Computed Adjusted Balance:              ₹{adjusted_balance:>12,.0f}')
diff = cb_closing - adjusted_balance
print(f'Unexplained difference:                 ₹{diff:>12,.0f}  ← {"✅ Reconciled" if abs(diff) < 100 else "❌ Investigate"}')
```

---
## Part 6: Ledger Scrutiny — Unusual Pattern Detection


```python
# ── Generate a detailed ledger for one account ────────────────────────────────
# Focus: Miscellaneous Expenses A/c (5012) — typically a catch-all account
np.random.seed(33)
n_misc = 80

misc_narrations = [
    'Office supplies purchased', 'Staff refreshments', 'Courier charges',
    'Petty cash reimbursement', 'Cleaning charges', 'Tea/coffee expenses',
    'Miscellaneous charges', 'Subscription renewal', 'Stationery purchase',
    'Festival gifts — staff',
]

misc_amounts = np.concatenate([
    np.random.lognormal(7.5, 0.8, 72).round(0).clip(200, 50_000),  # normal
    [5_00_000, 8_00_000, 12_00_000, 3_50_000,                       # large anomalies
     25_000, 75_000, 45_000, 55_000]                                # borderline
])

misc_dates = random_dates(fy_start, fy_end, n_misc)

misc_ledger = pd.DataFrame({
    'date'    : pd.to_datetime(misc_dates),
    'voucher' : [f'PV-{i:04d}' for i in range(1, n_misc+1)],
    'user'    : np.random.choice(['rajesh.k', 'sunita.j', 'admin', 'priya.s'], n_misc),
    'narration': np.random.choice(misc_narrations, n_misc),
    'dr'      : misc_amounts,
    'cr'      : 0,
})

misc_ledger = misc_ledger.sort_values('date').reset_index(drop=True)
misc_ledger['running_balance'] = misc_ledger['dr'].cumsum()

print(f'Misc Expenses Ledger: {len(misc_ledger)} entries')
print(f'Total debit: ₹{misc_ledger["dr"].sum():,.0f}')
print(f'Budget for misc: ₹1,20,000 (standard for this size company)')
print()

# Flag high-value entries
threshold_misc = misc_ledger['dr'].quantile(0.95)
high_misc = misc_ledger[misc_ledger['dr'] > threshold_misc]
print(f'High-value entries (>95th percentile = ₹{threshold_misc:,.0f}):')
print(high_misc[['date', 'voucher', 'user', 'narration', 'dr']]
      .to_string(index=False))
```


```python
# ── Narration frequency analysis ─────────────────────────────────────────────
# Vague narrations = risk of misclassification / dummy entries
vague_keywords = ['misc', 'miscellaneous', 'others', 'charges', 'various', 'general']
vague_mask = misc_ledger['narration'].str.lower().str.contains('|'.join(vague_keywords))

vague_entries = misc_ledger[vague_mask]
print(f'Entries with vague narrations: {len(vague_entries)}')
print(f'Amount: ₹{vague_entries["dr"].sum():,.0f}')

# Narration frequency
narr_freq = misc_ledger['narration'].value_counts()
print('\nTop narrations:')
print(narr_freq.head(8))

# ── Visualise ledger pattern ───────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Running balance
axes[0].plot(misc_ledger['date'], misc_ledger['running_balance']/1e5,
             color='steelblue', linewidth=1.5)
axes[0].axhline(1.2, color='red', linestyle='--', linewidth=1.5, label='Budget ₹1.2L')
axes[0].set_title('Misc Expenses — Running Balance vs Budget', fontweight='bold')
axes[0].set_ylabel('Cumulative Amount (₹ Lakhs)')
axes[0].set_xlabel('Date')
axes[0].legend()
axes[0].tick_params(axis='x', rotation=30)

# Amount distribution
sns.histplot(misc_ledger['dr'], bins=20, ax=axes[1], color='coral', kde=True)
axes[1].axvline(threshold_misc, color='red', linestyle='--',
                label=f'95th pct: ₹{threshold_misc:,.0f}')
axes[1].set_title('Distribution of Misc Expense Amounts', fontweight='bold')
axes[1].set_xlabel('Amount (₹)')
axes[1].set_ylabel('Frequency')
axes[1].legend()

plt.tight_layout()
plt.show()
```

---
## Part 7: Period-End Accrual Analysis

**SA 560 (Subsequent Events) & SA 520 (Analytical Procedures)**: Year-end accruals and provisions are a key area of manipulation. Auditors focus on:
- Large entries in the last 5 working days
- Accruals reversed in April (next year) — indicates opportunistic timing
- Provisions without supporting documentation


```python
# ── Period-end entries (March 25-31) ─────────────────────────────────────────
period_end_entries = pd.DataFrame({
    'date'       : pd.to_datetime(['2025-03-25', '2025-03-26', '2025-03-27',
                                    '2025-03-28', '2025-03-29', '2025-03-31',
                                    '2025-03-31', '2025-03-31', '2025-03-31']),
    'je_number'  : ['JE-Y001','JE-Y002','JE-Y003','JE-Y004','JE-Y005',
                    'JE-Y006','JE-Y007','JE-Y008','JE-Y009'],
    'type'       : ['Provision', 'Accrual', 'Accrual', 'Write-off', 'Provision',
                    'Accrual', 'Provision', 'Accrual', 'Write-off'],
    'dr_account' : ['5010','5001','5007','5012','5033','5003','5010','5002','5012'],
    'amount'     : [5_00_000, 12_00_000, 3_50_000, 8_00_000, 2_50_000,
                    4_80_000, 1_80_000, 6_50_000, 3_20_000],
    'user'       : ['admin','priya.s','admin','rajesh.k','admin',
                    'sunita.j','admin','amit.v','admin'],
    'narration'  : [
        'Provision for doubtful debts FY25',
        'Accrual for services received — pending invoices',
        'Professional fees accrual — Dec-Mar',
        'Write-off of old unrecoverable advances',
        'Provision for warranty claims',
        'Rent accrual — pending March invoice',
        'Provision for bad debts — new customer',
        'Bonus accrual FY25 — pending HR approval',
        'Miscellaneous write-offs — year-end cleaning',
    ],
    'reversal_in_april': [False, True, True, False, False, True, False, True, False],
})

print('=== PERIOD-END ACCRUAL ANALYSIS ===')
print(f'Entries in last 7 days of FY: {len(period_end_entries)}')
print(f'Total value: ₹{period_end_entries["amount"].sum():,.0f}')
print()
print(period_end_entries[['date','je_number','type','amount','user','reversal_in_april','narration']]
      .to_string(index=False))
```


```python
# ── Risk Assessment ───────────────────────────────────────────────────────────
# Entries that will be reversed in April are genuine accruals
# Entries NOT reversed = should be supported by documentation

genuine_accruals = period_end_entries[period_end_entries['reversal_in_april'] == True]
permanent_entries = period_end_entries[period_end_entries['reversal_in_april'] == False]

print('RISK CLASSIFICATION')
print()
print(f'Genuine accruals (will reverse in April): {len(genuine_accruals)}')
print(f'Value: ₹{genuine_accruals["amount"].sum():,.0f}')
print(genuine_accruals[['je_number', 'amount', 'narration']].to_string(index=False))

print()
print(f'⚠️  Permanent entries (no reversal — require strong documentation): {len(permanent_entries)}')
print(f'Value: ₹{permanent_entries["amount"].sum():,.0f}')
print(permanent_entries[['je_number', 'type', 'amount', 'user', 'narration']].to_string(index=False))

print()
admin_year_end = period_end_entries[period_end_entries['user'] == 'admin']
print(f'⚠️  Admin user entries at year-end: {len(admin_year_end)} (₹{admin_year_end["amount"].sum():,.0f})')
print('   → Request justification and supporting documents for each')
```

---
## Part 8: Consolidated Audit Risk Dashboard


```python
# ── Compile all risk flags ────────────────────────────────────────────────────
risk_flags = [
    {
        'area'         : 'Trial Balance',
        'finding'      : f'Debit-Credit difference: ₹{abs(diff):,.0f}',
        'risk_level'   : 'HIGH' if abs(diff) > 0 else 'LOW',
        'amount'       : abs(diff),
        'action'       : 'Investigate unbalanced entries; check data import'
    },
    {
        'area'         : 'Journal Entries — Round Amounts',
        'finding'      : f'{len(round_je)} entries (₹{round_je["amount"].sum()/1e5:.1f}L)',
        'risk_level'   : 'MEDIUM',
        'amount'       : round_je['amount'].sum(),
        'action'       : 'Sample 10 entries; verify underlying support'
    },
    {
        'area'         : 'Journal Entries — Weekend',
        'finding'      : f'{len(weekend_je)} entries by {weekend_je["user"].nunique()} users',
        'risk_level'   : 'MEDIUM',
        'amount'       : weekend_je['amount'].sum(),
        'action'       : 'Confirm business need; review authorisation'
    },
    {
        'area'         : 'Journal Entries — Admin User',
        'finding'      : f'{len(admin_je)} entries by generic "admin" ID',
        'risk_level'   : 'HIGH',
        'amount'       : admin_je['amount'].sum(),
        'action'       : 'Identify actual preparer; review access controls'
    },
    {
        'area'         : 'AR Aging — Overdue >90 days',
        'finding'      : f'₹{ar_df[ar_df["days_outstanding"]>90]["amount"].sum()/1e5:.1f}L outstanding',
        'risk_level'   : 'HIGH',
        'amount'       : ar_df[ar_df['days_outstanding']>90]['amount'].sum(),
        'action'       : 'Assess recoverability; review provision adequacy'
    },
    {
        'area'         : 'AP Aging — Overdue invoices',
        'finding'      : f'{ap_df["overdue"].sum()} invoices, ₹{ap_df[ap_df["overdue"]]["amount"].sum()/1e5:.1f}L',
        'risk_level'   : 'MEDIUM',
        'amount'       : ap_df[ap_df['overdue']]['amount'].sum(),
        'action'       : 'Review vendor payment terms; compute late payment charges'
    },
    {
        'area'         : 'Misc Expenses — High Value',
        'finding'      : f'{len(high_misc)} entries above ₹{threshold_misc:,.0f}',
        'risk_level'   : 'HIGH',
        'amount'       : high_misc['dr'].sum(),
        'action'       : 'Vouch each entry against supporting bills/approvals'
    },
    {
        'area'         : 'Period-End — Admin entries',
        'finding'      : f'{len(admin_year_end)} entries totalling ₹{admin_year_end["amount"].sum()/1e5:.1f}L',
        'risk_level'   : 'HIGH',
        'amount'       : admin_year_end['amount'].sum(),
        'action'       : 'Obtain Board/Audit Committee approval for each provision'
    },
]

risk_df = pd.DataFrame(risk_flags)
risk_df['amount_lakhs'] = risk_df['amount'] / 1e5

# Colour code
risk_colour = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
risk_df['flag'] = risk_df['risk_level'].map(risk_colour)

print('=== AUDIT RISK DASHBOARD ===')
print(f'Meridian Consulting & Services Pvt. Ltd.')
print(f'FY 2024-25 | Prepared on: {REPORT_DATE}')
print()
for _, row in risk_df.iterrows():
    print(f'{row["flag"]} {row["risk_level"]:6s} | {row["area"]}')
    print(f'         Finding: {row["finding"]}')
    print(f'         Action : {row["action"]}')
    print()
```


```python
# ── Risk Dashboard Visual ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Risk count by level
risk_counts = risk_df['risk_level'].value_counts()
colours_risk = {'HIGH': '#C62828', 'MEDIUM': '#F57F17', 'LOW': '#2E7D32'}
bar_colors   = [colours_risk.get(r, 'grey') for r in risk_counts.index]

axes[0].bar(risk_counts.index, risk_counts.values, color=bar_colors, edgecolor='white')
axes[0].set_title('Risk Flags by Severity', fontweight='bold', fontsize=12)
axes[0].set_ylabel('Count')
for i, (lvl, cnt) in enumerate(risk_counts.items()):
    axes[0].text(i, cnt + 0.1, str(cnt), ha='center', fontweight='bold', fontsize=14)
axes[0].set_ylim(0, risk_counts.max() + 1.5)

# Amount at risk by area
risk_sorted = risk_df.sort_values('amount_lakhs', ascending=True)
bar_cols = [colours_risk.get(r, 'grey') for r in risk_sorted['risk_level']]

axes[1].barh(risk_sorted['area'], risk_sorted['amount_lakhs'], color=bar_cols)
axes[1].set_title('Amount at Risk by Finding (₹ Lakhs)', fontweight='bold', fontsize=12)
axes[1].set_xlabel('₹ Lakhs')
axes[1].tick_params(axis='y', labelsize=8)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colours_risk[k], label=k) for k in colours_risk]
axes[1].legend(handles=legend_elements, loc='lower right', fontsize=9)

plt.suptitle('Meridian Consulting — FY 2024-25 Audit Risk Dashboard',
             fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
plt.show()
```


```python
# ── Export Risk Report ────────────────────────────────────────────────────────
print('=== SUMMARY STATISTICS ===')
print(f'Total risk items identified : {len(risk_df)}')
print(f'High risk items             : {(risk_df["risk_level"]=="HIGH").sum()}')
print(f'Medium risk items           : {(risk_df["risk_level"]=="MEDIUM").sum()}')
print(f'Total amount at risk        : ₹{risk_df["amount_lakhs"].sum():.1f} Lakhs')
print()
print('TOP PRIORITY ACTIONS:')
for _, row in risk_df[risk_df['risk_level'] == 'HIGH'].iterrows():
    print(f'  → [{row["area"]}] {row["action"]}')
```

---
## Key Takeaways for CA Practitioners

| Analysis | Tool Used | CA Standard |
|---|---|---|
| Trial Balance validation | `df.sum()`, Boolean checks | SA 520 |
| Journal entry testing | Boolean filters, `groupby` | SA 240, SA 315 |
| AR/AP Aging | Custom `aging_bucket()`, `pivot_table` | SA 505, ICAI guidance |
| Bank Reconciliation | Arithmetic matching | SA 501 |
| Ledger scrutiny | `quantile()`, pattern analysis | SA 520 |
| Period-end accruals | Date filtering, risk scoring | SA 560 |
| Risk dashboard | `seaborn`, `matplotlib` | SA 300 (Audit Planning) |

### What would take 5 days manually... now takes 5 minutes with Python.

---
## Practice Exercises

1. Modify the `aging_bucket()` function to create 6 buckets: 0-15, 16-30, 31-60, 61-90, 91-120, >120 days.

2. Add a `doubtful_debt_risk` column to the AR DataFrame: 'Low' if <60 days, 'Medium' if 61-120, 'High' if >120 days.

3. Identify all journal entries where the same account is both debited and credited (self-referencing entries — a red flag).

4. Compute the Days Sales Outstanding (DSO) = `(Total AR / Annual Revenue) × 365` using the TB figures.

5. Create a heatmap showing journal entry volume by user and month — identify the months/users with unusually high activity.


```python
# ── Exercise Solutions ─────────────────────────────────────────────────────────

# Exercise 1: 6-bucket aging
def aging_bucket_6(days):
    if days <= 15:   return '0-15 days'
    elif days <= 30: return '16-30 days'
    elif days <= 60: return '31-60 days'
    elif days <= 90: return '61-90 days'
    elif days <= 120:return '91-120 days'
    else:            return '>120 days'

ar_df['aging_6'] = ar_df['days_outstanding'].apply(aging_bucket_6)
print('Exercise 1 — 6-bucket aging:')
print(ar_df['aging_6'].value_counts().sort_index())

# Exercise 2: Doubtful debt risk
ar_df['dd_risk'] = pd.cut(
    ar_df['days_outstanding'],
    bins=[0, 60, 120, np.inf],
    labels=['Low', 'Medium', 'High']
)
print('\nExercise 2 — Doubtful debt risk:')
print(ar_df.groupby('dd_risk')['amount'].agg(['count','sum']).map(
    lambda x: f'₹{x:,.0f}' if x > 100 else str(x)))

# Exercise 4: DSO
total_ar   = tb[tb['acc_code'] == '1010']['debit'].values[0]
annual_rev = tb[tb['acc_code'].isin(['4001','4002'])]['credit'].sum()
dso = total_ar / annual_rev * 365
print(f'\nExercise 4 — Days Sales Outstanding: {dso:.1f} days')
print(f'  (Industry benchmark: <45 days for consulting)')

# Exercise 5: JE heatmap by user × month
jv_pivot = jv_df.pivot_table(
    values='amount', index='user',
    columns=jv_df['date'].dt.strftime('%b'),
    aggfunc='count', fill_value=0
)
fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(jv_pivot, annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5,
            linecolor='white', ax=ax)
ax.set_title('JE Volume by User and Month — Concentration Analysis', fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('User')
plt.tight_layout()
plt.show()
```
