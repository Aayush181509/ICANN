"""
Generate dummy Nepali business / financial data CSV files for the
ICAN training session notebooks.

Run:  python3 _generate_data.py
Output: writes CSV files to ./data/
"""
import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

OUT = Path(__file__).parent / "data"
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Monthly sales — Nepali FY 2081-82 BS (Shrawan → Ashadh)
# ---------------------------------------------------------------------------
months = ["Shrawan", "Bhadra", "Ashwin", "Kartik", "Mangsir", "Poush",
          "Magh", "Falgun", "Chaitra", "Baishakh", "Jestha", "Ashadh"]

sales = pd.DataFrame({
    "Month": months,
    "Revenue_NPR":  [1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
                     1550000, 1420000, 1680000, 1910000, 2030000, 2150000],
    "Expense_NPR":  [ 920000,  980000,  870000, 1050000, 1180000, 1250000,
                     1100000, 1020000, 1190000, 1320000, 1410000, 1490000],
    "Units_Sold":   [  420,    465,    380,    498,    540,    605,
                       515,    478,    560,    640,    690,    720],
})
sales.to_csv(OUT / "monthly_sales.csv", index=False)


# ---------------------------------------------------------------------------
# 2. Invoice ledger — 200 invoices, 13% VAT, various customers
# ---------------------------------------------------------------------------
n_inv = 200
customers = ["Himalayan Traders", "Everest Suppliers", "Annapurna Stores",
             "Kathmandu Distributors", "Pokhara Mart", "Lumbini Imports",
             "Janakpur Wholesale", "Biratnagar Enterprise", "Nepalgunj Goods",
             "Birgunj Cargo"]
cities = ["Kathmandu", "Lalitpur", "Bhaktapur", "Pokhara", "Biratnagar",
          "Birgunj", "Janakpur", "Nepalgunj", "Butwal", "Hetauda"]
products = ["Stationery", "Electronics", "Textile", "Hardware", "Food", "Cosmetics"]

inv = pd.DataFrame({
    "Invoice_No":   [f"INV-{2081}{i:04d}" for i in range(1, n_inv + 1)],
    "Date":         pd.date_range("2024-07-16", periods=n_inv, freq="2D"),
    "Customer":     np.random.choice(customers, n_inv),
    "City":         np.random.choice(cities, n_inv),
    "Product":      np.random.choice(products, n_inv),
    "Quantity":     np.random.randint(1, 50, n_inv),
    "Unit_Price":   np.round(np.random.uniform(150, 8500, n_inv), 0),
})
inv["Amount_NPR"] = inv["Quantity"] * inv["Unit_Price"]
inv["VAT_NPR"]    = np.round(inv["Amount_NPR"] * 0.13, 2)
inv["Total_NPR"]  = inv["Amount_NPR"] + inv["VAT_NPR"]
inv["Payment_Status"] = np.random.choice(["Paid", "Pending", "Overdue"],
                                          n_inv, p=[0.6, 0.25, 0.15])
# Inject some realistic dirtiness for the cleaning notebook
dirty = inv.copy()
dirty.loc[np.random.choice(dirty.index, 12, replace=False), "Amount_NPR"] = np.nan
dirty.loc[np.random.choice(dirty.index, 8,  replace=False), "City"] = np.nan
dirty.loc[np.random.choice(dirty.index, 5,  replace=False), "Customer"] = "  himalayan traders "
dirty.loc[np.random.choice(dirty.index, 3,  replace=False), "Customer"] = "EVEREST SUPPLIERS"
# duplicates
dirty = pd.concat([dirty, dirty.sample(6, random_state=1)], ignore_index=True)
inv.to_csv(OUT / "invoices.csv", index=False)
dirty.to_csv(OUT / "invoices_dirty.csv", index=False)


# ---------------------------------------------------------------------------
# 3. NEPSE-style stock prices — 12 months for 5 listed companies
# ---------------------------------------------------------------------------
tickers = ["NABIL", "NTC", "NICA", "CHCL", "HDL"]
base    = {"NABIL": 1200, "NTC": 950, "NICA": 720, "CHCL": 540, "HDL": 880}
prices = {"Month": months}
rng = np.random.default_rng(7)
for t in tickers:
    drift = rng.normal(loc=0.018, scale=0.05, size=12)  # ~1.8% monthly drift
    walk  = np.cumprod(1 + drift)
    prices[t] = np.round(base[t] * walk, 2)
