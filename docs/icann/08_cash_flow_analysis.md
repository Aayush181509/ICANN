# Module 8: Cash Flow Analysis
### Data Science for Chartered Accountants

---

## Learning Objectives
- Prepare a **Direct Method** cash flow statement from bank receipts and payments
- Prepare the **Indirect Method** cash flow statement (reconcile PAT → Operating Cash Flow)
- Compute **Free Cash Flow (FCF)** and interpret its significance
- Analyse **Cash Conversion Cycle (CCC)** and working capital efficiency
- Build a **13-week rolling cash forecast**
- Detect **cash burn patterns** and liquidity stress signals

---

> **CA Context:** The Cash Flow Statement (as per AS 3 / Ind AS 7) is mandatory for all listed and large companies. CAs preparing standalone and consolidated financial statements must master both methods. The **indirect method** is most common in practice but understanding the direct method helps in **cash flow audits** and **treasury management**.


```python
import pandas as pd
import numpy as np

np.random.seed(2025)
pd.set_option('display.float_format', '{:,.0f}'.format)

# Company: Horizon Exports Ltd — a mid-size export-oriented manufacturer
print('Cash Flow Analysis — Horizon Exports Ltd')
print('FY 2024-25 | Amounts in ₹ Lakhs unless specified')
```

    Cash Flow Analysis — Horizon Exports Ltd
    FY 2024-25 | Amounts in ₹ Lakhs unless specified


---
## Section 1: Indirect Method — Operating Cash Flow from P&L & Balance Sheet


