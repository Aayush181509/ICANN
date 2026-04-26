# Module 7: Budgeting & Variance Analysis
### Data Science for Chartered Accountants

---

## Learning Objectives
- Compare **Budget vs. Actual** performance at company and department level
- Compute **absolute and percentage variances** and classify Favorable (F) / Unfavorable (U)
- Build a **flexible (flex) budget** that adjusts for actual activity level
- Perform **cost center performance analysis**
- Create a **rolling forecast** based on YTD actuals
- Identify departments with **budget overruns** and compute exposure

---

> **CA Context:** Budgetary control is a core management accounting tool. CAs in industry (CFO/Controller roles) prepare budgets, monitor variances, and present board-level MIS reports. Understanding the data side helps you build these reports 10× faster.


```python
import pandas as pd
import numpy as np

np.random.seed(42)
pd.set_option('display.float_format', '{:,.0f}'.format)
pd.set_option('display.max_columns', 15)

# ── Company: Pinnacle Manufacturing Ltd, FY 2024-25 ───────────────────────────
print('Budgeting & Variance Analysis — Pinnacle Manufacturing Ltd')
print('FY 2024-25 | Amounts in ₹ (Actuals)')
```

---
## Section 1: Annual Budget vs Actuals — P&L Level


```python
# ── Annual P&L Budget vs Actuals ──────────────────────────────────────────────
pl_items = [
    ('Revenue',                  18_00_00_000, 19_25_00_000),
    ('Less: COGS',               10_80_00_000, 11_89_50_000),
    ('Gross Profit',              7_20_00_000,  7_35_50_000),
    ('Less: Staff Costs',         2_16_00_000,  2_31_00_000),
    ('Less: Rent & Utilities',      90_00_000,    93_50_000),
    ('Less: Marketing',           1_08_00_000,  1_42_00_000),
    ('Less: Administration',        72_00_000,    69_00_000),
    ('Less: Depreciation',          54_00_000,    54_00_000),
    ('EBIT',                      1_80_00_000,  1_46_00_000),
    ('Less: Interest',              36_00_000,    39_00_000),
    ('PBT',                       1_44_00_000,  1_07_00_000),
    ('Less: Tax (25%)',             36_00_000,    26_75_000),
    ('PAT',                       1_08_00_000,    80_25_000),
]

pl = pd.DataFrame(pl_items, columns=['Line_Item','Budget','Actual'])
pl['Variance']  = pl['Actual'] - pl['Budget']
pl['Var_Pct']   = (pl['Variance'] / pl['Budget'] * 100).round(1)

# Favorable = revenue higher / expense lower
income_lines = ['Revenue', 'Gross Profit', 'EBIT', 'PBT', 'PAT']
pl['F_or_U'] = pl.apply(
    lambda r: 'F' if (r['Line_Item'] in income_lines and r['Variance'] >= 0) or
                     (r['Line_Item'] not in income_lines and r['Variance'] <= 0)
              else 'U', axis=1
)

print('ANNUAL P&L — BUDGET vs ACTUAL (₹ in Lakhs)')
print(f'{"Line Item":<28} {"Budget (₹L)":>12} {"Actual (₹L)":>12} {"Variance":>10} {"Var%":>7} {"F/U":>4}')
print('-' * 78)
for _, r in pl.iterrows():
    b = r['Budget']/1_00_000; a = r['Actual']/1_00_000; v = r['Variance']/1_00_000
    print(f'{r["Line_Item"]:<28} {b:>12,.0f} {a:>12,.0f} {v:>+10,.0f} {r["Var_Pct"]:>+7.1f}% {r["F_or_U"]:>4}')

print('\nKey Observations:')
pat_var = pl.loc[pl['Line_Item']=='PAT', 'Variance'].values[0]
print(f'  PAT underperformed budget by ₹{abs(pat_var)/1_00_000:.0f} Lakhs ({pl.loc[pl["Line_Item"]=="PAT","Var_Pct"].values[0]:.1f}%)')
mkt_var = pl.loc[pl['Line_Item']=='Less: Marketing','Variance'].values[0]
print(f'  Marketing overspent by ₹{mkt_var/1_00_000:.0f} Lakhs — largest cost overrun')
```

---
## Section 2: Department-wise Monthly Variance Analysis


