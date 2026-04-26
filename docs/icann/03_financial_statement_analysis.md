# Module 3: Financial Statement Analysis
### Data Science for Chartered Accountants

---

## Learning Objectives
- Build and analyse an Income Statement (P&L)
- Construct a Balance Sheet and verify accounting equation
- Compute key financial ratios (liquidity, profitability, solvency, efficiency)
- Perform Common-Size analysis
- Conduct multi-year trend analysis

---

> **CA Context:** This module mirrors what you do during **audit planning, statutory audit, and management reporting** — but automates the computation so you can analyse 5 years of financials in seconds and instantly spot red flags.


```python
import pandas as pd
import numpy as np

pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.max_columns', 20)

# ── Helper: Format currency ───────────────────────────────────────────────────
def fmt(x): return f'₹{x:>14,.0f}' if pd.notna(x) else ''
def pct(x): return f'{x:>8.2f}%'  if pd.notna(x) else ''
```

---
## Section 1: Income Statement (Profit & Loss)

We analyse **Hypothetical Company: Sunrise Manufacturing Ltd.** — a mid-size company in the engineering sector. Data is for FY 2021-22 to FY 2024-25.


```python
# ── Income Statement Data (₹ in Lakhs) ───────────────────────────────────────
years = ['FY22', 'FY23', 'FY24', 'FY25']

income_stmt = pd.DataFrame({
    'FY22': [4500, 150, 4650, 2700, 520, 280, 210, 180, 3890, 760, 95, 665, 225, 440, 132, 308],
    'FY23': [5200, 175, 5375, 3050, 590, 310, 245, 205, 4400, 975, 110, 865, 310, 555, 166, 389],
    'FY24': [6100, 200, 6300, 3480, 670, 360, 290, 235, 5035, 1265, 135, 1130, 390, 740, 222, 518],
    'FY25': [7200, 220, 7420, 3960, 750, 420, 335, 270, 5735, 1685, 155, 1530, 480, 1050, 315, 735]
}, index=[
    'Revenue from Operations',
    'Other Income',
    'Total Income',
    'Cost of Materials Consumed',
    'Employee Benefit Expenses',
    'Finance Costs',
    'Depreciation & Amortisation',
    'Other Expenses',
    'Total Expenses',
    'EBITDA',
    'Interest',
    'EBIT',
    'Tax Expense',
    'Profit Before Tax (PBT)',
    'Tax',
    'Profit After Tax (PAT)'
])

print('INCOME STATEMENT — Sunrise Manufacturing Ltd.')
print('(₹ in Lakhs)\n')
print(f'{"Line Item":<35} {"FY22":>8} {"FY23":>8} {"FY24":>8} {"FY25":>8}')
print('-' * 70)
for item, row in income_stmt.iterrows():
    print(f'{item:<35} {row["FY22"]:>8,.0f} {row["FY23"]:>8,.0f} {row["FY24"]:>8,.0f} {row["FY25"]:>8,.0f}')
```

    INCOME STATEMENT — Sunrise Manufacturing Ltd.
    (₹ in Lakhs)
    
    Line Item                               FY22     FY23     FY24     FY25
    ----------------------------------------------------------------------
    Revenue from Operations                4,500    5,200    6,100    7,200
    Other Income                             150      175      200      220
    Total Income                           4,650    5,375    6,300    7,420
    Cost of Materials Consumed             2,700    3,050    3,480    3,960
    Employee Benefit Expenses                520      590      670      750
    Finance Costs                            280      310      360      420
    Depreciation & Amortisation              210      245      290      335
    Other Expenses                           180      205      235      270
    Total Expenses                         3,890    4,400    5,035    5,735
    EBITDA                                   760      975    1,265    1,685
    Interest                                  95      110      135      155
    EBIT                                     665      865    1,130    1,530
    Tax Expense                              225      310      390      480
    Profit Before Tax (PBT)                  440      555      740    1,050
    Tax                                      132      166      222      315
    Profit After Tax (PAT)                   308      389      518      735



