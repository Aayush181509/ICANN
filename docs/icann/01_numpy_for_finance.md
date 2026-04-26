# Module 1: NumPy for Financial Calculations
### Data Science for Chartered Accountants

---

## Learning Objectives
By the end of this module, you will be able to:
- Create and operate on NumPy arrays using financial data
- Perform bulk EMI, depreciation, and tax computations without loops
- Analyze portfolio returns and compute risk metrics
- Apply time-value-of-money (NPV) concepts programmatically

---

> **CA Context:** Excel handles a few hundred rows comfortably. When your client's data has 1,00,000 loan accounts, invoices, or asset records, NumPy computes across all of them in milliseconds — with a single line of code.


```python
import numpy as np

print('NumPy version:', np.__version__)
np.set_printoptions(precision=2, suppress=True)  # clean decimal display
```

    NumPy version: 2.2.6


---
## Section 1: Financial Arrays — The Building Block

A NumPy **array** is like a column in a spreadsheet — but far faster and more powerful.

| Concept | Excel | NumPy |
|---|---|---|
| Column of values | Column A | 1-D array |
| Table | Sheet | 2-D array |
| Formula on all rows | Fill Down | Vectorized operation |


```python
# ── 1.1 Revenue & Expense Arrays for 12 months ──────────────────────────────
monthly_revenue = np.array([
    4_20_000, 3_85_000, 4_50_000, 5_10_000, 4_75_000, 5_25_000,
    4_90_000, 5_60_000, 6_10_000, 5_80_000, 6_30_000, 7_20_000
], dtype=float)

monthly_expenses = np.array([
    3_10_000, 2_95_000, 3_20_000, 3_60_000, 3_40_000, 3_80_000,
    3_55_000, 4_00_000, 4_30_000, 4_10_000, 4_50_000, 5_20_000
], dtype=float)

months = np.array(['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                   'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'])

# ── 1.2 Profit Computation — No loops needed ─────────────────────────────────
monthly_profit = monthly_revenue - monthly_expenses
profit_margin  = (monthly_profit / monthly_revenue) * 100

print('Monthly Profit (₹):'); print(monthly_profit)
print('\nProfit Margin (%):'); print(np.round(profit_margin, 2))
```

    Monthly Profit (₹):
    [110000.  90000. 130000. 150000. 135000. 145000. 135000. 160000. 180000.
     170000. 180000. 200000.]
    
    Profit Margin (%):
    [26.19 23.38 28.89 29.41 28.42 27.62 27.55 28.57 29.51 29.31 28.57 27.78]



```python
# ── 1.3 Summary Statistics (like Excel's AVERAGE, MAX, MIN) ──────────────────
print(f'Annual Revenue   : ₹{monthly_revenue.sum():>12,.0f}')
print(f'Annual Expense   : ₹{monthly_expenses.sum():>12,.0f}')
print(f'Annual Profit    : ₹{monthly_profit.sum():>12,.0f}')
print(f'Avg Monthly Rev  : ₹{monthly_revenue.mean():>12,.0f}')
print(f'Best Month       : {months[monthly_profit.argmax()]} (₹{monthly_profit.max():,.0f})')
print(f'Worst Month      : {months[monthly_profit.argmin()]} (₹{monthly_profit.min():,.0f})')
print(f'Revenue Std Dev  : ₹{monthly_revenue.std():>12,.0f}  (volatility measure)')
```

    Annual Revenue   : ₹   6,355,000
    Annual Expense   : ₹   4,570,000
    Annual Profit    : ₹   1,785,000
    Avg Monthly Rev  : ₹     529,583
    Best Month       : Mar (₹200,000)
    Worst Month      : May (₹90,000)
    Revenue Std Dev  : ₹      91,503  (volatility measure)


---
## Section 2: EMI Calculation

**Formula:**
$$EMI = P \times \frac{r(1+r)^n}{(1+r)^n - 1}$$

Where: `P` = Principal, `r` = monthly interest rate, `n` = number of months

**CA Use-Case:** A bank audit client has 50,000 loan accounts. Compute EMI for all of them simultaneously.


