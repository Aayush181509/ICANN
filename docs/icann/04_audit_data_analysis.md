# Module 4: Audit Data Analysis
### Data Science for Chartered Accountants

---

## Learning Objectives
- Draw scientifically valid audit samples (random, stratified, monetary unit)
- Apply **Benford's Law** to detect anomalies in accounting data
- Identify **duplicate invoices** and **gap testing** in serial numbers
- Perform statistical outlier detection on transaction data
- Build a systematic **audit risk flag** report

---

> **CA Context:** SA 530 (Audit Sampling), SA 520 (Analytical Procedures), and SA 240 (Fraud) all require quantitative analysis. These techniques directly support evidence gathering during statutory and tax audits.


```python
import pandas as pd
import numpy as np

np.random.seed(42)
pd.set_option('display.float_format', '{:,.2f}'.format)

print('Libraries loaded. Ready for audit analysis.')
```

    Libraries loaded. Ready for audit analysis.


---
## Section 1: Generating Realistic Audit Data

We simulate the **purchase register** of a manufacturing company with 500 invoices — typical for an MSME audit.


```python
# ── Simulate Purchase Register ────────────────────────────────────────────────
n_invoices = 500

vendors     = ['Ravi Steel Ltd', 'Shiva Metals', 'Om Electricals', 'Laxmi Traders',
                'Ganesh Supplies', 'Krishna Components', 'Saraswati Hardware', 'Durga Chemicals']
categories  = ['Raw Material', 'Packing Material', 'Consumables', 'Spare Parts', 'Utilities']
approvers   = ['Manager A', 'Manager B', 'Manager C', 'Director']

# Mostly legitimate invoices, some with embedded anomalies
amounts     = np.concatenate([
    np.random.lognormal(mean=10.5, sigma=1.2, size=460),   # Normal distribution
    np.array([50000, 50000, 75000, 75000, 99999, 99999]),   # Round numbers (suspicious)
    np.array([1_00_001, 2_00_001, 4_99_999]),               # Just above approval limits
    np.array([12500, 12500, 12500]),                         # Splitting invoices
    np.random.lognormal(mean=12, sigma=0.5, size=28)        # Large invoices
])
amounts = np.clip(amounts, 1000, 20_00_000).astype(int)

# Date range: FY 2024-25 (Apr 2024 – Mar 2025)
date_range  = pd.date_range('2024-04-01', '2025-03-31', periods=n_invoices)
invoice_dates = np.sort(np.random.choice(date_range, n_invoices, replace=False))

# Insert some weekend transactions
invoice_dates_list = list(invoice_dates)
for i in [10, 50, 120, 200, 350]:   # specific positions
    # Move to nearest Sunday
    d = pd.Timestamp(invoice_dates_list[i])
    invoice_dates_list[i] = d + pd.Timedelta(days=(6 - d.dayofweek))

purchase_register = pd.DataFrame({
    'Invoice_No'  : [f'PI-{str(i).zfill(4)}' for i in range(1, n_invoices + 1)],
    'Invoice_Date': invoice_dates_list,
    'Vendor'      : np.random.choice(vendors, n_invoices, p=[0.2,0.15,0.15,0.12,0.12,0.1,0.1,0.06]),
    'Category'    : np.random.choice(categories, n_invoices),
    'Amount'      : amounts[:n_invoices],
    'GST_Amount'  : (amounts[:n_invoices] * 0.18).astype(int),
    'Approver'    : np.random.choice(approvers, n_invoices, p=[0.4,0.35,0.15,0.1]),
    'Payment_Date': pd.NaT,   # will populate below
    'Booked_By'   : np.random.choice(['User1','User2','User3'], n_invoices)
})

# Payment dates: 20-45 days after invoice
pay_delay = np.random.randint(5, 60, n_invoices)
purchase_register['Payment_Date'] = pd.to_datetime(purchase_register['Invoice_Date']) + \
                                     pd.to_timedelta(pay_delay, unit='D')

# Introduce some duplicates
dup_rows = purchase_register.iloc[[5, 12, 55]].copy()
dup_rows['Invoice_No'] = ['PI-0501', 'PI-0502', 'PI-0503']  # different voucher no, same details
purchase_register = pd.concat([purchase_register, dup_rows], ignore_index=True)

print(f'Purchase Register: {len(purchase_register)} entries')
print(f'Total Purchase Value: ₹{purchase_register["Amount"].sum():,.0f}')
purchase_register.head()
```

    Purchase Register: 503 entries
    Total Purchase Value: ₹40,615,985





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
      <th>Invoice_Date</th>
      <th>Vendor</th>
      <th>Category</th>
      <th>Amount</th>
      <th>GST_Amount</th>
      <th>Approver</th>
      <th>Payment_Date</th>
      <th>Booked_By</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PI-0001</td>
      <td>2024-04-01 00:00:00.000000000</td>
      <td>Krishna Components</td>
      <td>Packing Material</td>
      <td>65910</td>
      <td>11863</td>
      <td>Manager B</td>
      <td>2024-05-09 00:00:00.000000000</td>
      <td>User1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>PI-0002</td>
      <td>2024-04-01 17:30:25.250501002</td>
      <td>Durga Chemicals</td>
      <td>Packing Material</td>
      <td>30763</td>
      <td>5537</td>
      <td>Manager B</td>
      <td>2024-05-09 17:30:25.250501002</td>
      <td>User1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>PI-0003</td>
      <td>2024-04-02 11:00:50.501002004</td>
      <td>Krishna Components</td>
      <td>Raw Material</td>
      <td>79001</td>
      <td>14220</td>
      <td>Manager B</td>
      <td>2024-05-04 11:00:50.501002004</td>
      <td>User3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>PI-0004</td>
      <td>2024-04-03 04:31:15.751503006</td>
      <td>Ganesh Supplies</td>
      <td>Consumables</td>
      <td>225852</td>
      <td>40653</td>
      <td>Manager A</td>
      <td>2024-04-20 04:31:15.751503006</td>
      <td>User3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>PI-0005</td>
      <td>2024-04-03 22:01:41.002004008</td>
      <td>Laxmi Traders</td>
      <td>Utilities</td>
      <td>27419</td>
      <td>4935</td>
      <td>Manager A</td>
      <td>2024-04-22 22:01:41.002004008</td>
      <td>User1</td>
    </tr>
  </tbody>
