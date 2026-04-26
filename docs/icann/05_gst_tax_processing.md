# Module 5: GST & Tax Data Processing
### Data Science for Chartered Accountants

---

## Learning Objectives
- Process GSTR-1 (outward supplies) and GSTR-2A (auto-populated inward) data
- Reconcile purchase register with GSTR-2A to identify ITC mismatches
- Compute GST liability: CGST, SGST, IGST
- Perform HSN-wise and GSTIN-wise summaries
- Detect common GST compliance issues

---

> **CA Context:** GST reconciliation is one of the most time-consuming tasks in practice. A CA firm reconciles GSTR-2A with the purchase register for every client every month. This module automates that process entirely.


```python
import pandas as pd
import numpy as np

np.random.seed(7)
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', 15)
print('GST Analysis Module — Ready')
```

---
## Section 1: Sales Register & GSTR-1 Preparation

**GSTR-1** is filed by the **supplier** and contains details of all outward supplies (sales invoices). This is what your client's **customer sees in their GSTR-2A**.


```python
# ── HSN Master ────────────────────────────────────────────────────────────────
hsn_master = pd.DataFrame({
    'HSN_Code'   : ['7208', '7209', '8483', '3926', '4901', '8504', '3402', '2710'],
    'Description': ['Steel Plates/Sheets', 'Steel Coils', 'Mechanical Components',
                    'Plastic Articles', 'Printed Books/Manuals', 'Electrical Transformers',
                    'Industrial Detergents', 'Petroleum Products'],
    'GST_Rate'   : [18, 18, 18, 18, 0, 18, 18, 5]
})

# ── Customer Master ───────────────────────────────────────────────────────────
customers = pd.DataFrame({
    'Customer_Name': ['Aadhar Industries', 'Bharat Fabricators', 'Chandra Metals',
                      'Devraj Engineering', 'Ekta Plastics', 'Falguni Components'],
    'GSTIN'        : ['27AADHA1234A1Z5', '29BHFAB5678B1Z5', '33CHMET9012C1Z5',
                      '07DEVRA3456D1Z5', '24EKTAP7890E1Z5', '27FALGU1234F1Z5'],
    'State'        : ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Gujarat', 'Maharashtra'],
    'Supplier_State': 'Maharashtra'   # Our company is in Maharashtra
})

# Determine supply type
customers['Supply_Type'] = customers.apply(
    lambda r: 'Intra-State' if r['State'] == r['Supplier_State'] else 'Inter-State', axis=1
)

# ── Sales Register ────────────────────────────────────────────────────────────
n_sales = 120
sales_data = pd.DataFrame({
    'Invoice_No'    : [f'SI-{str(i).zfill(4)}' for i in range(1, n_sales + 1)],
    'Invoice_Date'  : pd.to_datetime(np.random.choice(
        pd.date_range('2024-04-01', '2024-04-30'), n_sales
    )),
    'Customer'      : np.random.choice(customers['Customer_Name'], n_sales),
    'HSN_Code'      : np.random.choice(hsn_master['HSN_Code'], n_sales,
                                        p=[0.25, 0.20, 0.15, 0.10, 0.05, 0.10, 0.10, 0.05]),
    'Taxable_Value' : np.random.randint(10_000, 5_00_000, n_sales)
})

# Merge GST rate and customer details
sales_data = sales_data.merge(hsn_master[['HSN_Code','GST_Rate']], on='HSN_Code')
sales_data = sales_data.merge(customers[['Customer_Name','GSTIN','Supply_Type']], 
                               left_on='Customer', right_on='Customer_Name', how='left')

# Compute GST components
sales_data['GST_Amount'] = (sales_data['Taxable_Value'] * sales_data['GST_Rate'] / 100).round(2)
sales_data['CGST']  = np.where(sales_data['Supply_Type'] == 'Intra-State', sales_data['GST_Amount'] / 2, 0)
sales_data['SGST']  = np.where(sales_data['Supply_Type'] == 'Intra-State', sales_data['GST_Amount'] / 2, 0)
sales_data['IGST']  = np.where(sales_data['Supply_Type'] == 'Inter-State', sales_data['GST_Amount'], 0)
sales_data['Invoice_Value'] = sales_data['Taxable_Value'] + sales_data['GST_Amount']

print(f'Sales Register: {len(sales_data)} invoices')
print(f'Total Taxable Value  : ₹{sales_data["Taxable_Value"].sum():>14,.0f}')
print(f'Total CGST           : ₹{sales_data["CGST"].sum():>14,.0f}')
print(f'Total SGST           : ₹{sales_data["SGST"].sum():>14,.0f}')
print(f'Total IGST           : ₹{sales_data["IGST"].sum():>14,.0f}')
print(f'Total Invoice Value  : ₹{sales_data["Invoice_Value"].sum():>14,.0f}')
```