```python
# ── 2.1 EMI for a Single Loan ────────────────────────────────────────────────
def emi(principal, annual_rate_pct, tenure_months):
    r = annual_rate_pct / (12 * 100)          # monthly rate
    return principal * r * (1 + r)**tenure_months / ((1 + r)**tenure_months - 1)

# Home loan example
P, rate, n = 50_00_000, 8.5, 240  # ₹50L at 8.5% for 20 years
monthly_emi = emi(P, rate, n)
total_payment = monthly_emi * n
total_interest = total_payment - P

print(f'Loan Amount   : ₹{P:>12,.0f}')
print(f'Monthly EMI   : ₹{monthly_emi:>12,.0f}')
print(f'Total Payment : ₹{total_payment:>12,.0f}')
print(f'Total Interest: ₹{total_interest:>12,.0f}  ({total_interest/P*100:.1f}% of principal)')
```

    Loan Amount   : ₹   5,000,000
    Monthly EMI   : ₹      43,391
    Total Payment : ₹  10,413,879
    Total Interest: ₹   5,413,879  (108.3% of principal)



```python
# ── 2.2 Loan Portfolio — 10 Clients at Once (vectorized) ────────────────────
principals  = np.array([10, 25, 50, 75, 100, 150, 200, 35, 80, 120]) * 1_00_000
rates       = np.array([7.5, 8.0, 8.5, 8.5, 9.0, 9.5, 10.0, 7.0, 8.75, 9.25])
tenures     = np.array([60, 120, 240, 180, 300, 240, 300, 84, 180, 240])  # months

emis        = emi(principals, rates, tenures)
total_pay   = emis * tenures
interest    = total_pay - principals

print(f'{"Client":<8} {"Principal":>12} {"Rate":>6} {"Tenure":>8} {"EMI":>12} {"Interest":>14}')
print('-' * 65)
for i in range(len(principals)):
    print(f'Client {i+1:<2} ₹{principals[i]:>10,.0f}  {rates[i]:>5.2f}%  {tenures[i]:>5}M  ₹{emis[i]:>10,.0f}  ₹{interest[i]:>12,.0f}')
print('-' * 65)
print(f'{"Portfolio":<8} ₹{principals.sum():>10,.0f}  {"":>6}  {"":>8}  ₹{emis.sum():>10,.0f}  ₹{interest.sum():>12,.0f}')
```

    Client      Principal   Rate   Tenure          EMI       Interest
    -----------------------------------------------------------------
    Client 1  ₹ 1,000,000   7.50%     60M  ₹    20,038  ₹     202,277
    Client 2  ₹ 2,500,000   8.00%    120M  ₹    30,332  ₹   1,139,828
    Client 3  ₹ 5,000,000   8.50%    240M  ₹    43,391  ₹   5,413,879
    Client 4  ₹ 7,500,000   8.50%    180M  ₹    73,855  ₹   5,793,984
    Client 5  ₹10,000,000   9.00%    300M  ₹    83,920  ₹  15,175,891
    Client 6  ₹15,000,000   9.50%    240M  ₹   139,820  ₹  18,556,723
    Client 7  ₹20,000,000  10.00%    300M  ₹   181,740  ₹  34,522,045
    Client 8  ₹ 3,500,000   7.00%     84M  ₹    52,824  ₹     937,248
    Client 9  ₹ 8,000,000   8.75%    180M  ₹    79,956  ₹   6,392,061
    Client 10 ₹12,000,000   9.25%    240M  ₹   109,904  ₹  14,376,965
    -----------------------------------------------------------------
    Portfolio ₹84,500,000                    ₹   815,780  ₹ 102,510,899