</table>
</div>



---
## Section 2: Audit Sampling (SA 530)

Three sampling approaches:
1. **Simple Random Sampling** — every item has equal probability
2. **Stratified Sampling** — divide population into strata, sample each
3. **Monetary Unit Sampling (MUS)** — higher-value items get higher selection probability


```python
# ── 2.1 Simple Random Sampling ────────────────────────────────────────────────
sample_size = 50
random_sample = purchase_register.sample(n=sample_size, random_state=42)

total_pop    = purchase_register['Amount'].sum()
sample_mean  = random_sample['Amount'].mean()
pop_estimate = sample_mean * len(purchase_register)

print('SIMPLE RANDOM SAMPLE')
print(f'  Sample size     : {len(random_sample)} invoices')
print(f'  Sample total    : ₹{random_sample["Amount"].sum():,.0f}')
print(f'  Sample mean     : ₹{sample_mean:,.0f}')
print(f'  Population est. : ₹{pop_estimate:,.0f}  (vs actual ₹{total_pop:,.0f})')
error_pct = abs(pop_estimate - total_pop) / total_pop * 100
print(f'  Estimation error: {error_pct:.1f}%')
```

    SIMPLE RANDOM SAMPLE
      Sample size     : 50 invoices
      Sample total    : ₹3,077,970
      Sample mean     : ₹61,559
      Population est. : ₹30,964,378  (vs actual ₹40,615,985)
      Estimation error: 23.8%