---
## Section 2: GSTR-1 — B2B Summary & HSN Summary


```python
# ── 2.1 B2B Invoice Summary (Table 4A of GSTR-1) ─────────────────────────────
gstr1_b2b = sales_data.groupby(['Customer','GSTIN','Supply_Type']).agg(
    No_of_Invoices   = ('Invoice_No', 'count'),
    Taxable_Value    = ('Taxable_Value', 'sum'),
    CGST             = ('CGST', 'sum'),
    SGST             = ('SGST', 'sum'),
    IGST             = ('IGST', 'sum'),
    Invoice_Value    = ('Invoice_Value', 'sum')
).reset_index()

print('GSTR-1: B2B Summary (Table 4)')
print(gstr1_b2b.to_string(index=False))
```


```python
# ── 2.2 HSN-wise Summary (Table 12 of GSTR-1) ────────────────────────────────
hsn_summary = sales_data.groupby(['HSN_Code', 'GST_Rate']).agg(
    Description      = ('HSN_Code', lambda x: hsn_master.loc[
                            hsn_master['HSN_Code'] == x.iloc[0], 'Description'].values[0]
                            if len(x) > 0 else ''),
    Qty_Invoices     = ('Invoice_No', 'count'),
    Taxable_Value    = ('Taxable_Value', 'sum'),
    CGST             = ('CGST', 'sum'),
    SGST             = ('SGST', 'sum'),
    IGST             = ('IGST', 'sum'),
).reset_index().sort_values('Taxable_Value', ascending=False)

print('GSTR-1: HSN-wise Summary (Table 12)')
print(hsn_summary[['HSN_Code','GST_Rate','Taxable_Value','CGST','SGST','IGST']].to_string(index=False))

# ── 2.3 Rate-wise Summary ────────────────────────────────────────────────────
rate_summary = sales_data.groupby('GST_Rate').agg(
    Invoices      = ('Invoice_No', 'count'),
    Taxable_Value = ('Taxable_Value', 'sum'),
    GST_Amount    = ('GST_Amount', 'sum')
).reset_index()
rate_summary['% of Total Taxable'] = rate_summary['Taxable_Value'] / rate_summary['Taxable_Value'].sum() * 100
print('\nRate-wise Tax Summary:')
print(rate_summary.round(1).to_string(index=False))
```

---
## Section 3: GSTR-2A vs Purchase Register Reconciliation

**GSTR-2A** is auto-populated from suppliers' GSTR-1 filings. The taxpayer needs to match this against their own **purchase register** to claim Input Tax Credit (ITC).

### Why Reconciliation Matters:
| Situation | Consequence |
|---|---|
| Invoice in books, NOT in 2A | ITC may be denied under Rule 36(4) |
| Invoice in 2A, NOT in books | Need to book the entry |
| Amount mismatch | ITC claim should be the lower of two |
| GSTIN mismatch | Fraudulent supplier — serious risk |