```python
# ── 2.3 Amortisation Schedule for one loan ───────────────────────────────────
P_single, r_annual, n_months = 20_00_000, 9.0, 60
r_monthly = r_annual / (12 * 100)
emi_val   = emi(P_single, r_annual, n_months)

balance       = P_single
interest_paid = []
principal_paid= []
balances      = []

for _ in range(n_months):
    int_part  = balance * r_monthly
    prin_part = emi_val - int_part
    balance  -= prin_part
    interest_paid.append(int_part)
    principal_paid.append(prin_part)
    balances.append(max(balance, 0))

interest_paid  = np.array(interest_paid)
principal_paid = np.array(principal_paid)
balances       = np.array(balances)

print('First 6 months of Amortisation Schedule:')
print(f'{"Month":<6} {"EMI":>10} {"Interest":>12} {"Principal":>12} {"Balance":>14}')
print('-' * 58)
for i in range(6):
    print(f'{i+1:<6} ₹{emi_val:>8,.0f}  ₹{interest_paid[i]:>10,.0f}  ₹{principal_paid[i]:>10,.0f}  ₹{balances[i]:>12,.0f}')
print(f'\nTotal Interest over {n_months}M: ₹{interest_paid.sum():,.0f}')
```

    First 6 months of Amortisation Schedule:
    Month         EMI     Interest    Principal        Balance
    ----------------------------------------------------------
    1      ₹  41,517  ₹    15,000  ₹    26,517  ₹   1,973,483
    2      ₹  41,517  ₹    14,801  ₹    26,716  ₹   1,946,768
    3      ₹  41,517  ₹    14,601  ₹    26,916  ₹   1,919,852
    4      ₹  41,517  ₹    14,399  ₹    27,118  ₹   1,892,734
    5      ₹  41,517  ₹    14,196  ₹    27,321  ₹   1,865,413
    6      ₹  41,517  ₹    13,991  ₹    27,526  ₹   1,837,887
    
    Total Interest over 60M: ₹491,003


---
## Section 3: Depreciation Calculations

| Method | Formula | When Used |
|---|---|---|
| **SLM** (Straight Line) | `(Cost - Salvage) / Useful Life` | Companies Act |
| **WDV** (Written Down Value) | `Book Value × Rate%` | Income Tax Act |

> **CA Insight:** Schedule II of Companies Act 2013 prescribes useful lives for SLM. For IT purposes, CBDT notifies WDV rates (e.g., 15% for plant & machinery).


```python
# ── 3.1 SLM Depreciation for an Asset Block ─────────────────────────────────
asset_names = np.array(['Machinery A', 'Machinery B', 'Vehicle', 'Computer', 'Furniture'])
cost        = np.array([5_00_000, 8_00_000, 12_00_000, 80_000, 1_50_000], dtype=float)
salvage     = np.array([50_000,   80_000,    1_00_000,  5_000,  10_000],  dtype=float)
useful_life = np.array([10, 10, 8, 3, 10], dtype=float)   # years

slm_dep    = (cost - salvage) / useful_life
dep_rate   = slm_dep / cost * 100

print('Fixed Asset Schedule — SLM Depreciation')
print(f'{"Asset":<14} {"Cost":>10} {"Salvage":>10} {"Life":>5} {"Annual Dep":>12} {"Dep Rate":>9}')
print('-' * 65)
for i in range(len(asset_names)):
    print(f'{asset_names[i]:<14} ₹{cost[i]:>8,.0f}  ₹{salvage[i]:>8,.0f}  {useful_life[i]:>4.0f}Y  ₹{slm_dep[i]:>10,.0f}  {dep_rate[i]:>8.2f}%')
print('-' * 65)
print(f'{"Total":<14} ₹{cost.sum():>8,.0f}  {"":>10}  {"":>5}  ₹{slm_dep.sum():>10,.0f}')
```

    Fixed Asset Schedule — SLM Depreciation
    Asset                Cost    Salvage  Life   Annual Dep  Dep Rate
    -----------------------------------------------------------------
    Machinery A    ₹ 500,000  ₹  50,000    10Y  ₹    45,000      9.00%
    Machinery B    ₹ 800,000  ₹  80,000    10Y  ₹    72,000      9.00%
    Vehicle        ₹1,200,000  ₹ 100,000     8Y  ₹   137,500     11.46%
    Computer       ₹  80,000  ₹   5,000     3Y  ₹    25,000     31.25%
    Furniture      ₹ 150,000  ₹  10,000    10Y  ₹    14,000      9.33%
    -----------------------------------------------------------------
    Total          ₹2,730,000                     ₹   293,500