```python
# ── Monthly Budget & Actuals by Department ────────────────────────────────────
departments = ['Production', 'Sales', 'HR', 'Finance', 'IT', 'Admin']
months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']

# Annual budgets per department (opex)
annual_budgets = {
    'Production': 4_80_00_000,
    'Sales'     : 2_40_00_000,
    'HR'        : 96_00_000,
    'Finance'   : 72_00_000,
    'IT'        : 1_20_00_000,
    'Admin'     : 60_00_000
}

# Monthly seasonality (sums to 1 for each)
seasonality = [0.07, 0.07, 0.08, 0.08, 0.09, 0.09, 0.09, 0.09, 0.10, 0.08, 0.08, 0.08]

records = []
for dept, ann_budget in annual_budgets.items():
    for i, month in enumerate(months):
        monthly_bgt = ann_budget * seasonality[i]
        # Add realistic noise to actuals
        noise_factor = 1 + np.random.normal(0, 0.06)  # ±6% random noise
        if dept == 'Sales' and month in ['Sep', 'Oct', 'Nov']:  # Sales spends more in H2
            noise_factor *= 1.15
        if dept == 'IT' and month in ['Oct', 'Nov']:  # IT project overrun
            noise_factor *= 1.25
        monthly_act = monthly_bgt * noise_factor
        records.append({'Department': dept, 'Month': month, 'Month_No': i+1,
                         'Budget': round(monthly_bgt, -3),
                         'Actual': round(monthly_act, -3)})

dept_monthly = pd.DataFrame(records)
dept_monthly['Variance']  = dept_monthly['Actual'] - dept_monthly['Budget']
dept_monthly['Var_Pct']   = dept_monthly['Variance'] / dept_monthly['Budget'] * 100
dept_monthly['F_or_U']    = dept_monthly['Variance'].apply(lambda v: 'F' if v <= 0 else 'U')

# YTD (full year)
dept_ytd = dept_monthly.groupby('Department').agg(
    Budget    = ('Budget','sum'),
    Actual    = ('Actual','sum'),
    Variance  = ('Variance','sum')
).reset_index()
dept_ytd['Var_Pct'] = dept_ytd['Variance'] / dept_ytd['Budget'] * 100
dept_ytd['F_or_U']  = dept_ytd['Variance'].apply(lambda v: 'F ✓' if v <= 0 else 'U ✗')

print('ANNUAL DEPARTMENT BUDGET PERFORMANCE')
print(f'{"Department":<14} {"Budget (₹L)":>12} {"Actual (₹L)":>12} {"Variance":>12} {"Var%":>8} {"Status":>7}')
print('-' * 68)
for _, r in dept_ytd.iterrows():
    b = r['Budget']/1_00_000; a = r['Actual']/1_00_000; v = r['Variance']/1_00_000
    print(f'{r["Department"]:<14} {b:>12,.0f} {a:>12,.0f} {v:>+12,.0f} {r["Var_Pct"]:>+7.1f}%  {r["F_or_U"]:>7}')

total_overrun = dept_ytd[dept_ytd['Variance'] > 0]['Variance'].sum()
print(f'\nTotal Budget Overrun: ₹{total_overrun/1_00_000:,.0f} Lakhs')
```


```python
# ── Monthly Variance Trend for Top Overspending Department ────────────────────
worst_dept = dept_ytd.sort_values('Variance', ascending=False).iloc[0]['Department']
print(f'MONTHLY VARIANCE TREND: {worst_dept}')
print(f'{"Month":<6} {"Budget (₹L)":>12} {"Actual (₹L)":>12} {"Variance":>10} {"Var%":>8} {"F/U":>4}')
print('-' * 58)
dept_trend = dept_monthly[dept_monthly['Department']==worst_dept].sort_values('Month_No')
for _, r in dept_trend.iterrows():
    b = r['Budget']/1_00_000; a = r['Actual']/1_00_000; v = r['Variance']/1_00_000
    flag = '⚠' if r['Var_Pct'] > 10 else ''
    print(f'{r["Month"]:<6} {b:>12,.0f} {a:>12,.0f} {v:>+10,.0f} {r["Var_Pct"]:>+7.1f}%  {r["F_or_U"]:>4} {flag}')
```

---
## Section 3: Flexible Budget Analysis

A **flexible budget** adjusts for the **actual level of activity** — enabling fairer comparison.

**Formula:**
$$\text{Flex Budget} = \text{Fixed Cost} + (\text{Variable Rate} \times \text{Actual Output})$$