```python
# ── Purchase Register ─────────────────────────────────────────────────────────
purchase_reg = pd.DataFrame({
    'PR_Invoice_No' : ['INV-101','INV-102','INV-103','INV-104','INV-105',
                       'INV-106','INV-107','INV-108','INV-109','INV-110',
                       'INV-111','INV-112','INV-113'],
    'Supplier_GSTIN': ['27AADHA1234A1Z5','29BHFAB5678B1Z5','33CHMET9012C1Z5',
                       '07DEVRA3456D1Z5','24EKTAP7890E1Z5','27FALGU1234F1Z5',
                       '27AADHA1234A1Z5','29BHFAB5678B1Z5','33CHMET9012C1Z5',
                       '07DEVRA3456D1Z5','WRONGGSTIN12345','27FALGU1234F1Z5',
                       '27AADHA1234A1Z5'],
    'Taxable_Value' : [1_00_000, 2_50_000, 75_000, 3_20_000, 1_80_000,
                       95_000, 1_40_000, 2_10_000, 60_000, 4_50_000,
                       80_000, 1_25_000, 3_00_000],
    'ITC_Claimed'   : [18_000, 30_000, 13_500, 57_600, 32_400,
                       17_100, 25_200, 37_800, 10_800, 81_000,
                       14_400, 22_500, 54_000]
})

# ── GSTR-2A Data (from portal) ────────────────────────────────────────────────
gstr2a = pd.DataFrame({
    'GSTR1_Invoice_No': ['INV-101','INV-102','INV-103','INV-104','INV-105',
                         'INV-106','INV-107','INV-108','INV-109','INV-110',
                         'INV-114',  # In 2A but not in purchase register
                         'INV-112'],  # Amount different in 2A
    'Supplier_GSTIN'  : ['27AADHA1234A1Z5','29BHFAB5678B1Z5','33CHMET9012C1Z5',
                         '07DEVRA3456D1Z5','24EKTAP7890E1Z5','27FALGU1234F1Z5',
                         '27AADHA1234A1Z5','29BHFAB5678B1Z5','33CHMET9012C1Z5',
                         '07DEVRA3456D1Z5','27NEWSU9999G1Z5','27FALGU1234F1Z5'],
    'Taxable_Value_2A': [1_00_000, 2_50_000, 75_000, 3_20_000, 1_80_000,
                         95_000, 1_40_000, 2_10_000, 60_000, 4_50_000,
                         1_10_000, 1_15_000],   # INV-112 has different value
    'ITC_in_2A'       : [18_000, 30_000, 13_500, 57_600, 32_400,
                         17_100, 25_200, 37_800, 10_800, 81_000,
                         19_800, 20_700]
})

print(f'Purchase Register : {len(purchase_reg)} invoices  | ITC Claimed: ₹{purchase_reg["ITC_Claimed"].sum():,.0f}')
print(f'GSTR-2A           : {len(gstr2a)} invoices | ITC in 2A : ₹{gstr2a["ITC_in_2A"].sum():,.0f}')
```


```python
# ── Reconciliation ────────────────────────────────────────────────────────────
recon = purchase_reg.merge(
    gstr2a,
    left_on =['PR_Invoice_No', 'Supplier_GSTIN'],
    right_on=['GSTR1_Invoice_No', 'Supplier_GSTIN'],
    how='outer',
    indicator=True
)

# Categorize each invoice
def recon_status(row):
    if row['_merge'] == 'left_only':
        return 'In Books only — ITC at risk'
    elif row['_merge'] == 'right_only':
        return 'In 2A only — Not booked'
    elif abs(row['ITC_Claimed'] - row['ITC_in_2A']) > 100:
        return 'Amount Mismatch'
    else:
        return 'Matched'

recon['Status'] = recon.apply(recon_status, axis=1)

print('GSTR-2A RECONCILIATION REPORT')
print('=' * 80)
for status, group in recon.groupby('Status'):
    inv_col = group['PR_Invoice_No'].fillna(group['GSTR1_Invoice_No'])
    print(f'\n{status.upper()} — {len(group)} invoice(s)')
    for _, row in group.iterrows():
        inv = row['PR_Invoice_No'] if pd.notna(row['PR_Invoice_No']) else row['GSTR1_Invoice_No']
        gstin = row['Supplier_GSTIN']
        itc_books = row['ITC_Claimed'] if pd.notna(row['ITC_Claimed']) else 0
        itc_2a    = row['ITC_in_2A']   if pd.notna(row['ITC_in_2A'])   else 0
        print(f'  {inv}  GSTIN:{gstin}  Books:₹{itc_books:>8,.0f}  2A:₹{itc_2a:>8,.0f}')
```