```python
# ── 1.1 P&L Margin Analysis ───────────────────────────────────────────────────
revenue = income_stmt.loc['Revenue from Operations']

margins = pd.DataFrame({
    yr: {
        'Gross Profit Margin %'  : (revenue[yr] - income_stmt.loc['Cost of Materials Consumed', yr]) / revenue[yr] * 100,
        'EBITDA Margin %'        : income_stmt.loc['EBITDA', yr] / revenue[yr] * 100,
        'EBIT Margin %'          : income_stmt.loc['EBIT', yr] / revenue[yr] * 100,
        'PBT Margin %'           : income_stmt.loc['Profit Before Tax (PBT)', yr] / revenue[yr] * 100,
        'Net Profit Margin (PAT)%': income_stmt.loc['Profit After Tax (PAT)', yr] / revenue[yr] * 100
    }
    for yr in years
}).T

print('PROFITABILITY MARGINS (%)')
print(margins.round(2))

# Trend Check
pat_margin_trend = margins['Net Profit Margin (PAT)%']
if pat_margin_trend.iloc[-1] > pat_margin_trend.iloc[0]:
    print(f'\n✓ PAT Margin improving: {pat_margin_trend.iloc[0]:.1f}% → {pat_margin_trend.iloc[-1]:.1f}%')
else:
    print(f'\n⚠ PAT Margin declining: {pat_margin_trend.iloc[0]:.1f}% → {pat_margin_trend.iloc[-1]:.1f}%')
```

    PROFITABILITY MARGINS (%)
          Gross Profit Margin %  EBITDA Margin %  EBIT Margin %  PBT Margin %  \
    FY22                  40.00            16.89          14.78          9.78   
    FY23                  41.35            18.75          16.63         10.67   
    FY24                  42.95            20.74          18.52         12.13   
    FY25                  45.00            23.40          21.25         14.58   
    
          Net Profit Margin (PAT)%  
    FY22                      6.84  
    FY23                      7.48  
    FY24                      8.49  
    FY25                     10.21  
    
    ✓ PAT Margin improving: 6.8% → 10.2%



```python
# ── 1.2 Year-on-Year Growth Rates ────────────────────────────────────────────
growth_items = ['Revenue from Operations', 'EBITDA', 'Profit Before Tax (PBT)', 'Profit After Tax (PAT)']
growth_df = income_stmt.loc[growth_items]

# pct_change computes YoY growth automatically
yoy_growth = growth_df.T.pct_change() * 100

print('YEAR-ON-YEAR GROWTH RATES (%)')
print(yoy_growth.round(1).T)

# CAGR computation
def cagr(series):
    return ((series.iloc[-1] / series.iloc[0]) ** (1 / (len(series)-1)) - 1) * 100

print('\nCAGR (FY22–FY25):')
for item in growth_items:
    c = cagr(income_stmt.loc[item])
    print(f'  {item:<35}: {c:.1f}%')
```

    YEAR-ON-YEAR GROWTH RATES (%)
                             FY22  FY23  FY24  FY25
    Revenue from Operations   NaN 15.60 17.30 18.00
    EBITDA                    NaN 28.30 29.70 33.20
    Profit Before Tax (PBT)   NaN 26.10 33.30 41.90
    Profit After Tax (PAT)    NaN 26.30 33.20 41.90
    
    CAGR (FY22–FY25):
      Revenue from Operations            : 17.0%
      EBITDA                             : 30.4%
      Profit Before Tax (PBT)            : 33.6%
      Profit After Tax (PAT)             : 33.6%


---
## Section 2: Balance Sheet Analysis