```python
# ── 3.2 WDV Depreciation Schedule over 5 years ──────────────────────────────
opening_wdv = 10_00_000.0   # Plant & Machinery block
wdv_rate    = 0.15           # 15% as per IT Act
years       = np.arange(1, 6)

# Vectorized: WDV at end of year y = Cost × (1 - rate)^y
closing_wdv = opening_wdv * (1 - wdv_rate) ** years
opening_wdv_arr = np.concatenate([[opening_wdv], closing_wdv[:-1]])
depreciation = opening_wdv_arr * wdv_rate

print('WDV Depreciation Schedule (IT Act — 15% rate)')
print(f'{"Year":<6} {"Opening WDV":>14} {"Depreciation":>14} {"Closing WDV":>14}')
print('-' * 52)
for i in range(5):
    print(f'Year {i+1:<2} ₹{opening_wdv_arr[i]:>12,.0f}  ₹{depreciation[i]:>12,.0f}  ₹{closing_wdv[i]:>12,.0f}')
print(f'\nTotal WDV Depreciation claimed: ₹{depreciation.sum():,.0f}')
print(f'Block value remaining after 5Y: ₹{closing_wdv[-1]:,.0f}')
```

    WDV Depreciation Schedule (IT Act — 15% rate)
    Year      Opening WDV   Depreciation    Closing WDV
    ----------------------------------------------------
    Year 1  ₹   1,000,000  ₹     150,000  ₹     850,000
    Year 2  ₹     850,000  ₹     127,500  ₹     722,500
    Year 3  ₹     722,500  ₹     108,375  ₹     614,125
    Year 4  ₹     614,125  ₹      92,119  ₹     522,006
    Year 5  ₹     522,006  ₹      78,301  ₹     443,705
    
    Total WDV Depreciation claimed: ₹556,295
    Block value remaining after 5Y: ₹443,705


---
## Section 4: Income Tax Computation

**New Tax Regime (FY 2024-25) Slabs:**

| Income Slab | Rate |
|---|---|
| Up to ₹3,00,000 | Nil |
| ₹3,00,001 – ₹7,00,000 | 5% |
| ₹7,00,001 – ₹10,00,000 | 10% |
| ₹10,00,001 – ₹12,00,000 | 15% |
| ₹12,00,001 – ₹15,00,000 | 20% |
| Above ₹15,00,000 | 30% |


```python
def compute_tax_new_regime(income):
    """Vectorised income tax computation — New Regime FY 2024-25."""
    slabs      = np.array([0, 3_00_000, 7_00_000, 10_00_000, 12_00_000, 15_00_000])
    rates      = np.array([0.00, 0.05, 0.10, 0.15, 0.20, 0.30])
    slab_width = np.diff(slabs, append=np.inf)   # width of each slab

    income = np.atleast_1d(np.asarray(income, dtype=float))
    tax    = np.zeros_like(income)

    for i, (slab, width, rate) in enumerate(zip(slabs, slab_width, rates)):
        taxable_in_slab = np.clip(income - slab, 0, width)
        tax += taxable_in_slab * rate

    # Rebate u/s 87A (income <= 7L → tax = 0)
    tax = np.where(income <= 7_00_000, 0, tax)
    surcharge = np.where(income > 50_00_000, tax * 0.15,
                np.where(income > 20_00_000, tax * 0.10, 0))
    cess = (tax + surcharge) * 0.04
    return tax + surcharge + cess

# Compute for 8 employees
incomes = np.array([4_50_000, 6_80_000, 7_50_000, 11_00_000,
                    14_50_000, 20_00_000, 35_00_000, 60_00_000])
taxes   = compute_tax_new_regime(incomes)

print(f'{"Annual Income":>16} {"Tax Liability":>16} {"Effective Rate":>14}')
print('-' * 50)
for inc, tax in zip(incomes, taxes):
    eff = (tax / inc * 100) if inc > 0 else 0
    print(f'₹{inc:>14,.0f}  ₹{tax:>14,.0f}  {eff:>12.2f}%')
```

       Annual Income    Tax Liability Effective Rate
    --------------------------------------------------
    ₹       450,000  ₹             0          0.00%
    ₹       680,000  ₹             0          0.00%
    ₹       750,000  ₹        26,000          3.47%
    ₹     1,100,000  ₹        67,600          6.15%
    ₹     1,450,000  ₹       135,200          9.32%
    ₹     2,000,000  ₹       301,600         15.08%
    ₹     3,500,000  ₹       846,560         24.19%
    ₹     6,000,000  ₹     1,782,040         29.70%


---
## Section 5: Net Present Value (NPV) & Investment Appraisal