```python
# ── ITC Impact Summary ────────────────────────────────────────────────────────
matched_itc       = recon[recon['Status']=='Matched']['ITC_Claimed'].sum()
at_risk_itc       = recon[recon['Status']=='In Books only — ITC at risk']['ITC_Claimed'].sum()
mismatch_itc_diff = (recon[recon['Status']=='Amount Mismatch']['ITC_Claimed'] -
                     recon[recon['Status']=='Amount Mismatch']['ITC_in_2A']).abs().sum()
total_itc_claimed = purchase_reg['ITC_Claimed'].sum()

print('ITC RECONCILIATION SUMMARY')
print(f'  Total ITC Claimed in Books  : ₹{total_itc_claimed:>10,.0f}')
print(f'  ITC Fully Matched (Safe)    : ₹{matched_itc:>10,.0f}')
print(f'  ITC at Risk (Not in 2A)     : ₹{at_risk_itc:>10,.0f}  ⚠ May be disallowed')
print(f'  ITC Mismatch Difference     : ₹{mismatch_itc_diff:>10,.0f}  ⚠ Excess claimed')
print(f'  Estimated ITC Exposure      : ₹{at_risk_itc + mismatch_itc_diff:>10,.0f}')

# Invalid GSTIN check
invalid_gstin = purchase_reg[purchase_reg['Supplier_GSTIN'].str.len() != 15]
print(f'\n  Invalid GSTIN records       : {len(invalid_gstin)}')
if not invalid_gstin.empty:
    print(f'  ⚠ ITC on invalid GSTIN     : ₹{invalid_gstin["ITC_Claimed"].sum():>10,.0f}  MUST reverse')
```

---
## Section 4: GST Liability Computation — Monthly Summary

**GST Payable = Output Tax – ITC Available**

> **CA Insight:** The set-off order matters:
> - IGST credit can offset IGST, then CGST, then SGST
> - CGST credit can only offset CGST and IGST
> - SGST credit can only offset SGST and IGST


```python
# ── Monthly GST Computation (Apr 2024) ───────────────────────────────────────
output_tax = pd.DataFrame({
    'Component': ['CGST', 'SGST', 'IGST'],
    'Output_Tax': [
        sales_data['CGST'].sum(),
        sales_data['SGST'].sum(),
        sales_data['IGST'].sum()
    ]
})

# ITC available (from purchase register, only matched invoices)
matched_purchases = recon[recon['Status'] == 'Matched']
itc_available = {
    'IGST': matched_itc * 0.40,   # Assume 40% IGST, 30% CGST, 30% SGST
    'CGST': matched_itc * 0.30,
    'SGST': matched_itc * 0.30
}

print('MONTHLY GST LIABILITY STATEMENT — April 2024')
print('=' * 55)
print(f'{"Component":<12} {"Output Tax":>14} {"ITC Available":>14} {"Net Payable":>12}')
print('-' * 55)

total_output = 0; total_itc = 0; total_payable = 0
for _, row in output_tax.iterrows():
    comp   = row['Component']
    output = row['Output_Tax']
    itc    = itc_available.get(comp, 0)
    net    = max(0, output - itc)
    print(f'{comp:<12} ₹{output:>12,.0f}  ₹{itc:>12,.0f}  ₹{net:>10,.0f}')
    total_output += output; total_itc += itc; total_payable += net

print('-' * 55)
print(f'{"TOTAL":<12} ₹{total_output:>12,.0f}  ₹{total_itc:>12,.0f}  ₹{total_payable:>10,.0f}')
print(f'\nGST Cash to Pay (PMT-06): ₹{total_payable:,.0f}')
```