```python
# ── Balance Sheet Data (₹ in Lakhs) ──────────────────────────────────────────
balance_sheet = pd.DataFrame({
    'FY22': [1000, 800, 1200, 3000,  # Equity + Reserves, LT Debt, Other LT, Total Equity & Liab
              1800, 600, 3000,       # Fixed Assets (Net), CWIP, Total Non-Current
              450, 380, 170, 3000,   # Inventory, Debtors, Cash & Bank, Total Assets (check)
              350, 280, 420,         # Creditors, ST Borrowings, Other CL
              350, 280, 170],        # Inventory, Debtors, Cash
    'FY23': [1200, 950, 1300, 3450,
              2050, 650, 3450,
              520, 440, 200, 3450,
              410, 320, 480,
              520, 440, 200],
    'FY24': [1500, 1100, 1400, 4000,
              2300, 700, 4000,
              610, 520, 250, 4000,
              480, 370, 550,
              610, 520, 250],
    'FY25': [1900, 1250, 1450, 4600,
              2600, 750, 4600,
              720, 620, 310, 4600,
              550, 420, 630,
              720, 620, 310]
}, index=[
    'Share Capital & Reserves',
    'Long-Term Borrowings',
    'Other Non-Current Liabilities',
    'Total Equity & Liabilities',
    'Net Fixed Assets (PPE)',
    'Capital Work in Progress',
    'Total Non-Current Assets',
    'Inventories',
    'Trade Receivables',
    'Cash & Cash Equivalents',
    'Total Assets',
    'Trade Payables',
    'Short-Term Borrowings',
    'Other Current Liabilities',
    'Inventory (Working Capital)',
    'Debtors (Working Capital)',
    'Cash (Working Capital)'
])

# Verify Accounting Equation: Assets = Equity + Liabilities
print('Balance Sheet check (Assets = Equity + Liabilities):')
for yr in years:
    total_eq_liab = balance_sheet.loc['Total Equity & Liabilities', yr]
    total_assets  = balance_sheet.loc['Total Assets', yr]
    status = 'BALANCED' if total_eq_liab == total_assets else 'ERROR'
    print(f'  {yr}: ₹{total_assets:,.0f}L vs ₹{total_eq_liab:,.0f}L — {status}')
```

    Balance Sheet check (Assets = Equity + Liabilities):
      FY22: ₹3,000L vs ₹3,000L — BALANCED
      FY23: ₹3,450L vs ₹3,450L — BALANCED
      FY24: ₹4,000L vs ₹4,000L — BALANCED
      FY25: ₹4,600L vs ₹4,600L — BALANCED


---
## Section 3: Financial Ratio Analysis

Ratios are the **language of financial analysis**. They tell the story that raw numbers can't.

| Category | Ratios |
|---|---|
| **Liquidity** | Current Ratio, Quick Ratio, Cash Ratio |
| **Profitability** | ROE, ROA, ROCE |
| **Solvency / Leverage** | D/E Ratio, Interest Coverage, Debt-Asset Ratio |
| **Efficiency** | Debtor Days, Creditor Days, Inventory Turnover |


```python
# ── 3.1 Compute All Ratios for All Years ──────────────────────────────────────
ratios = {}
for yr in years:
    # Shorthand
    inv  = balance_sheet.loc['Inventories', yr]
    rec  = balance_sheet.loc['Trade Receivables', yr]
    cash = balance_sheet.loc['Cash & Cash Equivalents', yr]
    ca   = inv + rec + cash                                # Current Assets
    cp   = (balance_sheet.loc['Trade Payables', yr] +
            balance_sheet.loc['Short-Term Borrowings', yr] +
            balance_sheet.loc['Other Current Liabilities', yr])  # Current Liabilities
    nfa  = balance_sheet.loc['Net Fixed Assets (PPE)', yr]
    ta   = balance_sheet.loc['Total Assets', yr]
    ltd  = balance_sheet.loc['Long-Term Borrowings', yr]
    stb  = balance_sheet.loc['Short-Term Borrowings', yr]
    td   = ltd + stb                                       # Total Debt
    eq   = balance_sheet.loc['Share Capital & Reserves', yr]
    rev  = income_stmt.loc['Revenue from Operations', yr]
    pat  = income_stmt.loc['Profit After Tax (PAT)', yr]
    pbt  = income_stmt.loc['Profit Before Tax (PBT)', yr]
    int_ = income_stmt.loc['Finance Costs', yr]
    ebit = income_stmt.loc['EBIT', yr]
    ebitda = income_stmt.loc['EBITDA', yr]
    cogs = income_stmt.loc['Cost of Materials Consumed', yr]

    ratios[yr] = {
        # Liquidity
        'Current Ratio'          : round(ca / cp, 2),
        'Quick Ratio'            : round((ca - inv) / cp, 2),
        'Cash Ratio'             : round(cash / cp, 2),
        # Profitability
        'Return on Equity (ROE)%': round(pat / eq * 100, 2),
        'Return on Assets (ROA)%': round(pat / ta * 100, 2),
        'ROCE %'                 : round(ebit / (ta - cp) * 100, 2),
        # Solvency
        'Debt-to-Equity Ratio'   : round(td / eq, 2),
        'Interest Coverage'      : round(ebit / int_, 2),
        'Debt-to-Assets'         : round(td / ta, 2),
        # Efficiency (in Days)
        'Debtor Days'            : round(rec / rev * 365, 1),
        'Creditor Days'          : round(balance_sheet.loc['Trade Payables', yr] / cogs * 365, 1),
        'Inventory Days'         : round(inv / cogs * 365, 1),
    }

ratios_df = pd.DataFrame(ratios)
print('COMPREHENSIVE RATIO ANALYSIS')
print(ratios_df)
```

    COMPREHENSIVE RATIO ANALYSIS
                             FY22  FY23  FY24  FY25
    Current Ratio            0.95  0.96  0.99  1.03
    Quick Ratio              0.52  0.53  0.55  0.58
    Cash Ratio               0.16  0.17  0.18  0.19
    Return on Equity (ROE)% 30.80 32.42 34.53 38.68
    Return on Assets (ROA)% 10.27 11.28 12.95 15.98
    ROCE %                  34.10 38.62 43.46 51.00
    Debt-to-Equity Ratio     1.08  1.06  0.98  0.88
    Interest Coverage        2.38  2.79  3.14  3.64
    Debt-to-Assets           0.36  0.37  0.37  0.36
    Debtor Days             30.80 30.90 31.10 31.40
    Creditor Days           47.30 49.10 50.30 50.70
    Inventory Days          60.80 62.20 64.00 66.40