$$NPV = \sum_{t=0}^{n} \frac{CF_t}{(1+r)^t}$$

**CA Use-Case:** Evaluating a client's capital investment or project feasibility.


```python
# ── 5.1 NPV of a Capital Project ─────────────────────────────────────────────
# Project: Factory expansion — Year 0 outflow, Years 1-6 inflows
cash_flows    = np.array([-50_00_000, 12_00_000, 15_00_000, 18_00_000,
                           20_00_000, 20_00_000, 14_00_000])
discount_rate = 0.12   # 12% WACC / hurdle rate
years         = np.arange(len(cash_flows))

discount_factors = 1 / (1 + discount_rate) ** years
pv_cash_flows    = cash_flows * discount_factors
npv              = pv_cash_flows.sum()

print('Capital Budgeting — NPV Analysis')
print(f'{"Year":<6} {"Cash Flow":>14} {"Discount Factor":>16} {"Present Value":>16}')
print('-' * 58)
for y, cf, df, pv in zip(years, cash_flows, discount_factors, pv_cash_flows):
    print(f'Year {y:<2} ₹{cf:>12,.0f}   {df:>14.4f}   ₹{pv:>14,.0f}')
print('-' * 58)
print(f'NPV @ {discount_rate*100:.0f}% : ₹{npv:>14,.0f}')
print(f'\nDecision: {"ACCEPT — Project creates value" if npv > 0 else "REJECT — Project destroys value"}')
```

    Capital Budgeting — NPV Analysis
    Year        Cash Flow  Discount Factor    Present Value
    ----------------------------------------------------------
    Year 0  ₹  -5,000,000           1.0000   ₹    -5,000,000
    Year 1  ₹   1,200,000           0.8929   ₹     1,071,429
    Year 2  ₹   1,500,000           0.7972   ₹     1,195,791
    Year 3  ₹   1,800,000           0.7118   ₹     1,281,204
    Year 4  ₹   2,000,000           0.6355   ₹     1,271,036
    Year 5  ₹   2,000,000           0.5674   ₹     1,134,854
    Year 6  ₹   1,400,000           0.5066   ₹       709,284
    ----------------------------------------------------------
    NPV @ 12% : ₹     1,663,597
    
    Decision: ACCEPT — Project creates value



```python
# ── 5.2 Sensitivity Analysis — NPV at Different Discount Rates ───────────────
rates  = np.arange(0.06, 0.22, 0.02)
npvs   = np.array([
    (cash_flows / (1 + r) ** years).sum() for r in rates
])

print('Sensitivity: NPV vs Discount Rate')
print(f'{"Discount Rate":>14} {"NPV":>16} {"Decision":>10}')
print('-' * 45)
for r, n in zip(rates, npvs):
    decision = 'ACCEPT' if n > 0 else 'REJECT'
    print(f'{r*100:>13.0f}%  ₹{n:>14,.0f}  {decision:>10}')

# Approximate IRR (rate where NPV = 0)
sign_changes = np.where(np.diff(np.sign(npvs)))[0]
if len(sign_changes) > 0:
    irr_approx = (rates[sign_changes[0]] + rates[sign_changes[0]+1]) / 2
    print(f'\nApproximate IRR: ~{irr_approx*100:.1f}%')
```

    Sensitivity: NPV vs Discount Rate
     Discount Rate              NPV   Decision
    ---------------------------------------------
                6%  ₹     3,044,033      ACCEPT
                8%  ₹     2,539,481      ACCEPT
               10%  ₹     2,081,078      ACCEPT
               12%  ₹     1,663,597      ACCEPT
               14%  ₹     1,282,501      ACCEPT
               16%  ₹       933,838      ACCEPT
               18%  ₹       614,162      ACCEPT
               20%  ₹       320,452      ACCEPT


---
## Section 6: Portfolio & Investment Risk Analysis

**CA Use-Case:** Reviewing a mutual fund portfolio for a high-net-worth client or analyzing a company's investment portfolio.