| Variance Type | Formula |
|---|---|
| Static variance | Actual - Original Budget |
| Activity variance | Flex Budget - Original Budget |
| Spending variance | Actual - Flex Budget |


```python
# ── Flexible Budget for Production Department ──────────────────────────────────
# Budgeted production: 10,000 units; Actual production: 11,500 units
budgeted_units = 10_000
actual_units   = 11_500
activity_ratio = actual_units / budgeted_units  # 1.15 = 15% more output

# Cost structure of Production department
prod_costs = pd.DataFrame({
    'Cost_Element'   : ['Raw Materials', 'Direct Labour', 'Factory Power',
                        'Variable Overhead', 'Factory Rent', 'Depreciation', 'Supervisory Staff'],
    'Cost_Type'      : ['Variable','Variable','Variable','Variable','Fixed','Fixed','Fixed'],
    'Budget_Total'   : [2_40_00_000, 1_20_00_000, 48_00_000, 36_00_000, 24_00_000, 18_00_000, 24_00_000],
    'Actual_Total'   : [2_85_00_000, 1_35_00_000, 55_00_000, 41_00_000, 24_00_000, 18_00_000, 25_00_000]
})

# Flex budget: variable costs scale with activity, fixed costs stay fixed
prod_costs['Flex_Budget'] = prod_costs.apply(
    lambda r: r['Budget_Total'] * activity_ratio if r['Cost_Type'] == 'Variable'
              else r['Budget_Total'], axis=1
).round(-3)

prod_costs['Static_Variance']   = prod_costs['Actual_Total'] - prod_costs['Budget_Total']
prod_costs['Activity_Variance'] = prod_costs['Flex_Budget']  - prod_costs['Budget_Total']
prod_costs['Spending_Variance'] = prod_costs['Actual_Total'] - prod_costs['Flex_Budget']

def fav(v):
    return f'₹{abs(v)/1_00_000:,.0f}L (F)' if v <= 0 else f'₹{abs(v)/1_00_000:,.0f}L (U)'

print(f'PRODUCTION FLEX BUDGET ANALYSIS')
print(f'Budgeted Units: {budgeted_units:,}  |  Actual Units: {actual_units:,}  |  Activity Ratio: {activity_ratio:.2f}')
print()
print(f'{"Cost Element":<22} {"Type":>8} {"Budget":>12} {"Flex Bgt":>12} {"Actual":>12} {"Spend Var":>12}')
print('-' * 82)
for _, r in prod_costs.iterrows():
    print(f'{r["Cost_Element"]:<22} {r["Cost_Type"]:>8} ₹{r["Budget_Total"]/1_00_000:>9,.0f}L ₹{r["Flex_Budget"]/1_00_000:>9,.0f}L ₹{r["Actual_Total"]/1_00_000:>9,.0f}L  {fav(r["Spending_Variance"]):>14}')

print('-' * 82)
print(f'{"TOTAL":<22} {"":>8} ₹{prod_costs["Budget_Total"].sum()/1_00_000:>9,.0f}L ₹{prod_costs["Flex_Budget"].sum()/1_00_000:>9,.0f}L ₹{prod_costs["Actual_Total"].sum()/1_00_000:>9,.0f}L  {fav(prod_costs["Spending_Variance"].sum()):>14}')
print(f'\nConclusion: Producing 15% more units incurred {abs(prod_costs["Spending_Variance"].sum())/1_00_000:.0f}L in excess spending (efficiency loss)')
```

---
## Section 4: Cost Centre MIS Report