```python
# ── 3.2 Ratio Interpretation ─────────────────────────────────────────────────
def interpret_ratio(name, value, yr):
    if name == 'Current Ratio':
        if value >= 2:     return f'{yr} {name}: {value} — STRONG (>2 is ideal)'
        elif value >= 1.5: return f'{yr} {name}: {value} — ADEQUATE'
        else:              return f'{yr} {name}: {value} — ⚠ WEAK (<1.5 needs attention)'
    elif name == 'Interest Coverage':
        if value >= 3:     return f'{yr} {name}: {value} — SAFE (>3x coverage)'
        elif value >= 1.5: return f'{yr} {name}: {value} — MODERATE'
        else:              return f'{yr} {name}: {value} — ⚠ RISK (barely covering interest)'
    elif name == 'Debt-to-Equity Ratio':
        if value <= 1:     return f'{yr} {name}: {value} — CONSERVATIVE'
        elif value <= 2:   return f'{yr} {name}: {value} — MODERATE'
        else:              return f'{yr} {name}: {value} — ⚠ HIGH LEVERAGE'
    return ''

print('KEY RATIO INTERPRETATION:')
for metric in ['Current Ratio', 'Interest Coverage', 'Debt-to-Equity Ratio']:
    for yr in years:
        msg = interpret_ratio(metric, ratios_df.loc[metric, yr], yr)
        if msg: print(f'  {msg}')
    print()
```

    KEY RATIO INTERPRETATION:
      FY22 Current Ratio: 0.95 — ⚠ WEAK (<1.5 needs attention)
      FY23 Current Ratio: 0.96 — ⚠ WEAK (<1.5 needs attention)
      FY24 Current Ratio: 0.99 — ⚠ WEAK (<1.5 needs attention)
      FY25 Current Ratio: 1.03 — ⚠ WEAK (<1.5 needs attention)
    
      FY22 Interest Coverage: 2.38 — MODERATE
      FY23 Interest Coverage: 2.79 — MODERATE
      FY24 Interest Coverage: 3.14 — SAFE (>3x coverage)
      FY25 Interest Coverage: 3.64 — SAFE (>3x coverage)
    
      FY22 Debt-to-Equity Ratio: 1.08 — MODERATE
      FY23 Debt-to-Equity Ratio: 1.06 — MODERATE
      FY24 Debt-to-Equity Ratio: 0.98 — CONSERVATIVE
      FY25 Debt-to-Equity Ratio: 0.88 — CONSERVATIVE
    


---
## Section 4: Common-Size Analysis

**Common-size** expresses every line item as a **percentage of a base figure** (Revenue for P&L, Total Assets for Balance Sheet). This enables cross-year and cross-company comparison regardless of scale.