```python
# ── 6.1 Monthly Returns for 5 Equity Funds ───────────────────────────────────
np.random.seed(42)
# Simulate 24 months of returns (%) — realistic fund data
fund_returns = np.array([
    [2.1, -1.3, 3.2, 1.8, -0.5, 4.1, 2.8, -2.1, 1.5, 3.3, 0.9, 2.5,
     1.2, 3.8, -1.1, 2.9, 4.2, 0.7, -0.8, 3.5, 1.9, 2.2, -1.5, 3.1],   # Large Cap
    [3.2, -2.1, 4.5, 2.3, -1.2, 5.8, 3.9, -3.4, 2.1, 4.8, 1.2, 3.6,
     2.1, 5.2, -1.8, 4.1, 5.9, 1.1, -1.5, 4.8, 2.7, 3.1, -2.2, 4.4],   # Mid Cap
    [1.5, -0.8, 2.1, 1.2, -0.3, 2.8, 1.9, -1.3, 1.0, 2.3, 0.6, 1.8,
     0.9, 2.6, -0.7, 2.0, 2.9, 0.5, -0.5, 2.4, 1.3, 1.6, -1.0, 2.2],   # Balanced
    [0.6, 0.4, 0.7, 0.6, 0.5, 0.8, 0.7, 0.5, 0.6, 0.8, 0.5, 0.7,
     0.6, 0.7, 0.5, 0.7, 0.8, 0.5, 0.6, 0.7, 0.6, 0.7, 0.5, 0.8],       # Debt
    [4.1, -3.2, 6.2, 3.5, -2.1, 8.1, 5.3, -5.2, 3.1, 6.8, 1.8, 5.1,
     3.2, 7.1, -2.9, 5.8, 8.5, 1.6, -2.3, 6.9, 3.8, 4.4, -3.1, 6.3],   # Small Cap
])

fund_names = ['Large Cap', 'Mid Cap', 'Balanced', 'Debt Fund', 'Small Cap']

# ── 6.2 Key Metrics ──────────────────────────────────────────────────────────
avg_returns  = fund_returns.mean(axis=1)    # average monthly return per fund
annual_ret   = (1 + avg_returns/100)**12 - 1  # annualised
std_devs     = fund_returns.std(axis=1)      # risk (monthly std dev)
sharpe       = avg_returns / std_devs         # simplified Sharpe (risk-free=0)

print(f'{"Fund":<12} {"Avg Monthly Ret":>16} {"Annual Return":>14} {"Std Dev":>9} {"Sharpe":>7}')
print('-' * 65)
for i, name in enumerate(fund_names):
    print(f'{name:<12} {avg_returns[i]:>15.2f}%  {annual_ret[i]*100:>12.2f}%  {std_devs[i]:>8.2f}%  {sharpe[i]:>6.2f}')

best = fund_names[sharpe.argmax()]
print(f'\nBest risk-adjusted fund: {best} (Sharpe: {sharpe.max():.2f})')
```

    Fund          Avg Monthly Ret  Annual Return   Std Dev  Sharpe
    -----------------------------------------------------------------
    Large Cap               1.60%         20.98%      1.88%    0.85
    Mid Cap                 2.19%         29.71%      2.76%    0.79
    Balanced                1.12%         14.37%      1.26%    0.89
    Debt Fund               0.63%          7.82%      0.11%    5.54
    Small Cap               3.03%         43.13%      3.98%    0.76
    
    Best risk-adjusted fund: Debt Fund (Sharpe: 5.54)


---
## Section 7: Key NumPy Functions — Quick Reference

| Function | Financial Use |
|---|---|
| `np.sum()` | Total revenue, total expenses |
| `np.mean()` | Average collection period |
| `np.std()` | Revenue/cost volatility |
| `np.max()` / `np.min()` | Best/worst performing period |
| `np.argmax()` | Month with highest sales |
| `np.cumsum()` | Running total / YTD figures |
| `np.where()` | Conditional logic (like IF in Excel) |
| `np.piecewise()` | Tax slab calculations |
| `np.round()` | Round to nearest rupee |
| `np.clip()` | Cap values (e.g., max credit limit) |