```python
# ── P&L Summary (₹ in Lakhs) ──────────────────────────────────────────────────
pl = {
    'Revenue'               : 8_500,
    'COGS'                  : 5_100,
    'Gross_Profit'          : 3_400,
    'Operating_Exp'         : 1_800,
    'EBITDA'                : 1_600,
    'Depreciation'          :   280,
    'EBIT'                  : 1_320,
    'Interest_Exp'          :   220,
    'PBT'                   : 1_100,
    'Tax'                   :   275,
    'PAT'                   :   825
}

# ── Balance Sheet Changes (FY25 vs FY24) — Working Capital ────────────────────
# Positive = increase in asset / decrease in liability = cash outflow
wc_changes = pd.DataFrame([
    ('Trade Receivables',     +450,  'Increase = cash tied up — bad sign'),
    ('Inventories',           +180,  'Increase = slower inventory turn'),
    ('Other Current Assets',  + 60,  'Advances to suppliers increased'),
    ('Trade Payables',        -320,  'Decrease = paying suppliers faster'),
    ('Other Current Liab.',   + 90,  'Increase = accruals increased'),
    ('Provisions',            + 30,  'Increase in provisions'),
], columns=['Item', 'Change', 'Comment'])

# Cash flow impact: increase in asset = cash outflow (negative); increase in liability = inflow
asset_items = ['Trade Receivables','Inventories','Other Current Assets']
wc_changes['CF_Impact'] = wc_changes.apply(
    lambda r: -r['Change'] if r['Item'] in asset_items else r['Change'], axis=1
)

total_wc_impact = wc_changes['CF_Impact'].sum()

# ── Indirect Method Cash Flow Statement ───────────────────────────────────────
print('CASH FLOW STATEMENT — INDIRECT METHOD (₹ Lakhs)')
print('For the year ended 31st March 2025')
print('=' * 60)

print('\nA. OPERATING ACTIVITIES')
print(f'   Net Profit After Tax                          {pl["PAT"]:>8,.0f}')
print('   Adjustments for non-cash items:')
print(f'     Add: Depreciation & Amortisation            {pl["Depreciation"]:>8,.0f}')
print(f'     Add: Interest Expense (financing)           {pl["Interest_Exp"]:>8,.0f}')

non_cash_total = pl['Depreciation'] + pl['Interest_Exp']
profit_adj     = pl['PAT'] + non_cash_total
print(f'   Operating Profit before WC changes           {profit_adj:>8,.0f}')

print('\n   Changes in Working Capital:')
for _, r in wc_changes.iterrows():
    impact_str = f'{r["CF_Impact"]:>+8,.0f}'
    flag = '  ⚠' if abs(r['CF_Impact']) > 200 else ''
    print(f'     {r["Item"]:<35} {impact_str}{flag}')

print(f'   Net WC change                                {total_wc_impact:>+8,.0f}')
operating_cf = profit_adj + total_wc_impact - pl['Tax']
print(f'\n   Less: Income Tax Paid                         ({pl["Tax"]:>6,.0f})')
print(f'   ─────────────────────────────────────────────────────')
print(f'   NET CASH FROM OPERATIONS                     {operating_cf:>8,.0f}')

# ── Investing Activities ──────────────────────────────────────────────────────
investing_items = [
    ('Purchase of PPE',                 -650),
    ('Sale of fixed assets',            + 35),
    ('Purchase of investments',         -120),
    ('Interest received',               + 18),
    ('Dividend received',               +  8),
]
investing_cf = sum(v for _, v in investing_items)

print('\nB. INVESTING ACTIVITIES')
for item, val in investing_items:
    print(f'   {item:<42} {val:>+8,.0f}')
print(f'   ─────────────────────────────────────────────────────')
print(f'   NET CASH USED IN INVESTING                   {investing_cf:>8,.0f}')

# ── Financing Activities ──────────────────────────────────────────────────────
financing_items = [
    ('Proceeds from term loan',          +300),
    ('Repayment of term loan',           -200),
    ('Repayment of working capital loan',- 50),
    ('Dividend paid',                    -125),
    ('Interest paid',                    -220),
]
financing_cf = sum(v for _, v in financing_items)

print('\nC. FINANCING ACTIVITIES')
for item, val in financing_items:
    print(f'   {item:<42} {val:>+8,.0f}')
print(f'   ─────────────────────────────────────────────────────')
print(f'   NET CASH FROM / (USED IN) FINANCING          {financing_cf:>8,.0f}')

# ── Summary ──────────────────────────────────────────────────────────────────
net_cash_flow   = operating_cf + investing_cf + financing_cf
opening_cash    = 320
closing_cash    = opening_cash + net_cash_flow

print(f'\n   ═════════════════════════════════════════════════════')
print(f'   NET CHANGE IN CASH                           {net_cash_flow:>+8,.0f}')
print(f'   Opening Cash & Bank Balance                   {opening_cash:>8,.0f}')
print(f'   CLOSING CASH & BANK BALANCE                   {closing_cash:>8,.0f}')
```

    CASH FLOW STATEMENT — INDIRECT METHOD (₹ Lakhs)
    For the year ended 31st March 2025
    ============================================================
    
    A. OPERATING ACTIVITIES
       Net Profit After Tax                               825
       Adjustments for non-cash items:
         Add: Depreciation & Amortisation                 280
         Add: Interest Expense (financing)                220
       Operating Profit before WC changes              1,325
    
       Changes in Working Capital:
         Trade Receivables                       -450  ⚠
         Inventories                             -180
         Other Current Assets                     -60
         Trade Payables                          -320  ⚠
         Other Current Liab.                      +90
         Provisions                               +30
       Net WC change                                    -890
    
       Less: Income Tax Paid                         (   275)
       ─────────────────────────────────────────────────────
       NET CASH FROM OPERATIONS                          160
    
    B. INVESTING ACTIVITIES
       Purchase of PPE                                -650
       Sale of fixed assets                            +35
       Purchase of investments                        -120
       Interest received                               +18
       Dividend received                                +8
       ─────────────────────────────────────────────────────
       NET CASH USED IN INVESTING                       -709
    
    C. FINANCING ACTIVITIES
       Proceeds from term loan                        +300
       Repayment of term loan                         -200
       Repayment of working capital loan               -50
       Dividend paid                                  -125
       Interest paid                                  -220
       ─────────────────────────────────────────────────────
       NET CASH FROM / (USED IN) FINANCING              -295
    
       ═════════════════════════════════════════════════════
       NET CHANGE IN CASH                               -844
       Opening Cash & Bank Balance                        320
       CLOSING CASH & BANK BALANCE                       -524


---
## Section 2: Direct Method — Cash Flow from Bank Ledger