```python
# ── Cost Centre MIS Report ────────────────────────────────────────────────────
# Multi-dimensional: Department × Month × Cost Head
cost_heads = ['Salaries', 'Travel', 'Marketing', 'IT Infra', 'Repairs', 'Misc']

# Generate synthetic cost-centre data
cc_records = []
head_allocations = {
    'Production': {'Salaries':0.5,'Travel':0.05,'Marketing':0,'IT Infra':0.1,'Repairs':0.2,'Misc':0.15},
    'Sales'     : {'Salaries':0.4,'Travel':0.2,'Marketing':0.3,'IT Infra':0.02,'Repairs':0,'Misc':0.08},
    'HR'        : {'Salaries':0.7,'Travel':0.05,'Marketing':0.05,'IT Infra':0.05,'Repairs':0,'Misc':0.15},
    'Finance'   : {'Salaries':0.65,'Travel':0.1,'Marketing':0,'IT Infra':0.1,'Repairs':0,'Misc':0.15},
    'IT'        : {'Salaries':0.5,'Travel':0.05,'Marketing':0,'IT Infra':0.35,'Repairs':0.05,'Misc':0.05},
    'Admin'     : {'Salaries':0.45,'Travel':0.1,'Marketing':0,'IT Infra':0.1,'Repairs':0.15,'Misc':0.2}
}

for dept, ann_bgt in annual_budgets.items():
    for head, share in head_allocations[dept].items():
        head_annual_bgt = ann_bgt * share
        head_actual     = head_annual_bgt * (1 + np.random.normal(0, 0.08))
        cc_records.append({
            'Department': dept,
            'Cost_Head' : head,
            'Budget'    : round(head_annual_bgt, -3),
            'Actual'    : round(head_actual, -3)
        })

cc_df = pd.DataFrame(cc_records)
cc_df['Variance'] = cc_df['Actual'] - cc_df['Budget']
cc_df['Var_Pct']  = cc_df['Variance'] / cc_df['Budget'] * 100

# Pivot: Cost Head as rows, Department as columns
cc_pivot = cc_df.pivot_table(values='Variance', index='Cost_Head', columns='Department', aggfunc='sum')
cc_pivot = cc_pivot.fillna(0) / 1_00_000  # convert to lakhs

print('COST CENTRE VARIANCE PIVOT (₹ Lakhs — Positive = Overrun)')
print(cc_pivot.round(1).to_string())
print(f'\nWorst performing cost head: {cc_pivot.sum(axis=1).idxmax()} (₹{cc_pivot.sum(axis=1).max():.0f}L overrun)')
```

---
## Section 5: Rolling Forecast (Full Year Projection)


```python
# ── Rolling Forecast Logic ────────────────────────────────────────────────────
# Assume we are at Month 9 (Dec 2024) — 9 months actual, 3 months to forecast
current_month = 9

revenue_budget_monthly  = [18_00_00_000 * s for s in seasonality]
revenue_actual_monthly  = [
    1_25_00_000, 1_40_00_000, 1_35_00_000, 1_55_00_000, 1_65_00_000,
    1_60_00_000, 1_70_00_000, 1_80_00_000, 1_88_00_000,
    0, 0, 0  # Jan-Mar not yet available
]

revenue_df = pd.DataFrame({
    'Month'  : months,
    'Budget' : revenue_budget_monthly,
    'Actual' : revenue_actual_monthly
})

# Forecast remaining months using average run-rate of last 3 months
last3_avg = np.mean(revenue_actual_monthly[current_month-3:current_month])
for i in range(current_month, 12):
    # Apply same seasonal factor
    revenue_df.loc[i, 'Forecast'] = round(
        last3_avg * (seasonality[i] / np.mean(seasonality[current_month-3:current_month])), -3
    )

revenue_df['Forecast'] = revenue_df.apply(
    lambda r: r['Actual'] if r['Actual'] > 0 else r.get('Forecast', 0), axis=1
)
revenue_df['Variance']    = revenue_df['Forecast'] - revenue_df['Budget']
revenue_df['Var_Pct']     = revenue_df['Variance'] / revenue_df['Budget'] * 100
revenue_df['Source']      = revenue_df['Actual'].apply(
    lambda a: 'Actual' if a > 0 else 'Forecast'
)

print('ROLLING FORECAST — REVENUE (₹ Lakhs)')
print(f'{"Month":<6} {"Budget":>9} {"Actual/Forecast":>16} {"Variance":>10} {"Var%":>7} {"Source":>9}')
print('-' * 62)
for _, r in revenue_df.iterrows():
    b = r['Budget']/1_00_000; f = r['Forecast']/1_00_000; v = r['Variance']/1_00_000
    mark = '◀ Forecast' if r['Source'] == 'Forecast' else ''
    print(f'{r["Month"]:<6} ₹{b:>7,.0f}L ₹{f:>13,.0f}L {v:>+9,.0f}L {r["Var_Pct"]:>+6.1f}% {mark}')

print('-' * 62)
totals = revenue_df[['Budget','Forecast','Variance']].sum()
print(f'{"FY TOTAL":<6} ₹{totals["Budget"]/1_00_000:>7,.0f}L ₹{totals["Forecast"]/1_00_000:>13,.0f}L {totals["Variance"]/1_00_000:>+9,.0f}L')
print(f'\nFull-Year Revenue Forecast: ₹{totals["Forecast"]/1_00_00_000:.2f} Crores vs Budget ₹{totals["Budget"]/1_00_00_000:.2f} Crores')
```