```python
# ── 7.1 Cumulative Revenue (YTD) ─────────────────────────────────────────────
ytd_revenue = np.cumsum(monthly_revenue)
print('Year-to-Date Revenue:')
for m, r, y in zip(months, monthly_revenue, ytd_revenue):
    print(f'  {m}: Monthly ₹{r:>10,.0f}  |  YTD ₹{y:>12,.0f}')

# ── 7.2 np.where — Flag months with below-average revenue ────────────────────
avg_rev = monthly_revenue.mean()
flags   = np.where(monthly_revenue < avg_rev, 'BELOW AVG', 'OK')
print(f'\nMonths below average revenue (₹{avg_rev:,.0f}):')
for m, f in zip(months, flags):
    if f == 'BELOW AVG': print(f'  ⚠ {m}')
```

    Year-to-Date Revenue:
      Apr: Monthly ₹   420,000  |  YTD ₹     420,000
      May: Monthly ₹   385,000  |  YTD ₹     805,000
      Jun: Monthly ₹   450,000  |  YTD ₹   1,255,000
      Jul: Monthly ₹   510,000  |  YTD ₹   1,765,000
      Aug: Monthly ₹   475,000  |  YTD ₹   2,240,000
      Sep: Monthly ₹   525,000  |  YTD ₹   2,765,000
      Oct: Monthly ₹   490,000  |  YTD ₹   3,255,000
      Nov: Monthly ₹   560,000  |  YTD ₹   3,815,000
      Dec: Monthly ₹   610,000  |  YTD ₹   4,425,000
      Jan: Monthly ₹   580,000  |  YTD ₹   5,005,000
      Feb: Monthly ₹   630,000  |  YTD ₹   5,635,000
      Mar: Monthly ₹   720,000  |  YTD ₹   6,355,000
    
    Months below average revenue (₹529,583):
      ⚠ Apr
      ⚠ May
      ⚠ Jun
      ⚠ Jul
      ⚠ Aug
      ⚠ Sep
      ⚠ Oct


---
## Practice Exercises

1. A company has 8 assets. Their costs are ₹2L, ₹4L, ₹6L, ₹8L, ₹10L, ₹3L, ₹5L, ₹7L. All have useful life of 8 years and salvage of 10% of cost. Compute SLM depreciation for each and the total charge for the year.

2. Compute income tax for 5 employees with incomes: ₹5.5L, ₹8L, ₹12L, ₹18L, ₹25L under the new regime.

3. A project requires ₹1 crore investment and generates cash flows of ₹25L per year for 6 years. Compute NPV at 10%, 12%, 14%, 16% and determine the IRR band.

4. Using the monthly_revenue array above, compute: (a) quarterly revenue totals, (b) which quarter had the highest revenue, (c) growth rate from Q1 to Q4.


```python
# ── Exercise Solutions ────────────────────────────────────────────────────────

# Exercise 1: SLM Depreciation
costs_ex = np.array([2, 4, 6, 8, 10, 3, 5, 7]) * 1_00_000
salvage_ex = costs_ex * 0.10
slm_ex = (costs_ex - salvage_ex) / 8
print('Ex 1 — Annual Depreciation:', np.round(slm_ex, 0))
print('       Total charge: ₹', f'{slm_ex.sum():,.0f}')

# Exercise 4: Quarterly Analysis
quarterly = monthly_revenue.reshape(4, 3).sum(axis=1)
qtrs = ['Q1 (Apr-Jun)', 'Q2 (Jul-Sep)', 'Q3 (Oct-Dec)', 'Q4 (Jan-Mar)']
print('\nEx 4 — Quarterly Revenue:')
for q, r in zip(qtrs, quarterly):
    print(f'  {q}: ₹{r:>12,.0f}')
print(f'  Best Quarter: {qtrs[quarterly.argmax()]}')
growth = (quarterly[-1] - quarterly[0]) / quarterly[0] * 100
print(f'  Q1-to-Q4 Growth: {growth:.1f}%')
```

    Ex 1 — Annual Depreciation: [ 22500.  45000.  67500.  90000. 112500.  33750.  56250.  78750.]
           Total charge: ₹ 506,250
    
    Ex 4 — Quarterly Revenue:
      Q1 (Apr-Jun): ₹   1,255,000
      Q2 (Jul-Sep): ₹   1,510,000
      Q3 (Oct-Dec): ₹   1,660,000
      Q4 (Jan-Mar): ₹   1,930,000
      Best Quarter: Q4 (Jan-Mar)
      Q1-to-Q4 Growth: 53.8%



```python

```


```python

```