```python
# ── Simulate Monthly Bank Statement ──────────────────────────────────────────
months = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']

bank_cash = pd.DataFrame({
    'Month'              : months,
    # Receipts
    'Collections'        : [680,720,690,750,810,800,870,920,940,840,880,980],
    'Export_Proceeds'    : [120,130,115,140,160,155,175,185,195,165,175,200],
    'Other_Income'       : [ 15, 12, 18, 10, 14, 16, 12, 18, 10, 20, 15, 18],
    # Payments
    'Supplier_Payments'  : [410,430,415,460,490,480,520,555,565,500,525,590],
    'Salaries'           : [180,180,180,185,185,185,190,190,190,195,195,195],
    'Tax_Payments'       : [ 70,  0,  0, 80,  0,  0, 65,  0,  0, 60,  0,  0],  # quarterly
    'Loan_Repayments'    : [ 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25],
    'Capital_Exp'        : [  0, 80,120,  0, 90,  0,200, 80,  0,  0,  0, 80],
    'Other_Expenses'     : [ 55, 60, 58, 62, 65, 63, 70, 68, 72, 65, 68, 75],
})

bank_cash['Total_Receipts']  = bank_cash[['Collections','Export_Proceeds','Other_Income']].sum(axis=1)
bank_cash['Total_Payments']  = bank_cash[['Supplier_Payments','Salaries','Tax_Payments',
                                           'Loan_Repayments','Capital_Exp','Other_Expenses']].sum(axis=1)
bank_cash['Net_Cash_Flow']   = bank_cash['Total_Receipts'] - bank_cash['Total_Payments']
bank_cash['Cumulative_Cash'] = bank_cash['Net_Cash_Flow'].cumsum() + opening_cash

print('DIRECT METHOD — MONTHLY CASH FLOW (₹ Lakhs)')
print(f'{"Month":<6} {"Receipts":>10} {"Payments":>10} {"Net CF":>8} {"Cum Cash":>10} {"Signal"}')
print('-' * 60)
for _, r in bank_cash.iterrows():
    signal = '🔴 LOW' if r['Cumulative_Cash'] < 200 else ('🟡 WATCH' if r['Cumulative_Cash'] < 400 else '🟢')
    print(f'{r["Month"]:<6} ₹{r["Total_Receipts"]:>7,.0f}L ₹{r["Total_Payments"]:>7,.0f}L {r["Net_Cash_Flow"]:>+7,.0f}L ₹{r["Cumulative_Cash"]:>7,.0f}L  {signal}')

print(f'\nMonths with cash outflow: {(bank_cash["Net_Cash_Flow"] < 0).sum()}')
print(f'Minimum cash balance: ₹{bank_cash["Cumulative_Cash"].min():,.0f}L in {bank_cash.loc[bank_cash["Cumulative_Cash"].idxmin(),"Month"]}')
```

    DIRECT METHOD — MONTHLY CASH FLOW (₹ Lakhs)
    Month    Receipts   Payments   Net CF   Cum Cash Signal
    ------------------------------------------------------------
    Apr    ₹    815L ₹    740L     +75L ₹    395L  🟡 WATCH
    May    ₹    862L ₹    775L     +87L ₹    482L  🟢
    Jun    ₹    823L ₹    798L     +25L ₹    507L  🟢
    Jul    ₹    900L ₹    812L     +88L ₹    595L  🟢
    Aug    ₹    984L ₹    855L    +129L ₹    724L  🟢
    Sep    ₹    971L ₹    753L    +218L ₹    942L  🟢
    Oct    ₹  1,057L ₹  1,070L     -13L ₹    929L  🟢
    Nov    ₹  1,123L ₹    918L    +205L ₹  1,134L  🟢
    Dec    ₹  1,145L ₹    852L    +293L ₹  1,427L  🟢
    Jan    ₹  1,025L ₹    845L    +180L ₹  1,607L  🟢
    Feb    ₹  1,070L ₹    813L    +257L ₹  1,864L  🟢
    Mar    ₹  1,198L ₹    965L    +233L ₹  2,097L  🟢
    
    Months with cash outflow: 1
    Minimum cash balance: ₹395L in Apr


---
## Section 3: Free Cash Flow & Quality of Earnings