---
## Section 5: Compliance Checks & Red Flags


```python
# ── 5.1 E-Invoice Threshold Check (turnover > ₹5 Cr) ──────────────────────────
annual_turnover = sales_data['Invoice_Value'].sum() * 12  # annualised
e_invoice_required = annual_turnover > 5_00_00_000  # ₹5 Crore threshold

print(f'Estimated Annual Turnover: ₹{annual_turnover:,.0f}')
print(f'E-Invoice Mandatory: {"YES — IRN generation required" if e_invoice_required else "No"}')

# ── 5.2 B2C Large Invoice Check (invoice > ₹2.5 Lakh to unregistered) ─────────
high_value_b2c = sales_data[
    (sales_data['Supply_Type'] == 'Intra-State') &
    (sales_data['Invoice_Value'] > 2_50_000)
]
print(f'\nB2C invoices > ₹2.5L (to be reported in GSTR-1 Table 5): {len(high_value_b2c)}')

# ── 5.3 Nil-Rated Supply Check ────────────────────────────────────────────────
nil_rated = sales_data[sales_data['GST_Rate'] == 0]
print(f'Nil-rated supplies (to be declared separately in GSTR-1 Table 8): ₹{nil_rated["Taxable_Value"].sum():,.0f}')

# ── 5.4 GSTIN Format Validation ──────────────────────────────────────────────
import re
def validate_gstin(gstin):
    if pd.isna(gstin): return False
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, str(gstin)))

purchase_reg['GSTIN_Valid'] = purchase_reg['Supplier_GSTIN'].apply(validate_gstin)
invalid_count = (~purchase_reg['GSTIN_Valid']).sum()
print(f'\nInvalid Supplier GSTINs in Purchase Register: {invalid_count}')
if invalid_count > 0:
    print('These entries:')
    print(purchase_reg[~purchase_reg['GSTIN_Valid']][['PR_Invoice_No','Supplier_GSTIN','ITC_Claimed']])
```


```python
# ── 5.5 Late Filing Penalty Computation ──────────────────────────────────────
filing_scenarios = pd.DataFrame({
    'Return'      : ['GSTR-1', 'GSTR-3B', 'GSTR-9'],
    'Due_Date'    : pd.to_datetime(['2024-05-11', '2024-05-20', '2024-12-31']),
    'Filed_Date'  : pd.to_datetime(['2024-05-11', '2024-05-28', '2025-01-15']),
    'Daily_Late_Fee': [50, 50, 200]   # per day
})

filing_scenarios['Days_Late'] = (
    filing_scenarios['Filed_Date'] - filing_scenarios['Due_Date']
).dt.days.clip(lower=0)

filing_scenarios['Late_Fee'] = filing_scenarios['Days_Late'] * filing_scenarios['Daily_Late_Fee']
# Max late fee for nil returns = ₹500; for others = ₹10,000
filing_scenarios['Late_Fee'] = filing_scenarios['Late_Fee'].clip(upper=10_000)
filing_scenarios['Interest_18%'] = 0  # would need tax amount for interest

print('LATE FILING IMPACT:')
print(filing_scenarios[['Return','Due_Date','Filed_Date','Days_Late','Late_Fee']].to_string(index=False))
print(f'\nTotal Late Fees: ₹{filing_scenarios["Late_Fee"].sum():,.0f}')
```

---
## Section 6: Multi-Month GST Dashboard