pd.DataFrame(prices).to_csv(OUT / "nepse_prices.csv", index=False)


# ---------------------------------------------------------------------------
# 4. Payroll — 25 employees
# ---------------------------------------------------------------------------
nep_first = ["Ramesh", "Sita", "Hari", "Sunita", "Bikash", "Anita", "Prakash",
             "Kabita", "Dipesh", "Nisha", "Suman", "Rekha", "Saroj", "Pratima",
             "Manoj", "Kalpana", "Rajesh", "Sushila", "Deepak", "Gita",
             "Mukesh", "Sarita", "Arjun", "Laxmi", "Bishnu"]
nep_last  = ["Sharma", "Karki", "Shrestha", "Adhikari", "Gurung", "Tamang",
             "Magar", "Rai", "Limbu", "KC", "Thapa", "Bhattarai", "Pandey",
             "Lamichhane", "Rana", "Pokhrel", "Acharya", "Dahal", "Joshi",
             "Khadka", "Basnet", "Maharjan", "Bhandari", "Subedi", "Paudel"]
depts = ["Audit", "Tax", "Advisory", "Finance", "HR"]
designations = ["Junior", "Senior", "Manager", "Director"]

pay = pd.DataFrame({
    "Emp_ID":       [f"E{1000+i}" for i in range(25)],
    "Name":         [f"{f} {l}" for f, l in zip(nep_first, nep_last)],
    "Department":   np.random.choice(depts, 25),
    "Designation":  np.random.choice(designations, 25, p=[0.4, 0.35, 0.2, 0.05]),
    "Years_Exp":    np.random.randint(1, 25, 25),
    "Basic_Salary": np.random.choice([35000, 45000, 60000, 85000, 120000, 180000, 250000], 25),
})
pay["Allowance"]   = (pay["Basic_Salary"] * 0.4).round(0)
pay["Gross"]       = pay["Basic_Salary"] + pay["Allowance"]
pay["EPF_10pct"]   = (pay["Basic_Salary"] * 0.10).round(0)
pay["SSF_1pct"]    = (pay["Gross"] * 0.01).round(0)
pay["Net_Salary"]  = pay["Gross"] - pay["EPF_10pct"] - pay["SSF_1pct"]
pay.to_csv(OUT / "payroll.csv", index=False)


# ---------------------------------------------------------------------------
# 5. Loan portfolio — for classification (300 loans)
# ---------------------------------------------------------------------------
n = 300
rng = np.random.default_rng(11)
loans = pd.DataFrame({
    "Loan_ID":       [f"L{2000+i}" for i in range(n)],
    "Customer":      [f"Cust_{i:03d}" for i in range(n)],
    "Loan_Amount":   rng.choice([100000, 250000, 500000, 1000000, 2500000, 5000000], n,
                                p=[0.15, 0.2, 0.25, 0.2, 0.15, 0.05]),
    "Tenure_Months": rng.choice([12, 24, 36, 60, 120], n),
    "Interest_Rate": np.round(rng.uniform(8, 16, n), 2),
    "Annual_Income": rng.choice([180000, 360000, 600000, 1200000, 2400000], n,
                                 p=[0.2, 0.3, 0.25, 0.15, 0.1]),
    "Credit_Score":  rng.integers(300, 850, n),
    "Has_Collateral": rng.choice(["Yes", "No"], n, p=[0.6, 0.4]),
    "Sector":        rng.choice(["Agriculture", "Trade", "Manufacturing",
                                  "Service", "Personal"], n),
})
# Synthetic default rule: low credit + high loan-to-income + no collateral
lti = loans["Loan_Amount"] / loans["Annual_Income"]
prob = 1 / (1 + np.exp(-( -2 + (700 - loans["Credit_Score"]) / 200 + lti * 0.3
                          + (loans["Has_Collateral"] == "No") * 0.6 )))
loans["Defaulted"] = (rng.random(n) < prob).astype(int)
loans.to_csv(OUT / "loans.csv", index=False)