```python
# ── Free Cash Flow Analysis ───────────────────────────────────────────────────
capex_total   = bank_cash['Capital_Exp'].sum()
fcf           = operating_cf - capex_total
fcf_yield     = fcf / (pl['Revenue']) * 100
ocf_to_pat    = operating_cf / pl['PAT']

print('FREE CASH FLOW ANALYSIS')
print(f'Operating Cash Flow (OCF) : ₹{operating_cf:>8,.0f}L')
print(f'Less: Capital Expenditure : ₹{capex_total:>8,.0f}L')
print(f'FREE CASH FLOW            : ₹{fcf:>8,.0f}L')
print(f'FCF as % of Revenue       : {fcf_yield:>8.1f}%')
print(f'OCF / PAT ratio           : {ocf_to_pat:>8.2f}x  (>1.0 is healthy)')

print('\nINTERPRETATION:')
if ocf_to_pat >= 1.0:
    print(f'  ✅ OCF/PAT = {ocf_to_pat:.2f}x — Cash earnings are higher than accounting profits')
    print(f'     This indicates GOOD earnings quality')
else:
    print(f'  ⚠ OCF/PAT = {ocf_to_pat:.2f}x — Profits are not being converted to cash')
    print(f'     Investigate receivables and inventory build-up')

# ── Multi-year FCF trend ──────────────────────────────────────────────────────
fcf_trend = pd.DataFrame({
    'Year'   : ['FY22','FY23','FY24','FY25'],
    'PAT'    : [  620,   710,   780,   825],
    'OCF'    : [  480,   650,   720,  operating_cf],
    'CapEx'  : [  420,   380,   510,  capex_total],
})
fcf_trend['FCF']       = fcf_trend['OCF'] - fcf_trend['CapEx']
fcf_trend['OCF_PAT']   = fcf_trend['OCF'] / fcf_trend['PAT']
fcf_trend['FCF_Yield'] = fcf_trend['FCF'] / 8500 * 100  # denominator = FY25 revenue

print('\nMULTI-YEAR FCF TREND (₹ Lakhs)')
print(fcf_trend.to_string(index=False))
```

    FREE CASH FLOW ANALYSIS
    Operating Cash Flow (OCF) : ₹     160L
    Less: Capital Expenditure : ₹     650L
    FREE CASH FLOW            : ₹    -490L
    FCF as % of Revenue       :     -5.8%
    OCF / PAT ratio           :     0.19x  (>1.0 is healthy)
    
    INTERPRETATION:
      ⚠ OCF/PAT = 0.19x — Profits are not being converted to cash
         Investigate receivables and inventory build-up
    
    MULTI-YEAR FCF TREND (₹ Lakhs)
    Year  PAT  OCF  CapEx  FCF  OCF_PAT  FCF_Yield
    FY22  620  480    420   60        1          1
    FY23  710  650    380  270        1          3
    FY24  780  720    510  210        1          2
    FY25  825  160    650 -490        0         -6


---
## Section 4: Cash Conversion Cycle (CCC)


```python
# ── Cash Conversion Cycle ─────────────────────────────────────────────────────
# CCC = DIO + DSO - DPO
# DIO = Days Inventory Outstanding
# DSO = Days Sales Outstanding
# DPO = Days Payable Outstanding

bs_data = pd.DataFrame({
    'Year'             : ['FY22','FY23','FY24','FY25'],
    'Revenue'          : [6_200, 7_100, 7_800, 8_500],
    'COGS'             : [3_720, 4_260, 4_680, 5_100],
    'Trade_Receivables': [  820,   890,   940, 1_390],
    'Inventories'      : [  560,   620,   680,   860],
    'Trade_Payables'   : [  480,   510,   560,   240],
})

bs_data['DSO'] = bs_data['Trade_Receivables'] / bs_data['Revenue'] * 365
bs_data['DIO'] = bs_data['Inventories']       / bs_data['COGS']    * 365
bs_data['DPO'] = bs_data['Trade_Payables']    / bs_data['COGS']    * 365
bs_data['CCC'] = bs_data['DSO'] + bs_data['DIO'] - bs_data['DPO']

print('CASH CONVERSION CYCLE ANALYSIS (Days)')
print(f'{"Year":<7} {"DSO":>8} {"DIO":>8} {"DPO":>8} {"CCC":>8}  Trend')
print('-' * 50)
prev_ccc = None
for _, r in bs_data.iterrows():
    arrow = '' if prev_ccc is None else ('↑⚠' if r['CCC'] > prev_ccc + 5 else ('↓✓' if r['CCC'] < prev_ccc - 5 else '→'))
    print(f'{r["Year"]:<7} {r["DSO"]:>8.1f} {r["DIO"]:>8.1f} {r["DPO"]:>8.1f} {r["CCC"]:>8.1f}  {arrow}')
    prev_ccc = r['CCC']

print('\nINTERPRETATION:')
latest = bs_data.iloc[-1]
prev   = bs_data.iloc[-2]
print(f'  DSO worsened from {prev["DSO"]:.0f} to {latest["DSO"]:.0f} days — receivables growing faster than sales')
print(f'  DPO collapsed from {prev["DPO"]:.0f} to {latest["DPO"]:.0f} days — paying suppliers much faster (why?)')
print(f'  CCC deteriorated by {latest["CCC"]-prev["CCC"]:.0f} days — significant working capital pressure')
```

    CASH CONVERSION CYCLE ANALYSIS (Days)
    Year         DSO      DIO      DPO      CCC  Trend
    --------------------------------------------------
    FY22        48.3     54.9     47.1     56.1  
    FY23        45.8     53.1     43.7     55.2  →
    FY24        44.0     53.0     43.7     53.3  →
    FY25        59.7     61.5     17.2    104.1  ↑⚠
    
    INTERPRETATION:
      DSO worsened from 44 to 60 days — receivables growing faster than sales
      DPO collapsed from 44 to 17 days — paying suppliers much faster (why?)
      CCC deteriorated by 51 days — significant working capital pressure