```python
# ── 6.1 Monthly GST Summary for FY 2024-25 ────────────────────────────────────
months_fy = ['Apr-24','May-24','Jun-24','Jul-24','Aug-24','Sep-24',
              'Oct-24','Nov-24','Dec-24','Jan-25','Feb-25','Mar-25']

gst_dashboard = pd.DataFrame({
    'Month'         : months_fy,
    'Outward_Supply': [28_50_000, 31_20_000, 29_80_000, 33_50_000, 36_20_000, 34_80_000,
                       38_50_000, 42_30_000, 45_10_000, 41_20_000, 44_80_000, 52_10_000],
    'Output_GST'    : [4_14_000, 4_57_600, 4_36_800, 4_93_200, 5_35_680, 5_12_640,
                       5_68_800, 6_26_280, 6_67_880, 5_97_960, 6_56_640, 7_60_000],
    'ITC_Utilised'  : [2_80_000, 3_10_000, 2_95_000, 3_25_000, 3_55_000, 3_42_000,
                       3_75_000, 4_12_000, 4_38_000, 3_95_000, 4_25_000, 4_98_000]
})

gst_dashboard['Cash_Payment']   = (gst_dashboard['Output_GST'] - gst_dashboard['ITC_Utilised']).clip(lower=0)
gst_dashboard['ITC_Balance']    = (gst_dashboard['ITC_Utilised'] - gst_dashboard['Output_GST']).clip(lower=0)
gst_dashboard['Effective_Rate'] = gst_dashboard['Output_GST'] / gst_dashboard['Outward_Supply'] * 100

print('FY 2024-25 GST MONTHLY DASHBOARD')
print(f'{"Month":<9} {"Outward":>12} {"Output GST":>11} {"ITC Used":>10} {"Cash Pay":>10} {"Eff Rate":>9}')
print('-' * 65)
for _, r in gst_dashboard.iterrows():
    print(f'{r["Month"]:<9} ₹{r["Outward_Supply"]:>10,.0f} ₹{r["Output_GST"]:>9,.0f} ₹{r["ITC_Utilised"]:>8,.0f} ₹{r["Cash_Payment"]:>8,.0f} {r["Effective_Rate"]:>8.1f}%')
print('-' * 65)
totals = gst_dashboard[['Outward_Supply','Output_GST','ITC_Utilised','Cash_Payment']].sum()
print(f'{"TOTAL":<9} ₹{totals["Outward_Supply"]:>10,.0f} ₹{totals["Output_GST"]:>9,.0f} ₹{totals["ITC_Utilised"]:>8,.0f} ₹{totals["Cash_Payment"]:>8,.0f}')
```

---
## Practice Exercises

1. From the sales register, find all invoices where GST was **NOT charged** (rate = 0%) but should have been (HSN code 7208 – Steel at 18%).

2. Identify **suppliers whose ITC claims exceed ₹5 Lakhs** but do not appear in GSTR-2A — calculate the financial exposure.

3. Compute the **cumulative ITC balance** month-wise for FY 2024-25 (opening + ITC earned - ITC used).

4. Calculate the **annualized penalty** if GSTR-3B was consistently filed 5 days late every month.

5. For the HSN summary, identify which HSN codes contribute more than 20% of total taxable value.


```python
# ── Exercise Solutions ────────────────────────────────────────────────────────

# Exercise 3: Cumulative ITC Balance
opening_itc = 1_50_000  # Opening ITC balance
monthly_itc_earned = gst_dashboard['ITC_Utilised'] * 1.1  # Assume earned = 110% of utilised
gst_dashboard['ITC_Earned']      = monthly_itc_earned
gst_dashboard['Closing_ITC_Bal'] = opening_itc + monthly_itc_earned.cumsum() - gst_dashboard['ITC_Utilised'].cumsum()

print('Ex 3 — Cumulative ITC Balance:')
print(gst_dashboard[['Month','ITC_Earned','ITC_Utilised','Closing_ITC_Bal']].to_string(index=False))

# Exercise 4: Late filing penalty
monthly_penalty = 5 * 50 * 12  # 5 days × ₹50/day × 12 months
print(f'\nEx 4 — Annual penalty for 5 days late filing: ₹{monthly_penalty:,.0f}')
```