```python
# ── 2.2 Stratified Sampling — by Amount Band ──────────────────────────────────
def assign_stratum(amount):
    if amount < 10_000:    return 'Low (<10K)'
    elif amount < 50_000:  return 'Medium (10K-50K)'
    elif amount < 2_00_000: return 'High (50K-2L)'
    else:                  return 'Very High (>2L)'

purchase_register['Stratum'] = purchase_register['Amount'].apply(assign_stratum)

# Sample 20% from each stratum
stratified_sample = purchase_register.groupby('Stratum', group_keys=False).apply(
    lambda x: x.sample(frac=0.20, random_state=42)
)

strat_summary = purchase_register.groupby('Stratum').agg(
    Population   = ('Invoice_No', 'count'),
    Pop_Amount   = ('Amount', 'sum'),
)
strat_sample_summary = stratified_sample.groupby('Stratum').agg(
    Sampled      = ('Invoice_No', 'count'),
    Sample_Amount= ('Amount', 'sum')
)

strat_report = strat_summary.join(strat_sample_summary)
strat_report['Coverage%'] = strat_report['Sample_Amount'] / strat_report['Pop_Amount'] * 100
print('STRATIFIED SAMPLING REPORT')
print(strat_report.round(1))
print(f'\nTotal sample size: {len(stratified_sample)} invoices')
print(f'Value coverage: {stratified_sample["Amount"].sum() / total_pop * 100:.1f}% of total')
```

    STRATIFIED SAMPLING REPORT
                      Population  Pop_Amount  Sampled  Sample_Amount  Coverage%
    Stratum                                                                    
    High (50K-2L)            172    16268343       34        2882584      17.70
    Low (<10K)                59      372370       12          65055      17.50
    Medium (10K-50K)         225     5905230       45        1172925      19.90
    Very High (>2L)           47    18070042        9        2991569      16.60
    
    Total sample size: 100 invoices
    Value coverage: 17.5% of total


    /var/folders/kp/mytrwq8157q9s1tmw7r79fkm0000gn/T/ipykernel_84611/1885076552.py:11: FutureWarning: DataFrameGroupBy.apply operated on the grouping columns. This behavior is deprecated, and in a future version of pandas the grouping columns will be excluded from the operation. Either pass `include_groups=False` to exclude the groupings or explicitly select the grouping columns after groupby to silence this warning.
      stratified_sample = purchase_register.groupby('Stratum', group_keys=False).apply(



```python
# ── 2.3 Monetary Unit Sampling (MUS / PPS) ────────────────────────────────────
# Every rupee has equal probability of selection — large items more likely to be sampled
sampling_interval = total_pop / sample_size  # rupee interval
random_start = np.random.uniform(0, sampling_interval)

# Create cumulative amount column
pr_sorted = purchase_register.sort_values('Amount', ascending=False).reset_index(drop=True)
pr_sorted['Cumulative'] = pr_sorted['Amount'].cumsum()

# Select: pick every (interval)-th rupee
selection_points = np.arange(random_start, total_pop, sampling_interval)
mus_sample_idx = []
for sp in selection_points:
    idx = (pr_sorted['Cumulative'] >= sp).idxmax()
    if idx not in mus_sample_idx:
        mus_sample_idx.append(idx)

mus_sample = pr_sorted.iloc[mus_sample_idx]
print('MONETARY UNIT SAMPLING (MUS)')
print(f'  Sampling Interval : ₹{sampling_interval:,.0f}')
print(f'  Random Start      : ₹{random_start:,.0f}')
print(f'  Items selected    : {len(mus_sample)}')
print(f'  Min amount sampled: ₹{mus_sample["Amount"].min():,.0f}')
print(f'  Coverage          : {mus_sample["Amount"].sum() / total_pop * 100:.1f}% of total value')
print('\nTop 10 MUS selections:')
print(mus_sample[['Invoice_No','Vendor','Amount','Category']].head(10).to_string(index=False))
```

    MONETARY UNIT SAMPLING (MUS)
      Sampling Interval : ₹812,320
      Random Start      : ₹556,800
      Items selected    : 49
      Min amount sampled: ₹8,291
      Coverage          : 31.9% of total value
    
    Top 10 MUS selections:
    Invoice_No             Vendor  Amount         Category
       PI-0210 Krishna Components 2000000      Spare Parts
       PI-0180     Ravi Steel Ltd  949986      Spare Parts
       PI-0491      Laxmi Traders  758759      Spare Parts
       PI-0114    Durga Chemicals  697941        Utilities
       PI-0221 Krishna Components  583961     Raw Material
       PI-0126     Ravi Steel Ltd  503101      Consumables
       PI-0469     Ravi Steel Ltd  499999 Packing Material
       PI-0235       Shiva Metals  475790      Consumables
       PI-0285     Om Electricals  469601     Raw Material
       PI-0324    Ganesh Supplies  447246        Utilities


---
## Section 3: Benford's Law Test

**Benford's Law** states that in naturally occurring numerical data, the **leading digit** follows a specific logarithmic distribution:

$$P(d) = \log_{10}\left(1 + \frac{1}{d}\right)$$

| Digit | Expected % |
|---|---|
| 1 | 30.1% |
| 2 | 17.6% |
| 3 | 12.5% |
| 4 | 9.7% |
| 5 | 7.9% |
| 6 | 6.7% |
| 7 | 5.8% |
| 8 | 5.1% |
| 9 | 4.6% |

> **Audit Application:** A significant deviation from Benford's distribution in invoice amounts, expense claims, or journal entries can indicate **fraud, fabricated invoices, or manipulation**.


```python
# ── 3.1 Benford's Analysis ────────────────────────────────────────────────────
def benfords_expected():
    digits = np.arange(1, 10)
    return pd.Series(np.log10(1 + 1/digits) * 100, index=digits)

def leading_digit(x):
    x = abs(x)
    while x >= 10: x /= 10
    while x < 1  : x *= 10
    return int(x)

amounts_for_benford = purchase_register['Amount'].dropna()
observed_digits = amounts_for_benford.apply(leading_digit)
observed_pct    = observed_digits.value_counts(normalize=True).sort_index() * 100
expected_pct    = benfords_expected()

benford_df = pd.DataFrame({
    'Expected %' : expected_pct,
    'Observed %' : observed_pct
}).fillna(0)
benford_df['Deviation %']  = benford_df['Observed %'] - benford_df['Expected %']
benford_df['MAD']          = abs(benford_df['Deviation %'])
benford_df['Flag']         = benford_df['MAD'].apply(lambda x: '⚠ SIGNIFICANT' if x > 5 else ('MODERATE' if x > 2 else 'OK'))

print('BENFORD\'S LAW TEST — Purchase Register')
print(benford_df.round(2))
overall_mad = benford_df['MAD'].mean()
print(f'\nMean Absolute Deviation (MAD): {overall_mad:.2f}%')
if overall_mad < 1.5:    print('Overall: CONFORMS to Benford\'s Law (low risk)')
elif overall_mad < 2.5:  print('Overall: ACCEPTABLE deviation')
else:                    print('Overall: ⚠ SIGNIFICANT deviation — further investigation recommended')
```

    BENFORD'S LAW TEST — Purchase Register
       Expected %  Observed %  Deviation %  MAD      Flag
    1       30.10       30.42         0.31 0.31        OK
    2       17.61       15.51        -2.10 2.10  MODERATE
    3       12.49       12.52         0.03 0.03        OK
    4        9.69       10.14         0.45 0.45        OK
    5        7.92        9.15         1.23 1.23        OK
    6        6.69        6.36        -0.33 0.33        OK
    7        5.80        5.77        -0.03 0.03        OK
    8        5.12        5.17         0.05 0.05        OK
    9        4.58        4.97         0.39 0.39        OK
    
    Mean Absolute Deviation (MAD): 0.55%
    Overall: CONFORMS to Benford's Law (low risk)



```python
# ── 3.2 Vendor-wise Benford Test ──────────────────────────────────────────────
print('BENFORD TEST — VENDOR WISE')
print(f'{"Vendor":<25} {"Count":>6} {"MAD%":>8} {"Result":>15}')
print('-' * 60)
for vendor in vendors:
    vdata = purchase_register[purchase_register['Vendor'] == vendor]['Amount']
    if len(vdata) < 20:   # Need sufficient data for Benford's
        continue
    vdigits  = vdata.apply(leading_digit)
    vobs_pct = vdigits.value_counts(normalize=True).reindex(range(1,10), fill_value=0).sort_index() * 100
    vmad     = abs(vobs_pct - expected_pct).mean()
    result   = '⚠ FLAG' if vmad > 3 else 'OK'
    print(f'{vendor:<25} {len(vdata):>6}  {vmad:>7.2f}%  {result:>15}')
```

    BENFORD TEST — VENDOR WISE
    Vendor                     Count     MAD%          Result
    ------------------------------------------------------------
    Ravi Steel Ltd               103     2.13%               OK
    Shiva Metals                  61     2.39%               OK
    Om Electricals                75     3.70%           ⚠ FLAG
    Laxmi Traders                 75     1.47%               OK
    Ganesh Supplies               57     3.49%           ⚠ FLAG
    Krishna Components            48     3.24%           ⚠ FLAG
    Saraswati Hardware            48     2.78%               OK
    Durga Chemicals               36     3.34%           ⚠ FLAG


---
## Section 4: Duplicate Invoice Detection

> **Audit Risk:** Duplicate payments are one of the most common errors/frauds in accounts payable. SA 240 requires auditors to be alert to duplicate entries.


```python
# ── 4.1 Exact Duplicates (same vendor + amount + date) ───────────────────────
dup_check = purchase_register.copy()
dup_check['Invoice_Date'] = pd.to_datetime(dup_check['Invoice_Date'])

# Method 1: Exact match on vendor + amount + date
exact_dups = dup_check[
    dup_check.duplicated(subset=['Vendor', 'Amount', 'Invoice_Date'], keep=False)
].sort_values(['Vendor', 'Amount', 'Invoice_Date'])

print(f'EXACT DUPLICATES (same vendor + amount + date): {len(exact_dups)} records')
if not exact_dups.empty:
    print(exact_dups[['Invoice_No','Invoice_Date','Vendor','Amount','Approver']].to_string(index=False))
```

    EXACT DUPLICATES (same vendor + amount + date): 6 records
    Invoice_No                  Invoice_Date          Vendor  Amount  Approver
       PI-0013 2024-04-09 18:05:03.006012024 Durga Chemicals   48550  Director
       PI-0502 2024-04-09 18:05:03.006012024 Durga Chemicals   48550  Director
       PI-0006 2024-04-04 15:32:06.252505010  Ravi Steel Ltd   27420 Manager C
       PI-0501 2024-04-04 15:32:06.252505010  Ravi Steel Ltd   27420 Manager C
       PI-0056 2024-05-11 02:53:08.777555110  Ravi Steel Ltd  111027 Manager B
       PI-0503 2024-05-11 02:53:08.777555110  Ravi Steel Ltd  111027 Manager B



```python
# ── 4.2 Near-Duplicates (same vendor + same amount within 7 days) ─────────────
pr_sorted2 = dup_check.sort_values(['Vendor', 'Amount', 'Invoice_Date']).reset_index(drop=True)

near_dups = []
for i in range(len(pr_sorted2) - 1):
    row1 = pr_sorted2.iloc[i]
    row2 = pr_sorted2.iloc[i+1]
    if (row1['Vendor'] == row2['Vendor'] and
        row1['Amount'] == row2['Amount'] and
        abs((pd.Timestamp(row2['Invoice_Date']) - pd.Timestamp(row1['Invoice_Date'])).days) <= 7):
        near_dups.append({
            'Invoice_1'  : row1['Invoice_No'],
            'Invoice_2'  : row2['Invoice_No'],
            'Vendor'     : row1['Vendor'],
            'Amount'     : row1['Amount'],
            'Date_1'     : row1['Invoice_Date'],
            'Date_2'     : row2['Invoice_Date'],
            'Days_Apart' : abs((pd.Timestamp(row2['Invoice_Date']) - pd.Timestamp(row1['Invoice_Date'])).days)
        })

near_dup_df = pd.DataFrame(near_dups)
print(f'NEAR-DUPLICATES (same vendor+amount, within 7 days): {len(near_dup_df)} pairs')
if not near_dup_df.empty:
    print(near_dup_df.to_string(index=False))
```

    NEAR-DUPLICATES (same vendor+amount, within 7 days): 3 pairs
    Invoice_1 Invoice_2          Vendor  Amount                        Date_1                        Date_2  Days_Apart
      PI-0013   PI-0502 Durga Chemicals   48550 2024-04-09 18:05:03.006012024 2024-04-09 18:05:03.006012024           0
      PI-0006   PI-0501  Ravi Steel Ltd   27420 2024-04-04 15:32:06.252505010 2024-04-04 15:32:06.252505010           0
      PI-0056   PI-0503  Ravi Steel Ltd  111027 2024-05-11 02:53:08.777555110 2024-05-11 02:53:08.777555110           0


---
## Section 5: Sequence Gap Testing

> **Audit Objective:** Verify completeness — are all invoice/voucher numbers accounted for? Missing numbers may indicate suppressed transactions (common in sales understatement).


```python
# ── 5.1 Create a Sales Register with deliberate gaps ─────────────────────────
# Simulate all invoice numbers from SI-0001 to SI-0200, with some intentionally missing
all_numbers   = list(range(1, 201))
missing_nums  = [15, 16, 42, 78, 79, 80, 143, 177]   # these are 'suppressed'
present_nums  = [n for n in all_numbers if n not in missing_nums]

sales_reg_nums = [f'SI-{str(n).zfill(4)}' for n in present_nums]
sales_register = pd.DataFrame({
    'Invoice_No'  : sales_reg_nums,
    'Seq_Num'     : present_nums,
    'Amount'      : np.random.randint(10000, 5_00_000, len(present_nums))
})

# ── 5.2 Detect Gaps ───────────────────────────────────────────────────────────
seq_nums     = sales_register['Seq_Num'].sort_values().reset_index(drop=True)
expected_seq = np.arange(seq_nums.min(), seq_nums.max() + 1)
gaps         = np.setdiff1d(expected_seq, seq_nums.values)

print(f'SEQUENCE GAP TEST — Sales Register')
print(f'Expected invoices : {len(expected_seq):4d} (SI-{expected_seq[0]:04d} to SI-{expected_seq[-1]:04d})')
print(f'Actual invoices   : {len(seq_nums):4d}')
print(f'Missing invoices  : {len(gaps):4d}')
print(f'\nMissing numbers   : {[f"SI-{n:04d}" for n in gaps]}')

# Group consecutive gaps into ranges
gap_groups = []
if len(gaps) > 0:
    start = gaps[0]
    for i in range(1, len(gaps)):
        if gaps[i] != gaps[i-1] + 1:
            gap_groups.append((start, gaps[i-1]))
            start = gaps[i]
    gap_groups.append((start, gaps[-1]))

print('\nGap ranges:')
for g_start, g_end in gap_groups:
    count = g_end - g_start + 1
    print(f'  SI-{g_start:04d} to SI-{g_end:04d} — {count} invoice(s) missing  ⚠ Investigate')
```

    SEQUENCE GAP TEST — Sales Register
    Expected invoices :  200 (SI-0001 to SI-0200)
    Actual invoices   :  192
    Missing invoices  :    8
    
    Missing numbers   : ['SI-0015', 'SI-0016', 'SI-0042', 'SI-0078', 'SI-0079', 'SI-0080', 'SI-0143', 'SI-0177']
    
    Gap ranges:
      SI-0015 to SI-0016 — 2 invoice(s) missing  ⚠ Investigate
      SI-0042 to SI-0042 — 1 invoice(s) missing  ⚠ Investigate
      SI-0078 to SI-0080 — 3 invoice(s) missing  ⚠ Investigate
      SI-0143 to SI-0143 — 1 invoice(s) missing  ⚠ Investigate
      SI-0177 to SI-0177 — 1 invoice(s) missing  ⚠ Investigate


---
## Section 6: Statistical Outlier Detection

Three methods for identifying unusual transactions:
1. **Z-Score** — how many standard deviations from the mean
2. **IQR Method** — interquartile range fencing
3. **Percentile Threshold** — top N% of transactions


```python
# ── 6.1 Z-Score Method ────────────────────────────────────────────────────────
pr = purchase_register.copy()
pr['Z_Score'] = (pr['Amount'] - pr['Amount'].mean()) / pr['Amount'].std()

z_outliers = pr[pr['Z_Score'].abs() > 2.5].sort_values('Z_Score', ascending=False)
print(f'Z-SCORE OUTLIERS (|Z| > 2.5): {len(z_outliers)} records')
print(z_outliers[['Invoice_No','Vendor','Amount','Z_Score','Category']].head(10).to_string(index=False))
```

    Z-SCORE OUTLIERS (|Z| > 2.5): 15 records
    Invoice_No             Vendor  Amount  Z_Score         Category
       PI-0210 Krishna Components 2000000    13.96      Spare Parts
       PI-0180     Ravi Steel Ltd  949986     6.32      Spare Parts
       PI-0491      Laxmi Traders  758759     4.93      Spare Parts
       PI-0114    Durga Chemicals  697941     4.49        Utilities
       PI-0221 Krishna Components  583961     3.66     Raw Material
       PI-0126     Ravi Steel Ltd  503101     3.07      Consumables
       PI-0379     Om Electricals  502707     3.07        Utilities
       PI-0469     Ravi Steel Ltd  499999     3.05 Packing Material
       PI-0375     Om Electricals  481094     2.91      Consumables
       PI-0235       Shiva Metals  475790     2.87      Consumables



```python
# ── 6.2 IQR Method ────────────────────────────────────────────────────────────
Q1    = pr['Amount'].quantile(0.25)
Q3    = pr['Amount'].quantile(0.75)
IQR   = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

iqr_outliers = pr[(pr['Amount'] < lower) | (pr['Amount'] > upper)]
print(f'IQR OUTLIERS: {len(iqr_outliers)} records')
print(f'  Normal range: ₹{max(0,lower):,.0f} – ₹{upper:,.0f}')
print(f'  High outliers: {(pr["Amount"] > upper).sum()}')
print(f'  Low outliers : {(pr["Amount"] < lower).sum()}')

# ── 6.3 Vendor-wise Outliers ─────────────────────────────────────────────────
print('\nVENDOR-WISE OUTLIER ANALYSIS')
print(f'{"Vendor":<25} {"Avg Amount":>12} {"Std Dev":>10} {"Max Amount":>12} {"Outliers":>9}')
print('-' * 75)
for vendor, group in pr.groupby('Vendor'):
    avg   = group['Amount'].mean()
    std   = group['Amount'].std()
    mx    = group['Amount'].max()
    z_fl  = ((group['Amount'] - avg) / std).abs() > 2
    out_c = z_fl.sum()
    print(f'{vendor:<25} ₹{avg:>10,.0f}  ₹{std:>8,.0f}  ₹{mx:>10,.0f}  {out_c:>9}')
```

    IQR OUTLIERS: 46 records
      Normal range: ₹0 – ₹202,883
      High outliers: 46
      Low outliers : 0
    
    VENDOR-WISE OUTLIER ANALYSIS
    Vendor                      Avg Amount    Std Dev   Max Amount  Outliers
    ---------------------------------------------------------------------------
    Durga Chemicals           ₹    95,126  ₹ 132,259  ₹   697,941          2
    Ganesh Supplies           ₹    77,026  ₹  82,404  ₹   447,246          2
    Krishna Components        ₹   108,043  ₹ 293,468  ₹ 2,000,000          1
    Laxmi Traders             ₹    70,718  ₹ 105,470  ₹   758,759          3
    Om Electricals            ₹    74,022  ₹ 107,591  ₹   502,707          5
    Ravi Steel Ltd            ₹    83,760  ₹ 128,183  ₹   949,986          4
    Saraswati Hardware        ₹    58,611  ₹  76,848  ₹   463,511          2
    Shiva Metals              ₹    87,193  ₹ 110,644  ₹   475,790          6


---
## Section 7: Consolidated Audit Risk Flag Report


```python
# ── Comprehensive Risk Flagging ───────────────────────────────────────────────
pr_flags = purchase_register.copy()
pr_flags['Invoice_Date'] = pd.to_datetime(pr_flags['Invoice_Date'])

# Flag 1: Weekend transactions
pr_flags['Flag_Weekend']    = pr_flags['Invoice_Date'].dt.dayofweek >= 5

# Flag 2: Round number amounts
pr_flags['Flag_Round_Num']  = pr_flags['Amount'] % 5000 == 0

# Flag 3: Just below approval threshold (99,000–99,999 if limit is 1,00,000)
pr_flags['Flag_Just_Below'] = pr_flags['Amount'].between(95_000, 99_999)

# Flag 4: Z-Score outlier
pr_flags['Z_Score']         = (pr_flags['Amount'] - pr_flags['Amount'].mean()) / pr_flags['Amount'].std()
pr_flags['Flag_Outlier']    = pr_flags['Z_Score'].abs() > 2.5

# Flag 5: Duplicate (same vendor + amount)
dup_mask = pr_flags.duplicated(subset=['Vendor', 'Amount'], keep=False)
pr_flags['Flag_Duplicate']  = dup_mask

# Risk Score (sum of flags)
flag_cols = ['Flag_Weekend', 'Flag_Round_Num', 'Flag_Just_Below', 'Flag_Outlier', 'Flag_Duplicate']
pr_flags['Risk_Score'] = pr_flags[flag_cols].sum(axis=1)

high_risk = pr_flags[pr_flags['Risk_Score'] >= 2].sort_values('Risk_Score', ascending=False)

print(f'AUDIT RISK FLAG REPORT')
print(f'Total invoices analysed : {len(pr_flags)}')
print(f'High risk (score >= 2)  : {len(high_risk)}')
print(f'Recommend for vouching  : {len(high_risk)} invoices')
print('\nFLAG SUMMARY:')
for col in flag_cols:
    count = pr_flags[col].sum()
    pct   = count / len(pr_flags) * 100
    print(f'  {col.replace("Flag_",""):<15}: {count:>4} invoices ({pct:.1f}%)')
print('\nTOP 10 HIGH-RISK INVOICES:')
print(high_risk[['Invoice_No','Vendor','Amount','Invoice_Date','Risk_Score'] + flag_cols].head(10).to_string(index=False))
```

    AUDIT RISK FLAG REPORT
    Total invoices analysed : 503
    High risk (score >= 2)  : 10
    Recommend for vouching  : 10 invoices
    
    FLAG SUMMARY:
      Weekend        :  147 invoices (29.2%)
      Round_Num      :    5 invoices (1.0%)
      Just_Below     :   11 invoices (2.2%)
      Outlier        :   15 invoices (3.0%)
      Duplicate      :    6 invoices (1.2%)
    
    TOP 10 HIGH-RISK INVOICES:
    Invoice_No             Vendor  Amount                  Invoice_Date  Risk_Score  Flag_Weekend  Flag_Round_Num  Flag_Just_Below  Flag_Outlier  Flag_Duplicate
       PI-0210 Krishna Components 2000000 2024-08-31 10:57:57.354709420           3          True            True            False          True           False
       PI-0056     Ravi Steel Ltd  111027 2024-05-11 02:53:08.777555110           2          True           False            False         False            True
       PI-0076    Ganesh Supplies   97370 2024-05-25 17:01:33.787575151           2          True           False             True         False           False
       PI-0114    Durga Chemicals  697941 2024-06-22 10:17:33.306613227           2          True           False            False          True           False
       PI-0221 Krishna Components  583961 2024-09-08 11:32:35.110220442           2          True           False            False          True           False
       PI-0375     Om Electricals  481094 2024-12-29 19:37:23.687374752           2          True           False            False          True           False
       PI-0421     Ravi Steel Ltd  430583 2025-02-01 08:56:45.210420844           2          True           False            False          True           False
       PI-0461 Krishna Components   50000 2025-03-02 13:13:35.230460924           2          True            True            False         False           False
       PI-0469     Ravi Steel Ltd  499999 2025-03-08 09:16:57.234468940           2          True           False            False          True           False
       PI-0503     Ravi Steel Ltd  111027 2024-05-11 02:53:08.777555110           2          True           False            False         False            True


---
## Practice Exercises

1. Draw a **systematic sample** (every kth item) of 30 invoices from the purchase register. Compare the sample's mean amount to the population mean.

2. Run Benford's test on **only the high-value invoices** (amount > ₹1 lakh). Does the digit distribution change?

3. Find all invoices where the **payment date is before the invoice date** — a clear accounting error.

4. Identify **split transactions**: same vendor, same week, amounts that sum to just below ₹1 lakh.

5. Build a **Vendor Risk Score** based on: frequency of round numbers, weekend entries, and Z-score outliers.


```python
# ── Exercise Solutions ────────────────────────────────────────────────────────

# Exercise 3: Payment before invoice date
pr_date = purchase_register.copy()
pr_date['Invoice_Date']  = pd.to_datetime(pr_date['Invoice_Date'])
pr_date['Payment_Date']  = pd.to_datetime(pr_date['Payment_Date'])
pre_dated = pr_date[pr_date['Payment_Date'] < pr_date['Invoice_Date']]
print(f'Ex 3 — Payment before invoice date: {len(pre_dated)} records')
if not pre_dated.empty:
    print(pre_dated[['Invoice_No','Vendor','Amount','Invoice_Date','Payment_Date']].head().to_string(index=False))

# Exercise 1: Systematic Sampling
k = len(purchase_register) // 30   # sampling interval
start = np.random.randint(0, k)
systematic = purchase_register.iloc[start::k].head(30)
print(f'\nEx 1 — Systematic Sample (every {k}th):')
print(f'  Sample mean  : ₹{systematic["Amount"].mean():,.0f}')
print(f'  Population mean: ₹{purchase_register["Amount"].mean():,.0f}')
```

    Ex 3 — Payment before invoice date: 0 records
    
    Ex 1 — Systematic Sample (every 16th):
      Sample mean  : ₹140,927
      Population mean: ₹80,747