---
## Section 5: 13-Week Rolling Cash Flow Forecast

> **CA Context:** Banks and lenders often require a **13-week cash forecast** during financial stress. Restructuring professionals (IBC proceedings) prepare this as a mandatory deliverable.


```python
# ── 13-Week Forecast ───────────────────────────────────────────────────────────
weeks = [f'W{i+1}' for i in range(13)]
current_cash = 380  # Opening cash

weekly_forecast = pd.DataFrame({
    'Week'          : weeks,
    'Collections'   : [180, 165, 200, 175, 190, 210, 160, 195, 205, 180, 215, 225, 190],
    'Other_Receipts': [  5,   0,   0,  10,   0,   0,  15,   0,   5,   0,   0,  10,   0],
    'Supplier_Pay'  : [120, 115, 135, 118, 128, 140, 110, 130, 138, 122, 142, 148, 128],
    'Wages'         : [ 45,   0,   0,  45,   0,   0,  45,   0,   0,  45,   0,   0,  45],
    'Loan_Instalment': [25,   0,   0,  25,   0,   0,  25,   0,   0,  25,   0,   0,  25],
    'Tax_Advance'   : [  0,   0,   0,   0,  75,   0,   0,   0,   0,   0,   0,  75,   0],
    'Other_Outflow' : [ 15,  12,  18,  15,  14,  16,  12,  18,  15,  16,  14,  18,  15],
})

weekly_forecast['Total_In']   = weekly_forecast['Collections'] + weekly_forecast['Other_Receipts']
weekly_forecast['Total_Out']  = (weekly_forecast['Supplier_Pay'] + weekly_forecast['Wages'] +
                                  weekly_forecast['Loan_Instalment'] + weekly_forecast['Tax_Advance'] +
                                  weekly_forecast['Other_Outflow'])
weekly_forecast['Net']        = weekly_forecast['Total_In'] - weekly_forecast['Total_Out']
weekly_forecast['Closing_Bal']= current_cash + weekly_forecast['Net'].cumsum()

MIN_CASH_BUFFER = 150  # Minimum required cash
weekly_forecast['Status'] = weekly_forecast['Closing_Bal'].apply(
    lambda b: 'CRITICAL ⛔' if b < MIN_CASH_BUFFER else ('WARNING ⚠' if b < MIN_CASH_BUFFER * 1.5 else 'OK ✓')
)

print('13-WEEK ROLLING CASH FORECAST (₹ Lakhs)')
print(f'Opening Balance: ₹{current_cash}L  |  Min. Buffer: ₹{MIN_CASH_BUFFER}L')
print(f'\n{"Week":<6} {"Inflows":>9} {"Outflows":>9} {"Net":>8} {"Closing":>9}  Status')
print('-' * 60)
for _, r in weekly_forecast.iterrows():
    print(f'{r["Week"]:<6} ₹{r["Total_In"]:>6,.0f}L  ₹{r["Total_Out"]:>6,.0f}L {r["Net"]:>+7,.0f}L ₹{r["Closing_Bal"]:>6,.0f}L  {r["Status"]}')

stressed = weekly_forecast[weekly_forecast['Status'] != 'OK ✓']
print(f'\nStress weeks (below buffer): {len(stressed)}')
if not stressed.empty:
    print(f'Minimum cash point: ₹{weekly_forecast["Closing_Bal"].min():.0f}L in {weekly_forecast.loc[weekly_forecast["Closing_Bal"].idxmin(),"Week"]}')
```

    13-WEEK ROLLING CASH FORECAST (₹ Lakhs)
    Opening Balance: ₹380L  |  Min. Buffer: ₹150L
    
    Week     Inflows  Outflows      Net   Closing  Status
    ------------------------------------------------------------
    W1     ₹   185L  ₹   205L     -20L ₹   360L  OK ✓
    W2     ₹   165L  ₹   127L     +38L ₹   398L  OK ✓
    W3     ₹   200L  ₹   153L     +47L ₹   445L  OK ✓
    W4     ₹   185L  ₹   203L     -18L ₹   427L  OK ✓
    W5     ₹   190L  ₹   217L     -27L ₹   400L  OK ✓
    W6     ₹   210L  ₹   156L     +54L ₹   454L  OK ✓
    W7     ₹   175L  ₹   192L     -17L ₹   437L  OK ✓
    W8     ₹   195L  ₹   148L     +47L ₹   484L  OK ✓
    W9     ₹   210L  ₹   153L     +57L ₹   541L  OK ✓
    W10    ₹   180L  ₹   208L     -28L ₹   513L  OK ✓
    W11    ₹   215L  ₹   156L     +59L ₹   572L  OK ✓
    W12    ₹   235L  ₹   241L      -6L ₹   566L  OK ✓
    W13    ₹   190L  ₹   213L     -23L ₹   543L  OK ✓
    
    Stress weeks (below buffer): 0