> **Audit Use:** Common-size analysis is used during **analytical procedures** (SA 520) to identify unusual movements.


```python
# ── 4.1 Common-Size P&L (% of Revenue) ───────────────────────────────────────
cs_items = [
    'Cost of Materials Consumed', 'Employee Benefit Expenses',
    'Finance Costs', 'Depreciation & Amortisation',
    'Other Expenses', 'Total Expenses',
    'EBITDA', 'Profit Before Tax (PBT)', 'Profit After Tax (PAT)'
]

revenue_row = income_stmt.loc['Revenue from Operations']
cs_pnl = income_stmt.loc[cs_items].div(revenue_row) * 100

print('COMMON-SIZE P&L (% of Revenue from Operations)')
print(f'{"Line Item":<35} {"FY22":>7} {"FY23":>7} {"FY24":>7} {"FY25":>7}')
print('-' * 62)
for item, row in cs_pnl.iterrows():
    print(f'{item:<35} {row["FY22"]:>6.1f}% {row["FY23"]:>6.1f}% {row["FY24"]:>6.1f}% {row["FY25"]:>6.1f}%')
```

    COMMON-SIZE P&L (% of Revenue from Operations)
    Line Item                              FY22    FY23    FY24    FY25
    --------------------------------------------------------------
    Cost of Materials Consumed            60.0%   58.7%   57.0%   55.0%
    Employee Benefit Expenses             11.6%   11.3%   11.0%   10.4%
    Finance Costs                          6.2%    6.0%    5.9%    5.8%
    Depreciation & Amortisation            4.7%    4.7%    4.8%    4.7%
    Other Expenses                         4.0%    3.9%    3.9%    3.8%
    Total Expenses                        86.4%   84.6%   82.5%   79.7%
    EBITDA                                16.9%   18.8%   20.7%   23.4%
    Profit Before Tax (PBT)                9.8%   10.7%   12.1%   14.6%
    Profit After Tax (PAT)                 6.8%    7.5%    8.5%   10.2%



```python
# ── 4.2 Flag Unusual Movements (like SA 520 Analytical Procedures) ────────────
cs_changes = cs_pnl.T.diff().T  # change in % from year to year
threshold  = 1.5  # flag if % shifts by more than 1.5 percentage points

print('ANALYTICAL REVIEW — Unusual Movements (shift > 1.5 pp):')
found = False
for item in cs_changes.index:
    for yr_idx in range(1, len(years)):
        change = cs_changes.loc[item, years[yr_idx]]
        if pd.notna(change) and abs(change) > threshold:
            direction = 'INCREASED' if change > 0 else 'DECREASED'
            print(f'  ⚠ {item:<35}: {direction} by {abs(change):.1f}pp in {years[yr_idx]}')
            found = True

if not found:
    print('  No significant unusual movements found.')
```

    ANALYTICAL REVIEW — Unusual Movements (shift > 1.5 pp):
      ⚠ Cost of Materials Consumed         : DECREASED by 1.6pp in FY24
      ⚠ Cost of Materials Consumed         : DECREASED by 2.0pp in FY25
      ⚠ Total Expenses                     : DECREASED by 1.8pp in FY23
      ⚠ Total Expenses                     : DECREASED by 2.1pp in FY24
      ⚠ Total Expenses                     : DECREASED by 2.9pp in FY25
      ⚠ EBITDA                             : INCREASED by 1.9pp in FY23
      ⚠ EBITDA                             : INCREASED by 2.0pp in FY24
      ⚠ EBITDA                             : INCREASED by 2.7pp in FY25
      ⚠ Profit Before Tax (PBT)            : INCREASED by 2.5pp in FY25
      ⚠ Profit After Tax (PAT)             : INCREASED by 1.7pp in FY25


---
## Section 5: DuPont Analysis — Decomposing ROE

The **DuPont framework** breaks ROE into three drivers:

$$ROE = \underbrace{\frac{PAT}{Revenue}}_{\text{Profit Margin}} \times \underbrace{\frac{Revenue}{Assets}}_{\text{Asset Turnover}} \times \underbrace{\frac{Assets}{Equity}}_{\text{Financial Leverage}}$$

> **CA Insight:** This tells you **why** ROE changed — was it better margins, higher asset utilisation, or just more debt?