# ---------------------------------------------------------------------------
# 6. Customer master with credit info (for feature engineering)
# ---------------------------------------------------------------------------
n_cust = 150
cust = pd.DataFrame({
    "Customer_ID":   [f"C{500+i}" for i in range(n_cust)],
    "Customer_Name": rng.choice(customers, n_cust),
    "Onboarded_Date": pd.to_datetime("2022-01-01") + pd.to_timedelta(
                        rng.integers(0, 1000, n_cust), unit="D"),
    "City":          rng.choice(cities, n_cust),
    "Annual_Revenue": rng.choice([500000, 1500000, 5000000, 15000000, 50000000], n_cust,
                                  p=[0.25, 0.3, 0.25, 0.15, 0.05]),
    "Credit_Limit":  rng.choice([100000, 250000, 500000, 1000000, 2500000], n_cust),
    "Outstanding":   0,
})
cust["Outstanding"] = (cust["Credit_Limit"] * rng.uniform(0, 1.3, n_cust)).round(0)
cust["Days_Past_Due"] = rng.choice([0, 0, 0, 15, 30, 60, 90, 120], n_cust)
cust.to_csv(OUT / "customers.csv", index=False)


# ---------------------------------------------------------------------------
# 7. Daily revenue — for regression (90 days)
# ---------------------------------------------------------------------------
days = pd.date_range("2024-07-16", periods=90, freq="D")
ads_spend = rng.uniform(2000, 25000, 90).round(0)
footfall  = rng.integers(50, 500, 90)
weekend   = (days.weekday >= 5).astype(int)
holiday   = rng.choice([0, 1], 90, p=[0.92, 0.08])

# True relationship + noise
daily_rev = (15000
             + 8 * ads_spend
             + 250 * footfall
             + 12000 * weekend
             + 35000 * holiday
             + rng.normal(0, 15000, 90)).round(0)

daily = pd.DataFrame({
    "Date":       days,
    "Ads_Spend":  ads_spend,
    "Footfall":   footfall,
    "Is_Weekend": weekend,
    "Is_Festival": holiday,
    "Revenue":    daily_rev,
})
daily.to_csv(OUT / "daily_revenue.csv", index=False)


# ---------------------------------------------------------------------------
# 8. Trial balance — for data cleaning + pandas selection
# ---------------------------------------------------------------------------
tb = pd.DataFrame({
    "Account_Code": ["1001", "1002", "1100", "1200", "1500", "2001", "2100",
                     "3000", "4001", "4002", "5001", "5002", "5100", "5200"],
    "Account_Name": ["Cash in Hand", "Bank - NIC Asia", "Accounts Receivable",
                     "Inventory", "Fixed Assets", "Accounts Payable",
                     "Long-term Loan", "Capital", "Sales Revenue",
                     "Service Revenue", "Salaries", "Rent", "Utilities",
                     "Office Supplies"],
    "Type":         ["Asset", "Asset", "Asset", "Asset", "Asset",
                     "Liability", "Liability", "Equity",
                     "Revenue", "Revenue",
                     "Expense", "Expense", "Expense", "Expense"],
    "Debit":   [ 285000,  1450000,  920000, 1850000, 4500000,       0,       0,
                     0,       0,       0, 1800000,  480000,  220000,  85000],
    "Credit":  [      0,        0,       0,       0,       0,  680000, 2500000,
               5000000, 3200000, 1610000,       0,       0,       0,       0],
})
tb.to_csv(OUT / "trial_balance.csv", index=False)


# ---------------------------------------------------------------------------
# 9. P&L data — simple for charts
# ---------------------------------------------------------------------------
pl = pd.DataFrame({
    "Quarter":        ["Q1", "Q2", "Q3", "Q4"],
    "Revenue":        [3750000, 4850000, 4650000, 6090000],
    "COGS":           [2100000, 2710000, 2580000, 3300000],
    "Operating_Exp":  [ 670000,  720000,  720000,  920000],
    "Tax":            [ 175000,  240000,  225000,  340000],
})
pl["Gross_Profit"]   = pl["Revenue"] - pl["COGS"]
pl["Net_Profit"]     = pl["Gross_Profit"] - pl["Operating_Exp"] - pl["Tax"]
pl.to_csv(OUT / "quarterly_pl.csv", index=False)


print("\nGenerated CSV files:")
for f in sorted(OUT.iterdir()):
    if f.suffix == ".csv":
        print(f"  {f.name:30s}  {f.stat().st_size:>8,} bytes")