---
## Section 6: Liquidity Ratio Trend Analysis


```python
# ── Liquidity Trend ───────────────────────────────────────────────────────────
liquidity = pd.DataFrame({
    'Year'            : ['FY22','FY23','FY24','FY25'],
    'Current_Assets'  : [2_100, 2_350, 2_580, 3_150],
    'Current_Liab'    : [1_200, 1_280, 1_380, 1_850],
    'Inventories'     : [  560,   620,   680,   860],
    'Receivables'     : [  820,   890,   940, 1_390],
    'Cash'            : [  280,   310,   320,   closing_cash],
})

liquidity['Current_Ratio'] = liquidity['Current_Assets']  / liquidity['Current_Liab']
liquidity['Quick_Ratio']   = (liquidity['Current_Assets'] - liquidity['Inventories']) / liquidity['Current_Liab']
liquidity['Cash_Ratio']    = liquidity['Cash']             / liquidity['Current_Liab']
liquidity['Defensive_Int'] = (liquidity['Cash'] + liquidity['Receivables']) / (liquidity['Current_Liab'] / 365)

print('LIQUIDITY RATIO TREND ANALYSIS')
print(f'{"Year":<6} {"Current":>9} {"Quick":>8} {"Cash":>8} {"Def.Int":>9}  Assessment')
print('-' * 60)
for _, r in liquidity.iterrows():
    current_ok = '✓' if r['Current_Ratio'] >= 2   else '⚠'
    quick_ok   = '✓' if r['Quick_Ratio']   >= 1   else '⚠'
    print(f'{r["Year"]:<6} {r["Current_Ratio"]:>9.2f} {r["Quick_Ratio"]:>8.2f} {r["Cash_Ratio"]:>8.2f} {r["Defensive_Int"]:>8.0f}d  CR:{current_ok} QR:{quick_ok}')

print('\nBenchmarks: Current Ratio ≥ 2.0, Quick Ratio ≥ 1.0')
lat = liquidity.iloc[-1]
print(f'\nFY25 Analysis:')
print(f'  Current Ratio {lat["Current_Ratio"]:.2f}x — {"ADEQUATE" if lat["Current_Ratio"] >= 2 else "BELOW BENCHMARK"}')
print(f'  Quick Ratio   {lat["Quick_Ratio"]:.2f}x — {"ADEQUATE" if lat["Quick_Ratio"] >= 1 else "BELOW BENCHMARK — inventory reliance"}')
print(f'  Defensive Interval: {lat["Defensive_Int"]:.0f} days of operations can be funded from liquid assets')
```

    LIQUIDITY RATIO TREND ANALYSIS
    Year     Current    Quick     Cash   Def.Int  Assessment
    ------------------------------------------------------------
    FY22        1.75     1.28     0.23      335d  CR:⚠ QR:✓
    FY23        1.84     1.35     0.24      342d  CR:⚠ QR:✓
    FY24        1.87     1.38     0.23      333d  CR:⚠ QR:✓
    FY25        1.70     1.24    -0.28      171d  CR:⚠ QR:✓
    
    Benchmarks: Current Ratio ≥ 2.0, Quick Ratio ≥ 1.0
    
    FY25 Analysis:
      Current Ratio 1.70x — BELOW BENCHMARK
      Quick Ratio   1.24x — ADEQUATE
      Defensive Interval: 171 days of operations can be funded from liquid assets