---
## Section 6: Capital Budget Monitoring


```python
# ── Capital Expenditure Budget ─────────────────────────────────────────────────
capex = pd.DataFrame({
    'Project'       : ['Plant Expansion', 'IT System Upgrade', 'Warehouse Construction',
                       'Fleet Purchase', 'Lab Equipment', 'Solar Installation'],
    'Approved_Budget': [5_00_00_000, 1_20_00_000, 3_50_00_000, 80_00_000, 60_00_000, 1_50_00_000],
    'Spent_to_Date' : [4_85_00_000, 1_38_00_000, 2_10_00_000, 78_00_000, 45_00_000, 50_00_000],
    'Committed'     : [20_00_000, 5_00_000, 1_80_00_000, 5_00_000, 12_00_000, 95_00_000],
    'Status'        : ['On Track', 'Overspent', 'In Progress', 'Complete', 'In Progress', 'In Progress']
})

capex['Total_Exposure'] = capex['Spent_to_Date'] + capex['Committed']
capex['Remaining_Budget'] = capex['Approved_Budget'] - capex['Total_Exposure']
capex['Overrun'] = capex['Total_Exposure'] - capex['Approved_Budget']
capex['Pct_Utilised'] = capex['Spent_to_Date'] / capex['Approved_Budget'] * 100

print('CAPITAL BUDGET MONITORING REPORT (₹ Lakhs)')
print(f'{"Project":<24} {"Approved":>10} {"Spent":>10} {"Committed":>10} {"Remaining":>10} {"% Used":>7} {"Status"}')
print('-' * 80)
for _, r in capex.iterrows():
    remaining = max(0, r['Remaining_Budget'])
    flag = ' ⚠ OVERRUN' if r['Overrun'] > 0 else ''
    print(f'{r["Project"]:<24} ₹{r["Approved_Budget"]/1_00_000:>7,.0f}L ₹{r["Spent_to_Date"]/1_00_000:>7,.0f}L ₹{r["Committed"]/1_00_000:>7,.0f}L ₹{remaining/1_00_000:>7,.0f}L {r["Pct_Utilised"]:>6.0f}%  {r["Status"]}{flag}')

overrun_projects = capex[capex['Overrun'] > 0]
print(f'\nProjects with overrun: {len(overrun_projects)}')
print(f'Total overrun exposure: ₹{overrun_projects["Overrun"].sum()/1_00_000:,.0f} Lakhs')
```

---
## Practice Exercises

1. For each department, compute the **absolute variance that would have been acceptable** if the company allowed ±5% tolerance. Flag all that breach this band.

2. Using the rolling forecast, calculate how much **additional revenue growth is needed in Q4** to hit the original full-year budget target.

3. Build a **traffic-light system**: Green (within 5%), Amber (5-15% overrun), Red (>15% overrun) for the department budget table.

4. Apply **flex budget principles** to the Sales department assuming actual sales calls were 12,000 vs budgeted 10,000.

5. Compute the **Return on Investment (ROI)** and payback period for each CapEx project, assuming each generates revenue equal to 20% of project value annually.


```python
# ── Exercise Solutions ─────────────────────────────────────────────────────────

# Exercise 3: Traffic Light System
dept_ytd['Traffic_Light'] = dept_ytd['Var_Pct'].apply(
    lambda p: '🟢 Green'  if abs(p) <= 5  else
              '🟡 Amber'  if abs(p) <= 15 else
              '🔴 Red'
)

print('Ex 3 — Traffic Light System:')
print(dept_ytd[['Department','Budget','Actual','Var_Pct','Traffic_Light']].to_string(index=False))

# Exercise 5: CapEx ROI
capex['Annual_Return']    = capex['Approved_Budget'] * 0.20
capex['Payback_Years']    = capex['Approved_Budget'] / capex['Annual_Return']
capex['ROI_10yr_pct']     = (capex['Annual_Return'] * 10 / capex['Approved_Budget']) * 100

print('\nEx 5 — CapEx ROI Analysis:')
print(capex[['Project','Approved_Budget','Annual_Return','Payback_Years','ROI_10yr_pct']].round(1).to_string(index=False))
```