```python
# ── DuPont Decomposition ──────────────────────────────────────────────────────
dupont = {}
for yr in years:
    pat    = income_stmt.loc['Profit After Tax (PAT)', yr]
    rev    = income_stmt.loc['Revenue from Operations', yr]
    ta     = balance_sheet.loc['Total Assets', yr]
    eq     = balance_sheet.loc['Share Capital & Reserves', yr]

    net_margin    = pat / rev
    asset_turnover= rev / ta
    leverage      = ta  / eq
    roe_dupont    = net_margin * asset_turnover * leverage

    dupont[yr] = {
        'Net Profit Margin'   : round(net_margin * 100, 2),
        'Asset Turnover'      : round(asset_turnover, 2),
        'Equity Multiplier'   : round(leverage, 2),
        'ROE (DuPont) %'      : round(roe_dupont * 100, 2)
    }

dupont_df = pd.DataFrame(dupont)
print('DUPONT ANALYSIS')
print(dupont_df)
```

    DUPONT ANALYSIS
                       FY22  FY23  FY24  FY25
    Net Profit Margin  6.84  7.48  8.49 10.21
    Asset Turnover     1.50  1.51  1.52  1.57
    Equity Multiplier  3.00  2.88  2.67  2.42
    ROE (DuPont) %    30.80 32.42 34.53 38.68


---
## Section 6: Working Capital Analysis


```python
# ── Working Capital & Cash Conversion Cycle ───────────────────────────────────
wc_analysis = {}
for yr in years:
    inv      = balance_sheet.loc['Inventories', yr]
    rec      = balance_sheet.loc['Trade Receivables', yr]
    cash_    = balance_sheet.loc['Cash & Cash Equivalents', yr]
    payables = balance_sheet.loc['Trade Payables', yr]
    stb      = balance_sheet.loc['Short-Term Borrowings', yr]
    ocl      = balance_sheet.loc['Other Current Liabilities', yr]
    ca       = inv + rec + cash_
    cl       = payables + stb + ocl
    nwc      = ca - cl
    rev      = income_stmt.loc['Revenue from Operations', yr]
    cogs     = income_stmt.loc['Cost of Materials Consumed', yr]

    inv_days  = inv / cogs * 365
    rec_days  = rec / rev * 365
    pay_days  = payables / cogs * 365
    ccc       = inv_days + rec_days - pay_days  # Cash Conversion Cycle

    wc_analysis[yr] = {
        'Current Assets (₹L)' : round(ca, 0),
        'Current Liab (₹L)'   : round(cl, 0),
        'Net Working Capital' : round(nwc, 0),
        'Inventory Days'      : round(inv_days, 1),
        'Debtor Days'         : round(rec_days, 1),
        'Creditor Days'       : round(pay_days, 1),
        'Cash Conv. Cycle'    : round(ccc, 1)
    }

wc_df = pd.DataFrame(wc_analysis)
print('WORKING CAPITAL & CASH CONVERSION CYCLE')
print(wc_df)
print('\n(Lower CCC = better cash management)')
```

    WORKING CAPITAL & CASH CONVERSION CYCLE
                            FY22     FY23     FY24     FY25
    Current Assets (₹L) 1,000.00 1,160.00 1,380.00 1,650.00
    Current Liab (₹L)   1,050.00 1,210.00 1,400.00 1,600.00
    Net Working Capital   -50.00   -50.00   -20.00    50.00
    Inventory Days         60.80    62.20    64.00    66.40
    Debtor Days            30.80    30.90    31.10    31.40
    Creditor Days          47.30    49.10    50.30    50.70
    Cash Conv. Cycle       44.30    44.00    44.70    47.10
    
    (Lower CCC = better cash management)


---
## Section 7: Automated Financial Health Scorecard

Based on the ratios, we build a scorecard that generates a **financial health flag** — useful for audit risk assessment.