---
## Practice Exercises

1. Compute the **OCF-to-Debt ratio** if total debt = ₹1,800 Lakhs. What does this indicate?

2. In the direct method statement, identify the **month(s) where capital expenditure caused a cash outflow spike**. How should a CFO plan for this?

3. If the company collects 10% of its receivables faster (reducing DSO by ~15 days), by how much would **operating cash flow improve**?

4. Build a **sensitivity table**: how does FCF change if revenue grows by 5%, 10%, or 15% while operating costs grow by 7%?

5. From the 13-week forecast, identify the **minimum credit facility (overdraft) required** to maintain the ₹150L minimum buffer throughout.


```python
# ── Exercise Solutions ─────────────────────────────────────────────────────────

# Exercise 1: OCF to Debt
total_debt      = 1800
ocf_to_debt     = operating_cf / total_debt
debt_payoff_yrs = 1 / ocf_to_debt if ocf_to_debt > 0 else float('inf')
print(f'Ex 1: OCF/Debt Ratio = {ocf_to_debt:.2f}x  (Debt payoff in {debt_payoff_yrs:.1f} years from OCF)')

# Exercise 3: Faster collection impact
revenue_daily    = pl['Revenue'] / 365
dso_improvement  = 15  # days
cash_released    = revenue_daily * dso_improvement
print(f'\nEx 3: Releasing {dso_improvement} days of DSO frees ₹{cash_released:.0f}L in cash')

# Exercise 4: FCF Sensitivity to Revenue Growth
base_rev  = pl['Revenue']; base_costs = pl['COGS'] + pl['Operating_Exp']
print('\nEx 4: FCF Sensitivity Table (₹ Lakhs)')
print(f'{"Revenue Growth":<18} {"Revenue":>10} {"Costs":>10} {"EBITDA":>10} {"FCF (est)":>10}')
for rev_growth in [0.05, 0.10, 0.15]:
    new_rev   = base_rev * (1 + rev_growth)
    new_costs = base_costs * 1.07
    new_ebitda= new_rev - new_costs
    est_ocf   = new_ebitda * (operating_cf / pl['EBITDA'])  # scale proportionally
    est_fcf   = est_ocf - capex_total
    print(f'+{rev_growth*100:.0f}%{"":<15} {new_rev:>10,.0f} {new_costs:>10,.0f} {new_ebitda:>10,.0f} {est_fcf:>10,.0f}')

# Exercise 5: Minimum OD required
min_cash_projected = weekly_forecast['Closing_Bal'].min()
od_required        = max(0, MIN_CASH_BUFFER - min_cash_projected)
print(f'\nEx 5: Minimum projected cash = ₹{min_cash_projected:.0f}L')
print(f'      OD facility needed to maintain ₹{MIN_CASH_BUFFER}L buffer = ₹{od_required:.0f}L')
```

    Ex 1: OCF/Debt Ratio = 0.09x  (Debt payoff in 11.2 years from OCF)
    
    Ex 3: Releasing 15 days of DSO frees ₹349L in cash
    
    Ex 4: FCF Sensitivity Table (₹ Lakhs)
    Revenue Growth        Revenue      Costs     EBITDA  FCF (est)
    +5%                     8,925      7,383      1,542       -496
    +10%                     9,350      7,383      1,967       -453
    +15%                     9,775      7,383      2,392       -411
    
    Ex 5: Minimum projected cash = ₹360L
          OD facility needed to maintain ₹150L buffer = ₹0L