```python
# ── Scorecard for FY25 ────────────────────────────────────────────────────────
def financial_scorecard(yr, ratios_df, income_stmt, balance_sheet):
    score = 0
    flags = []

    checks = [
        ('Current Ratio',        ratios_df.loc['Current Ratio', yr],        lambda v: v >= 1.5,   'Liquidity adequate',       'LOW LIQUIDITY — risk of default'),
        ('Interest Coverage',    ratios_df.loc['Interest Coverage', yr],    lambda v: v >= 2.5,   'Debt service comfortable',  'LOW INTEREST COVERAGE — solvency risk'),
        ('Debt-to-Equity Ratio', ratios_df.loc['Debt-to-Equity Ratio', yr], lambda v: v <= 2.0,   'Leverage acceptable',       'HIGH LEVERAGE — financing risk'),
        ('ROE %',                ratios_df.loc['Return on Equity (ROE)%', yr], lambda v: v >= 12, 'Good returns to equity',    'POOR ROE — below 12% hurdle'),
        ('Debtor Days',          ratios_df.loc['Debtor Days', yr],           lambda v: v <= 60,   'Efficient collections',     'HIGH DEBTOR DAYS — collection risk'),
    ]

    for name, value, good, ok_msg, warn_msg in checks:
        if good(value):
            score += 1
            flags.append(f'  ✓ {name} ({value:.2f}): {ok_msg}')
        else:
            flags.append(f'  ⚠ {name} ({value:.2f}): {warn_msg}')

    print(f'FINANCIAL HEALTH SCORECARD — {yr}')
    print('-' * 55)
    for f in flags: print(f)
    rating = 'STRONG' if score >= 4 else 'MODERATE' if score >= 3 else 'WEAK'
    print(f'\nOverall Score: {score}/5 — {rating}')

financial_scorecard('FY25', ratios_df, income_stmt, balance_sheet)
```

    FINANCIAL HEALTH SCORECARD — FY25
    -------------------------------------------------------
      ⚠ Current Ratio (1.03): LOW LIQUIDITY — risk of default
      ✓ Interest Coverage (3.64): Debt service comfortable
      ✓ Debt-to-Equity Ratio (0.88): Leverage acceptable
      ✓ ROE % (38.68): Good returns to equity
      ✓ Debtor Days (31.40): Efficient collections
    
    Overall Score: 4/5 — STRONG


---
## Practice Exercises

1. Using the data provided, compute the **Altman Z-Score** for FY25. Interpret whether the company is in the distress zone, grey zone, or safe zone.

2. Compute the **Operating Leverage** (EBIT change % / Revenue change %) for FY22→FY25. What does this tell about the cost structure?

3. A competitor company has the same revenue as Sunrise FY25 (₹7200L) but a PAT of ₹950L. Compare their profitability ratios.

4. Calculate the **Net Cash from Operations** estimate using: PAT + Depreciation - Change in Working Capital (between FY24 and FY25).

5. Extend the common-size P&L to also show the **year-on-year absolute change** for each line item.


```python
# ── Exercise 1: Altman Z-Score ────────────────────────────────────────────────
# Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
yr = 'FY25'
ta   = balance_sheet.loc['Total Assets', yr]
ca   = (balance_sheet.loc['Inventories', yr] +
        balance_sheet.loc['Trade Receivables', yr] +
        balance_sheet.loc['Cash & Cash Equivalents', yr])
cl   = (balance_sheet.loc['Trade Payables', yr] +
        balance_sheet.loc['Short-Term Borrowings', yr] +
        balance_sheet.loc['Other Current Liabilities', yr])
re   = balance_sheet.loc['Share Capital & Reserves', yr] * 0.4  # approximate retained earnings
ebit_ = income_stmt.loc['EBIT', yr]
rev_  = income_stmt.loc['Revenue from Operations', yr]
eq_  = balance_sheet.loc['Share Capital & Reserves', yr]
td_  = (balance_sheet.loc['Long-Term Borrowings', yr] +
        balance_sheet.loc['Short-Term Borrowings', yr])

X1 = (ca - cl) / ta
X2 = re / ta
X3 = ebit_ / ta
X4 = eq_ / td_
X5 = rev_ / ta

Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 1.0*X5
print(f'Altman Z-Score ({yr}): {Z:.2f}')
if Z > 2.99:   print('  Zone: SAFE (low bankruptcy risk)')
elif Z > 1.81: print('  Zone: GREY (moderate concern)')
else:          print('  Zone: ⚠ DISTRESS (high bankruptcy risk)')
```

    Altman Z-Score (FY25): 3.59
      Zone: SAFE (low bankruptcy risk)



```python

```
