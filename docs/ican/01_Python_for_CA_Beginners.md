# Python for CA Professionals
**A Complete Beginner's Guide**

---

**Welcome!** You've spent years mastering financial statements, auditing standards, and tax laws.  
Now it's time to add one more powerful tool to your arsenal: **Python**.

> *"Python is the Excel of the future — except it can do in 3 lines what Excel takes 30 clicks to do."*

### Who is this notebook for?

- CA graduates and finance professionals
- Absolute beginners — **zero coding experience required**
- Anyone who wants to automate repetitive financial tasks

### What will you learn?

By the end of this notebook, you will be able to:
- Write your first Python programs
- Work with numbers, text, and data — just like in Excel but far more powerful
- Build a simple tax calculator and financial report generator
- Automate repetitive calculations

### How to use this notebook

- Each **grey box** below is a **code cell** — it contains Python code you can run
- Click on a code cell and press **Shift + Enter** to run it
- **Markdown cells** (like this one) contain explanations — just read them
- Try changing the numbers in code cells and re-run them — experimentation is the best teacher!

---
⏱️ **Estimated time:** 3–4 hours (you can go at your own pace)

### 📋 Table of Contents

| # | Topic | What you'll learn |
|---|-------|-------------------|
| 1 | What is Python? | Why Python matters for finance |
| 2 | Your First Program | `print()`, comments |
| 3 | Variables | Storing values, naming rules |
| 4 | Data Types | Numbers, text, True/False |
| 5 | Python as a Calculator | Arithmetic, tax & interest calculations |
| 6 | Making Decisions | `if / elif / else`, tax brackets |
| 7 | Working with Text | Strings, formatting financial reports |
| 8 | Lists | Collections of data, expense lists |
| 9 | Dictionaries | Key-value data, ledger records |
| 10 | Loops | Automating repetitive work |
| 11 | Functions | Reusable code, tax calculator |
| 12 | Practice Exercises | Test your skills |

---

## Section 1: What is Python?

### Think of Python as a very smart assistant

Imagine you have a new junior staff member who:
- Does **exactly** what you tell them, every single time
- Works **24/7** without complaining
- Can process **thousands of transactions** in seconds
- **Never makes arithmetic mistakes**

That's Python.

### Why do CA professionals use Python?

| Task | Without Python | With Python |
|------|---------------|-------------|
| Calculate VAT on 500 invoices | 30 minutes in Excel | 2 seconds |
| Classify expenses into categories | Manual, error-prone | Automatic |
| Generate financial reports | Hours of formatting | Minutes |
| Detect anomalies in transactions | Sampling only | 100% coverage |
| Reconcile bank statements | Tedious VLOOKUP | One command |

### Python in the real world (Finance)
- **Big 4 firms** use Python for data analytics and audit automation
- **Banks** use Python for risk modelling and fraud detection
- **Tax authorities** (like IRD) use Python to analyse return data
- **Stock exchanges** use Python for real-time data processing

---
💡 **Key insight:** Python does not replace your CA knowledge. It **multiplies** it.

## Section 2: Your First Python Program

### The `print()` function

The most basic thing Python can do is **display a message on screen**.  
We use the `print()` function for this.

**Syntax:** `print('your message here')`

Think of `print()` as Python's way of **speaking to you**.  
Whatever you put inside the brackets (in quotes) will be displayed.

Let's run our first program:


```python
print('Hello, World!')
```

    Hello, World!


Congratulations! 🎉 You just wrote your first Python program!

Now let's try something more relevant to our work:


```python
print('Welcome to Python for Finance!')
print('This notebook will help CA professionals automate their work.')
print('Let us get started!')
```

    Welcome to Python for Finance!
    This notebook will help CA professionals automate their work.
    Let us get started!


### Comments — Notes to yourself

In your audit working papers, you write notes explaining your work.  
In Python, we do the same using **comments**.

A comment starts with `#` (hash symbol). Python **completely ignores** anything after `#` on that line.  
Comments are for **humans** to read — they help explain what the code is doing.


```python
# This is a comment — Python ignores this line
print('Fiscal Year 2081-82 BS (Mid-July 2024 to Mid-July 2025)')  # You can also add comments at the end of a line

# The line below prints the company name
print('Sunrise Trading Pvt. Ltd.')

# Always write comments to explain WHY you wrote the code, not just WHAT it does
```

    Fiscal Year 2081-82 BS (Mid-July 2024 to Mid-July 2025)
    Sunrise Trading Pvt. Ltd.


#### ✏️ Mini Exercise 1

In the cell below, write a Python program that prints:
1. Your name
2. Your firm name (or any name)
3. Today's date

Add a comment before each print statement explaining what it does.


```python
# Write your code here



```

## Section 3: Variables — Storing Information

### What is a variable?

In accounting, you have **ledger accounts** — each account holds a value (like Cash Account = NPR 50,000).

In Python, a **variable** is the same concept — it's a named container that holds a value.

```
cash_balance = 50000
     ↑              ↑
 account name    account value
```

The `=` sign means **"store this value in this variable"** (it does NOT mean "equal to" the way it does in maths).

Once you create a variable, you can use it anywhere in your code.


```python
# Creating variables — storing financial data
revenue = 1500000       # Total revenue: NPR 15,00,000
expenses = 980000       # Total expenses: NPR 9,80,000
tax_rate = 0.30         # Tax rate: 30%
company_name = 'Sunrise Trading Pvt. Ltd.'

# Now we can USE these variables
print(company_name)
print(revenue)
print(expenses)
print(tax_rate)
```

    Sunrise Trading Pvt. Ltd.
    1500000
    980000
    0.3



```python
# Variables can be used in calculations — just like cell references in Excel
profit = revenue - expenses
print('Profit before tax:', profit)

tax_payable = profit * tax_rate
print('Tax payable:', tax_payable)

profit_after_tax = profit - tax_payable
print('Profit after tax:', profit_after_tax)
```

    Profit before tax: 520000
    Tax payable: 156000.0
    Profit after tax: 364000.0


### Rules for naming variables

Just like account names follow conventions in accounting, variable names follow rules in Python:

| Rule | Example |
|------|---------|
| Use letters, numbers, underscores only | `tax_rate`, `profit2024` |
| Must start with a letter or underscore | `revenue` ✅  &nbsp;&nbsp; `1revenue` ❌ |
| No spaces — use underscore instead | `net_profit` ✅  &nbsp;&nbsp; `net profit` ❌ |
| Case-sensitive | `Revenue` and `revenue` are **different** variables |
| Use descriptive names | `tax_payable` ✅  &nbsp;&nbsp; `t` ❌ |

**Convention:** Use lowercase with underscores (this is called `snake_case` — very common in Python)


```python
# Good variable names — descriptive and clear
gross_salary = 1200000
standard_deduction = 50000
hra_exemption = 180000
taxable_income = gross_salary - standard_deduction - hra_exemption

print('Taxable Income:', taxable_income)

# Variables can be updated (reassigned)
gross_salary = 1500000  # Got a raise!
print('Updated salary:', gross_salary)
```

    Taxable Income: 970000
    Updated salary: 1500000


#### ✏️ Mini Exercise 2

Create variables for the following Balance Sheet items and print them:
- Share Capital: NPR 5,00,000
- Reserves & Surplus: NPR 2,50,000
- Long-term Debt: NPR 3,00,000
- Calculate and print: **Total Equity + Debt**


```python
# Write your code here



```

## Section 4: Data Types — Types of Information

### Every piece of data has a type

In accounting, data comes in different forms:
- **Amounts** — NPR 50,000 (numbers)
- **Client names** — "Reliance Industries" (text)
- **Audit status** — Yes/No (True/False)

Python has corresponding **data types** for each of these:

| Python Type | What it stores | Example |
|-------------|---------------|---------|
| `int` | Whole numbers | `1000`, `-500`, `0` |
| `float` | Decimal numbers | `18.5`, `0.30`, `99.99` |
| `str` | Text (string) | `'Revenue'`, `'ABC Ltd'` |
| `bool` | True or False | `True`, `False` |

You can check the type of any value using the `type()` function.


```python
# int — whole numbers (no decimal point)
number_of_invoices = 250
number_of_employees = 48
financial_year = 2025

print('Number of invoices:', number_of_invoices)
print('Type:', type(number_of_invoices))  # Shows the data type
```

    Number of invoices: 250
    Type: <class 'int'>



```python
# float — numbers with a decimal point
vat_rate = 13.0          # 13% Nepal VAT rate
income_tax_rate = 25.0   # Nepal corporate income tax rate
interest_rate = 8.5      # 8.5% interest rate
invoice_amount = 47500.75

print('VAT Rate:', vat_rate)
print('Type:', type(vat_rate))
print('Invoice Amount:', invoice_amount)
```

    VAT Rate: 13.0
    Type: <class 'float'>
    Invoice Amount: 47500.75



```python
# str (string) — text data
# Strings are ALWAYS enclosed in quotes (single '' or double "")

client_name = 'Himalayan Tech Solutions Pvt. Ltd.'
audit_period = 'Shrawan 2081 to Ashadh 2082 BS'
pan_number = '123456789'  # Nepal PAN (9 digits)   # Even numbers stored as text when not used for calculation

print('Client:', client_name)
print('Audit Period:', audit_period)
print('PAN:', pan_number)
print('Type:', type(client_name))
```

    Client: Himalayan Tech Solutions Pvt. Ltd.
    Audit Period: Shrawan 2081 to Ashadh 2082 BS
    PAN: 123456789
    Type: <class 'str'>



```python
# bool — Boolean (True or False only)
# Very useful for status checks and decisions

is_audit_complete = True
is_tax_paid = False
is_listed_company = True

print('Audit complete?', is_audit_complete)
print('Tax paid?', is_tax_paid)
print('Listed company?', is_listed_company)
print('Type:', type(is_audit_complete))
```

    Audit complete? True
    Tax paid? False
    Listed company? True
    Type: <class 'bool'>



```python
# Real-world example: A client record with mixed data types
client_name = 'Ncell Pvt. Ltd.'       # str
client_id = 10045                      # int
revenue_crores = 146767.0             # float (Revenue in crores)
is_fortune500 = True                   # bool

print('--- Client Profile ---')
print('Name:', client_name)
print('ID:', client_id)
print('Revenue (NPR Crores):', revenue_crores)
print('Fortune 500 Company?', is_fortune500)
```

    --- Client Profile ---
    Name: Ncell Pvt. Ltd.
    ID: 10045
    Revenue (NPR Crores): 146767.0
    Fortune 500 Company? True


### ⚠️ Important: Numbers in quotes are NOT numbers!

This is a very common beginner mistake. Watch carefully:


```python
# This is a NUMBER (int)
amount1 = 50000
print(type(amount1))   # <class 'int'>

# This is TEXT (str) — the quotes make it text!
amount2 = '50000'
print(type(amount2))   # <class 'str'>

# What happens when you try to add them?
print(amount1 + amount1)   # 100000 — correct! (number + number)
print(amount2 + amount2)   # '5000050000' — joins text! (text + text)

# Lesson: Always store amounts as numbers (int or float), not as strings
```

    <class 'int'>
    <class 'str'>
    100000
    5000050000


## Section 5: Python as Your Financial Calculator

### Arithmetic Operators

Python handles all standard arithmetic — and then some:

| Operator | Operation | Example | Result |
|----------|-----------|---------|--------|
| `+` | Addition | `100 + 50` | `150` |
| `-` | Subtraction | `100 - 30` | `70` |
| `*` | Multiplication | `100 * 2` | `200` |
| `/` | Division | `100 / 4` | `25.0` |
| `//` | Floor Division (quotient only) | `100 // 3` | `33` |
| `%` | Modulo (remainder only) | `100 % 3` | `1` |
| `**` | Exponent (power) | `2 ** 10` | `1024` |

**Order of operations** is the same as in mathematics (BODMAS/PEMDAS).


```python
# Basic arithmetic
revenue = 2500000
cost_of_goods = 1600000
operating_expenses = 350000

gross_profit = revenue - cost_of_goods
print('Gross Profit:', gross_profit)

net_profit = gross_profit - operating_expenses
print('Net Profit:', net_profit)

gross_margin = (gross_profit / revenue) * 100
print('Gross Profit Margin:', gross_margin, '%')
```

    Gross Profit: 900000
    Net Profit: 550000
    Gross Profit Margin: 36.0 %



```python
# VAT Calculation (Nepal — single tax, no CGST/SGST split)
invoice_base_amount = 85000   # Base amount before VAT (NPR)
vat_rate = 13.0               # 13% VAT (Nepal standard rate per IRD)

vat_amount = invoice_base_amount * (vat_rate / 100)
invoice_total = invoice_base_amount + vat_amount

print('--- VAT Invoice Summary (Nepal) ---')
print('Base Amount:    NPR ', f'{invoice_base_amount:,}')
print('VAT @ 13%:      NPR ', f'{vat_amount:,}')
print('Invoice Total:  NPR ', f'{invoice_total:,}')
print()
print('Note: Nepal uses a single VAT rate (no CGST/SGST split like India)')
print('VAT Registration required for turnover > NPR 50 Lakhs per year (IRD)')

```

    --- VAT Invoice Summary (Nepal) ---
    Base Amount:    NPR  85,000
    VAT @ 13%:      NPR  11,050.0
    Invoice Total:  NPR  96,050.0
    
    Note: Nepal uses a single VAT rate (no CGST/SGST split like India)
    VAT Registration required for turnover > NPR 50 Lakhs per year (IRD)



```python
# Compound Interest Calculation
# Formula: A = P * (1 + r/n)^(n*t)

principal = 500000    # NPR 5,00,000 initial investment
annual_rate = 0.12   # 12% per annum
n = 4                 # Compounded quarterly (4 times a year)
years = 3             # Investment period

# ** is the power operator in Python (same as ^ in Excel/maths)
amount = principal * (1 + annual_rate / n) ** (n * years)

interest_earned = amount - principal

print('--- Fixed Deposit Summary ---')
print('Principal:        NPR ', principal)
print('Rate:             ', annual_rate * 100, '% per annum')
print('Period:           ', years, 'years')
print('Maturity Amount:  NPR ', round(amount, 2))
print('Interest Earned:  NPR ', round(interest_earned, 2))
```

    --- Fixed Deposit Summary ---
    Principal:        NPR  500000
    Rate:              12.0 % per annum
    Period:            3 years
    Maturity Amount:  NPR  712880.44
    Interest Earned:  NPR  212880.44



```python
# EMI Calculation
# Formula: EMI = [P * r * (1+r)^n] / [(1+r)^n - 1]

loan_amount = 2000000    # NPR 20,00,000 home loan
annual_rate = 8.5        # 8.5% per annum
loan_years = 20          # 20 years

monthly_rate = (annual_rate / 100) / 12   # Convert to monthly rate
n_months = loan_years * 12                 # Total number of months

emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** n_months) / ((1 + monthly_rate) ** n_months - 1)

total_payment = emi * n_months
total_interest = total_payment - loan_amount

print('--- Home Loan EMI Calculator ---')
print('Loan Amount:      NPR ', loan_amount)
print('Interest Rate:    ', annual_rate, '% per annum')
print('Loan Tenure:      ', loan_years, 'years')
print('Monthly EMI:      NPR ', round(emi, 2))
print('Total Payment:    NPR ', round(total_payment, 2))
print('Total Interest:   NPR ', round(total_interest, 2))
```

    --- Home Loan EMI Calculator ---
    Loan Amount:      NPR  2000000
    Interest Rate:     8.5 % per annum
    Loan Tenure:       20 years
    Monthly EMI:      NPR  17356.46
    Total Payment:    NPR  4165551.52
    Total Interest:   NPR  2165551.52


#### ✏️ Mini Exercise 3

A client has the following P&L data:
- Net Sales: NPR 45,00,000
- Cost of Goods Sold: NPR 28,00,000
- Administrative Expenses: NPR 4,50,000
- Selling Expenses: NPR 2,20,000
- Tax Rate: 25%

Calculate and print:
1. Gross Profit
2. Net Profit Before Tax
3. Tax Amount
4. Net Profit After Tax
5. Net Profit Margin (%)


```python
# Write your P&L calculator here



```

## Section 6: Making Decisions — if / elif / else

### Python can think!

In your work, you constantly make decisions based on conditions:
- *"If income exceeds NPR 10 lakh, apply the higher tax slab"*
- *"If debt-to-equity ratio is above 2, flag as high risk"*
- *"If the account balance is negative, send an alert"*

Python does this using `if / elif / else` statements.

**Structure:**
```python
if condition:
    # do this if condition is True
elif another_condition:
    # do this if the above is False but this is True
else:
    # do this if ALL above conditions are False
```

⚠️ **Indentation is critical in Python!** The code inside `if/elif/else` must be indented (4 spaces or 1 Tab). This is how Python knows which code belongs to which block.


```python
# Simple if/else — Checking if a company is profitable
net_profit = 250000

if net_profit > 0:
    print('Company is PROFITABLE')
    print('Profit amount: NPR ', net_profit)
else:
    print('Company is at a LOSS')
    print('Loss amount: NPR ', abs(net_profit))   # abs() gives absolute (positive) value

# Try changing net_profit to a negative number and re-run!
```

    Company is PROFITABLE
    Profit amount: NPR  250000



```python
# Comparison operators — used to create conditions
# >   greater than
# <   less than
# >=  greater than or equal to
# <=  less than or equal to
# ==  equal to (note: TWO equal signs!)
# !=  not equal to

revenue = 5000000
threshold = 4000000

print(revenue > threshold)    # True
print(revenue < threshold)    # False
print(revenue == threshold)   # False (not equal)
print(revenue != threshold)   # True (they are different)
```

    True
    False
    False
    True



```python
# Nepal Income Tax Slab Calculator (FY 2081-82 BS)
# Source: Inland Revenue Department (IRD), Nepal
taxable_income = 850000   # Change this to test different amounts (in NPR)

# Nepal individual income tax slabs (FY 2081-82)
# Slab 1: Up to NPR 5,00,000        → 1%
# Slab 2: NPR 5,00,001 to 7,00,000  → 10%
# Slab 3: NPR 7,00,001 to 20,00,000 → 20%
# Slab 4: Above NPR 20,00,000       → 30%

print('Taxable Income: NPR ', f'{taxable_income:,}')
print('-' * 45)

if taxable_income <= 500000:
    tax = taxable_income * 0.01
    slab = '1% slab (up to NPR 5 Lakh)'

elif taxable_income <= 700000:
    tax = (500000 * 0.01) + (taxable_income - 500000) * 0.10
    slab = '10% slab (NPR 5L to NPR 7L)'

elif taxable_income <= 2000000:
    tax = (500000 * 0.01) + (200000 * 0.10) + (taxable_income - 700000) * 0.20
    slab = '20% slab (NPR 7L to NPR 20L)'

else:
    tax = (500000 * 0.01) + (200000 * 0.10) + (1300000 * 0.20) + (taxable_income - 2000000) * 0.30
    slab = '30% slab (above NPR 20L)'

print('Applicable Slab:', slab)
print('Income Tax:     NPR ', f'{round(tax, 2):,}')
print('Net Income:     NPR ', f'{round(taxable_income - tax, 2):,}')
print()
print('Note: No cess/surcharge in Nepal. SSF contribution is separate.')

```

    Taxable Income: NPR  850,000
    ---------------------------------------------
    Applicable Slab: 20% slab (NPR 7L to NPR 20L)
    Income Tax:     NPR  55,000.0
    Net Income:     NPR  795,000.0
    
    Note: No cess/surcharge in Nepal. SSF contribution is separate.



```python
# Loan Eligibility Check — using 'and' / 'or' for multiple conditions
age = 35
annual_income = 720000     # NPR 7.2 lakhs
credit_score = 720
existing_emi = 8000        # Monthly existing EMI

# Monthly income
monthly_income = annual_income / 12

# EMI should not exceed 40% of monthly income (FOIR rule)
max_emi = monthly_income * 0.40

print('--- Loan Eligibility Assessment ---')
print('Monthly Income: NPR ', round(monthly_income, 2))
print('Max Allowable EMI (40%): NPR ', round(max_emi, 2))
print()

if age >= 21 and age <= 60 and credit_score >= 700 and existing_emi < max_emi:
    print('Result: ELIGIBLE for loan ✓')
elif credit_score < 700:
    print('Result: NOT ELIGIBLE — Low credit score')
elif existing_emi >= max_emi:
    print('Result: NOT ELIGIBLE — Existing EMI too high')
else:
    print('Result: NOT ELIGIBLE — Age criteria not met')
```

    --- Loan Eligibility Assessment ---
    Monthly Income: NPR  60000.0
    Max Allowable EMI (40%): NPR  24000.0
    
    Result: ELIGIBLE for loan ✓


#### ✏️ Mini Exercise 4

Write a program that checks a company's **Debt-to-Equity ratio** and classifies it:
- D/E < 1.0 → "Low Risk — Financially healthy"
- D/E between 1.0 and 2.0 → "Moderate Risk — Monitor closely"
- D/E > 2.0 → "High Risk — Caution advised"

Test it with: Total Debt = NPR 45,00,000, Total Equity = NPR 30,00,000


```python
# Write your D/E ratio checker here
total_debt = 4500000
total_equity = 3000000

# Calculate D/E ratio


# Add your if/elif/else here


```

## Section 7: Working with Text — Strings

### Strings are everywhere in finance

Client names, invoice descriptions, report headings, audit observations — all of these are **text (strings)** in Python.

A string is any text enclosed in **single** `'...'` or **double** `"..."` quotes.

You can do many useful things with strings:
- Combine them (concatenation)
- Convert case (upper, lower)
- Check if something is in the string
- Format them with variables (f-strings) ← the most useful one!


```python
# String basics
company = 'CloudNepal Pvt. Ltd.'
city = 'Kathmandu'

# String length — how many characters?
print('Company name length:', len(company))

# Convert case
print(company.upper())       # WIPRO LIMITED
print(company.lower())       # wipro limited

# Combine strings (concatenation) using +
full_description = company + ', ' + city
print(full_description)
```

    Company name length: 20
    CLOUDNEPAL PVT. LTD.
    cloudnepal pvt. ltd.
    CloudNepal Pvt. Ltd., Kathmandu



```python
# f-strings — The best way to create formatted text
# Put 'f' before the opening quote, then use {} to insert variable values

client_name = 'Unilever Nepal Ltd.'
audit_year = 2025
fee = 850000
audit_status = 'In Progress'

# Without f-string (old way — clunky)
message_old = 'Client: ' + client_name + ', Year: ' + str(audit_year)
print(message_old)

# With f-string (modern way — clean and readable)
message = f'Client: {client_name}, Year: {audit_year}'
print(message)

# You can even do calculations inside {}
print(f'Audit Fee: NPR {fee:,}')        # {:,} adds comma formatting
print(f'Status: {audit_status}')
print(f'Fee in Lakhs: NPR {fee/100000:.2f}L')  # :.2f means 2 decimal places
```

    Client: Unilever Nepal Ltd., Year: 2025
    Client: Unilever Nepal Ltd., Year: 2025
    Audit Fee: NPR 850,000
    Status: In Progress
    Fee in Lakhs: NPR 8.50L



```python
# Creating a formatted financial report header using f-strings
company_name = 'Bottlers Nepal Ltd.'
report_type = 'Statement of Profit and Loss'
period = 'Year ended 16th July 2025 (Ashadh 2082 BS)'
currency = 'NPR (NPR in Lakhs)'

# Using the * operator to repeat characters — useful for formatting
separator = '=' * 55

print(separator)
print(f'  {company_name}')
print(f'  {report_type}')
print(f'  {period}')
print(f'  All figures in: {currency}')
print(separator)
```

    =======================================================
      Bottlers Nepal Ltd.
      Statement of Profit and Loss
      Year ended 16th July 2025 (Ashadh 2082 BS)
      All figures in: NPR (NPR in Lakhs)
    =======================================================



```python
# Useful string methods for data cleaning (very common in practice!)

# Often, data imported from Excel/CSV has extra spaces or inconsistent case
messy_client_name = '  infosys limited  '  # Extra spaces
print('Before cleaning:', messy_client_name)

# .strip() removes leading and trailing spaces
clean_name = messy_client_name.strip()
print('After strip():', clean_name)

# .title() makes first letter of each word uppercase
formatted_name = clean_name.title()
print('After title():', formatted_name)

# .replace() — find and replace text
description = 'Sales Receipts - Cash - 2024'
updated = description.replace('Cash', 'Online')
print('Updated:', updated)

# Check if a string contains something
print('Contains 2024?', '2024' in description)   # True
print('Contains 2025?', '2025' in description)   # False
```

    Before cleaning:   infosys limited  
    After strip(): infosys limited
    After title(): Infosys Limited
    Updated: Sales Receipts - Online - 2024
    Contains 2024? True
    Contains 2025? False


## Section 8: Lists — Collections of Data

### From single values to collections

So far, we've stored **one value** in each variable:  
`revenue = 2500000`

But what if you have **multiple invoices**, **multiple clients**, or **12 months of data**?

That's where **Lists** come in. A list stores **multiple values** in a specific order.

Think of a list like a **column in Excel** — it holds many values, one below the other.

**Syntax:** `my_list = [value1, value2, value3, ...]`


```python
# Creating lists
monthly_revenue = [120000, 135000, 98000, 145000, 162000, 178000,
                   155000, 142000, 168000, 191000, 203000, 215000]

expense_categories = ['Salaries', 'Rent', 'Utilities', 'Marketing', 'Depreciation']

clients = ['NTC', 'Ncell', 'Fusemachines', 'InfoDevelopers', 'Deerwalk Services Pvt. Ltd.']

print('Monthly Revenue:', monthly_revenue)
print('Expense Categories:', expense_categories)
print('Clients:', clients)
print()
print('Number of months of data:', len(monthly_revenue))   # len() gives length
print('Number of clients:', len(clients))
```

    Monthly Revenue: [120000, 135000, 98000, 145000, 162000, 178000, 155000, 142000, 168000, 191000, 203000, 215000]
    Expense Categories: ['Salaries', 'Rent', 'Utilities', 'Marketing', 'Depreciation']
    Clients: ['NTC', 'Ncell', 'Fusemachines', 'InfoDevelopers', 'Deerwalk Services Pvt. Ltd.']
    
    Number of months of data: 12
    Number of clients: 5



```python
# Accessing items in a list — indexing
# IMPORTANT: Python counts from 0, not 1!
# Index:   0       1      2      3       4
clients = ['NTC', 'Ncell', 'Fusemachines', 'InfoDevelopers', 'Deerwalk Services Pvt. Ltd.']

print('First client:', clients[0])    # TCS
print('Second client:', clients[1])   # Ncell
print('Last client:', clients[-1])    # -1 always gives the last item!
print('Second last:', clients[-2])

# Slicing — getting a range of items [start:end] (end is NOT included)
print('First three clients:', clients[0:3])   # Ncell, NTC, Fusemachines
print('Last two clients:', clients[-2:])
```

    First client: NTC
    Second client: Ncell
    Last client: Deerwalk Services Pvt. Ltd.
    Second last: InfoDevelopers
    First three clients: ['NTC', 'Ncell', 'Fusemachines']
    Last two clients: ['InfoDevelopers', 'Deerwalk Services Pvt. Ltd.']



```python
# Useful list operations for financial data
monthly_revenue = [120000, 135000, 98000, 145000, 162000, 178000,
                   155000, 142000, 168000, 191000, 203000, 215000]

print('--- Revenue Analysis ---')
print('Total Annual Revenue: NPR ', sum(monthly_revenue))     # sum() adds all values
print('Highest Month:        NPR ', max(monthly_revenue))     # max() finds highest
print('Lowest Month:         NPR ', min(monthly_revenue))     # min() finds lowest
print('Average Monthly:      NPR ', sum(monthly_revenue) / len(monthly_revenue))
print()

# Adding items to a list
clients = ['NTC', 'Ncell', 'Fusemachines']
clients.append('Accenture')    # Add to the end
print('Updated clients:', clients)

# Sorting
invoices = [45000, 12000, 78000, 34000, 91000, 23000]
invoices.sort()                # Sort in ascending order
print('Sorted invoices:', invoices)
invoices.sort(reverse=True)    # Sort in descending order
print('Descending order:', invoices)
```

    --- Revenue Analysis ---
    Total Annual Revenue: NPR  1912000
    Highest Month:        NPR  215000
    Lowest Month:         NPR  98000
    Average Monthly:      NPR  159333.33333333334
    
    Updated clients: ['NTC', 'Ncell', 'Fusemachines', 'Accenture']
    Sorted invoices: [12000, 23000, 34000, 45000, 78000, 91000]
    Descending order: [91000, 78000, 45000, 34000, 23000, 12000]


## Section 9: Dictionaries — Organized Data Records

### From lists to labelled data

A **List** stores values by position (index 0, 1, 2...).

But sometimes you want to label your data — like a **ledger entry** where each piece of information has a name.

A **Dictionary** stores data as **key-value pairs** — just like a real dictionary where each word (key) has a meaning (value).

```
Think of it like a mini spreadsheet row:
Column name  →  Value
'name'       →  'NTC'
'revenue'    →  2200000
'sector'     →  'IT'
```

**Syntax:** `my_dict = {'key1': value1, 'key2': value2}`


```python
# A dictionary — like a client record
client = {
    'name': 'Nepal Telecom (NTC)',
    'pan': '123456789',  # Nepal PAN — 9-digit numeric (IRD registration)
    'sector': 'Information Technology',
    'annual_revenue': 220000000000,   # NPR 2.2 lakh crores
    'employees': 614000,
    'is_listed': True
}

# Accessing values using the key (like looking up a column name)
print('Client Name:', client['name'])
print('PAN:', client['pan'])
print('Sector:', client['sector'])
print('Listed?', client['is_listed'])
```

    Client Name: Nepal Telecom (NTC)
    PAN: 123456789
    Sector: Information Technology
    Listed? True



```python
# Adding, updating, and removing from a dictionary
invoice = {
    'invoice_no': 'INV-2025-001',
    'client': 'ABC Pvt Ltd',
    'date': '15-Apr-2025',
    'amount': 250000,
    'vat_rate': 18
}

# Add a new key-value pair
invoice['vat_amount'] = invoice['amount'] * invoice['vat_rate'] / 100
invoice['total'] = invoice['amount'] + invoice['vat_amount']

# Update an existing value
invoice['status'] = 'Paid'

# Print all key-value pairs
print('--- Invoice Details ---')
for key, value in invoice.items():
    print(f'{key:15}: {value}')
```

    --- Invoice Details ---
    invoice_no     : INV-2025-001
    client         : ABC Pvt Ltd
    date           : 15-Apr-2025
    amount         : 250000
    vat_rate       : 18
    vat_amount     : 45000.0
    total          : 295000.0
    status         : Paid



```python
# List of dictionaries — like a table in Excel
# Each dictionary is one row, the keys are column names

transactions = [
    {'date': '01-Apr-2025', 'description': 'Sales Revenue',    'debit': 0,      'credit': 500000},
    {'date': '03-Apr-2025', 'description': 'Office Rent',      'debit': 45000,  'credit': 0},
    {'date': '05-Apr-2025', 'description': 'Sales Revenue',    'debit': 0,      'credit': 320000},
    {'date': '10-Apr-2025', 'description': 'Salaries Paid',    'debit': 180000, 'credit': 0},
    {'date': '15-Apr-2025', 'description': 'Utility Bill',     'debit': 12000,  'credit': 0},
]

print('--- Transaction Ledger ---')
print(f'{"Date":<15} {"Description":<20} {"Debit":>12} {"Credit":>12}')
print('-' * 62)
for txn in transactions:
    debit_str  = f"NPR {txn['debit']:>10,}" if txn['debit'] > 0 else ''
    credit_str = f"NPR {txn['credit']:>10,}" if txn['credit'] > 0 else ''
    print(f"{txn['date']:<15} {txn['description']:<20} {debit_str:>12} {credit_str:>12}")
```

    --- Transaction Ledger ---
    Date            Description                 Debit       Credit
    --------------------------------------------------------------
    01-Apr-2025     Sales Revenue                     NPR    500,000
    03-Apr-2025     Office Rent          NPR     45,000             
    05-Apr-2025     Sales Revenue                     NPR    320,000
    10-Apr-2025     Salaries Paid        NPR    180,000             
    15-Apr-2025     Utility Bill         NPR     12,000             


## Section 10: Loops — Automating Repetitive Work

### Stop repeating yourself!

Imagine you need to calculate GST on 100 invoices.  
Writing 100 separate `print()` statements is clearly not the answer.

**Loops** let you repeat an action multiple times automatically.

### The `for` loop

Use `for` when you want to go through a **collection** (list, etc.) one item at a time.

```python
for item in collection:
    # do something with item
```

Think of it as: *"For each invoice in my invoice list, calculate the GST"*


```python
# Simple for loop — going through a list
clients = ['NTC', 'Ncell', 'Fusemachines', 'InfoDevelopers', 'Deerwalk Services Pvt. Ltd.']

print('--- Client List ---')
for client in clients:
    print('Client:', client)
```

    --- Client List ---
    Client: NTC
    Client: Ncell
    Client: Fusemachines
    Client: InfoDevelopers
    Client: Deerwalk Services Pvt. Ltd.



```python
# Batch GST calculation on multiple invoices
invoice_amounts = [85000, 42000, 125000, 67500, 98000, 33000]
vat_rate = 13.0

total_gst_collected = 0   # We'll accumulate GST here

print(f"{'Invoice Amount':>17} | {'GST (13%)':>12} | {'Total Amount':>14}")
print('-' * 50)

for amount in invoice_amounts:
    gst = amount * vat_rate / 100
    total = amount + gst
    total_gst_collected += gst   # Same as: total_gst_collected = total_gst_collected + gst
    print(f'NPR {amount:>15,} | NPR {gst:>11,.2f} | NPR {total:>12,.2f}')

print('-' * 50)
print(f'Total GST Liability: NPR {total_gst_collected:,.2f}')
```

       Invoice Amount |    GST (13%) |   Total Amount
    --------------------------------------------------
    NPR          85,000 | NPR   11,050.00 | NPR    96,050.00
    NPR          42,000 | NPR    5,460.00 | NPR    47,460.00
    NPR         125,000 | NPR   16,250.00 | NPR   141,250.00
    NPR          67,500 | NPR    8,775.00 | NPR    76,275.00
    NPR          98,000 | NPR   12,740.00 | NPR   110,740.00
    NPR          33,000 | NPR    4,290.00 | NPR    37,290.00
    --------------------------------------------------
    Total GST Liability: NPR 58,565.00



```python
# range() — loop a specific number of times
# Useful when you don't have a list but know how many times to repeat

print('Quarterly Revenue Projections (10% growth each year):')
base_revenue = 1000000   # NPR 10 lakhs starting revenue
growth_rate = 0.10

for year in range(1, 6):   # range(1, 6) gives: 1, 2, 3, 4, 5
    projected = base_revenue * (1 + growth_rate) ** year
    print(f'Year {year}: NPR {projected:>12,.2f}')
```

    Quarterly Revenue Projections (10% growth each year):
    Year 1: NPR 1,100,000.00
    Year 2: NPR 1,210,000.00
    Year 3: NPR 1,331,000.00
    Year 4: NPR 1,464,100.00
    Year 5: NPR 1,610,510.00



```python
# while loop — keeps going as long as a condition is True
# Use when you don't know HOW MANY times to repeat

# How many years to double your investment at 8% per annum? (Rule of 72)
investment = 100000   # Starting amount
target = 200000       # Double the investment
rate = 0.08           # 8% annual return
year = 0

print('Investment Growth at 8% p.a.:')
while investment < target:
    investment = investment * (1 + rate)   # Grow by 8%
    year += 1   # Count the year
    print(f'Year {year}: NPR {investment:>12,.2f}')

print(f'\nYour investment doubled in {year} years!')
print(f'(Rule of 72 predicts: {round(72/8)} years)')
```

    Investment Growth at 8% p.a.:
    Year 1: NPR   108,000.00
    Year 2: NPR   116,640.00
    Year 3: NPR   125,971.20
    Year 4: NPR   136,048.90
    Year 5: NPR   146,932.81
    Year 6: NPR   158,687.43
    Year 7: NPR   171,382.43
    Year 8: NPR   185,093.02
    Year 9: NPR   199,900.46
    Year 10: NPR   215,892.50
    
    Your investment doubled in 10 years!
    (Rule of 72 predicts: 9 years)


#### ✏️ Mini Exercise 5

You have a list of 6 employees with their annual salaries:
```
salaries = [480000, 720000, 960000, 1200000, 1440000, 2400000]
```

Using a `for` loop, calculate and print for each employee:
1. Professional Tax (PT): NPR 200/month if salary ≤ NPR 10L, else NPR 2,500/year (Maharashtra slab — simplified)
2. Provident Fund (EPF @ 10% (employee) of salary (capped at salary of NPR 1,80,000)
3. Net take-home salary

*Hint: PF is calculated on salary capped at NPR 1,80,000*


```python
salaries = [480000, 720000, 960000, 1200000, 1440000, 2400000]

# Write your loop here


```

## Section 11: Functions — Write Once, Use Many Times

### What is a function?

Think about the **VLOOKUP formula** in Excel. You write the formula **once**, give it inputs, and it returns an output. You don't need to re-write the logic each time.

A **function** in Python works exactly the same way:
- You **define** it once (write the logic)
- You **call** it many times with different inputs
- It **returns** the result

```python
def function_name(input1, input2):
    # Do something with the inputs
    result = input1 + input2
    return result      # Send the answer back
```

This eliminates repetition and makes your code **reliable** — fix a bug in one place, it's fixed everywhere.


```python
# Defining a simple function
def calculate_gst(base_amount, rate=18):
    """
    Calculates GST on a given amount.
    base_amount: The pre-GST invoice amount
    rate: GST rate in % (default is 13%)
    Returns: (vat_amount, total_amount)
    """
    vat_amount = base_amount * rate / 100
    total_amount = base_amount + vat_amount
    return vat_amount, total_amount

# Calling the function — use it like Excel's VLOOKUP
gst, total = calculate_gst(85000)         # Uses default 13%
print(f'GST: NPR {gst:,}  |  Total: NPR {total:,}')

gst, total = calculate_gst(50000, 5)      # 5% GST
print(f'GST: NPR {gst:,}  |  Total: NPR {total:,}')

gst, total = calculate_gst(200000, 28)    # 28% GST
print(f'GST: NPR {gst:,}  |  Total: NPR {total:,}')
```

    GST: NPR 15,300.0  |  Total: NPR 100,300.0
    GST: NPR 2,500.0  |  Total: NPR 52,500.0
    GST: NPR 56,000.0  |  Total: NPR 256,000.0



```python
# Nepal Income Tax Calculator (FY 2081-82 BS)
# IRD-compliant individual income tax rates

def calculate_nepal_income_tax(taxable_income, status='individual'):
    """
    Calculate Nepal income tax per IRD slabs (FY 2081-82 BS).
    status: 'individual' (single) or 'couple' (additional NPR 1L exemption)
    """
    extra_exemption = 100000 if status == 'couple' else 0
    adjusted = max(taxable_income - extra_exemption, 0)

    # Nepal progressive slab
    if adjusted <= 500000:
        tax = adjusted * 0.01
    elif adjusted <= 700000:
        tax = 5000 + (adjusted - 500000) * 0.10
    elif adjusted <= 2000000:
        tax = 5000 + 20000 + (adjusted - 700000) * 0.20
    else:
        tax = 5000 + 20000 + 260000 + (adjusted - 2000000) * 0.30

    # Karmachari Sanchaya Kosh (EPF) is separate — not income tax
    return round(tax, 2)


# Test the function
income = 1200000

tax_individual = calculate_nepal_income_tax(income, 'individual')
tax_couple     = calculate_nepal_income_tax(income, 'couple')

print(f'Taxable Income:  NPR {income:,}')
print()
print(f"{'Particulars':<28} {'Individual':>12} {'Couple':>12}")
print('-' * 55)
print(f"{'Income Tax':<28} NPR {tax_individual:>9,} NPR {tax_couple:>9,}")
print(f"{'Effective Rate':<28} {tax_individual/income*100:>11.2f}% {tax_couple/income*100:>10.2f}%")
print(f"{'Net Take-home':<28} NPR {income-tax_individual:>9,} NPR {income-tax_couple:>9,}")
print()
print(f'Couple gets NPR {tax_individual - tax_couple:,} tax saving (NPR 1L extra exemption at 20% bracket)')
print()
print('Source: Inland Revenue Department (IRD), Nepal — FY 2081-82 BS')

```

    Taxable Income:  NPR 1,200,000
    
    Particulars                    Individual       Couple
    -------------------------------------------------------
    Income Tax                   NPR 125,000.0 NPR 105,000.0
    Effective Rate                     10.42%       8.75%
    Net Take-home                NPR 1,075,000.0 NPR 1,095,000.0
    
    Couple gets NPR 20,000.0 tax saving (NPR 1L extra exemption at 20% bracket)
    
    Source: Inland Revenue Department (IRD), Nepal — FY 2081-82 BS



```python
# Financial Ratios Calculator — all ratios in one place
def financial_ratios(revenue, gross_profit, net_profit, current_assets,
                     current_liabilities, total_debt, total_equity):
    """Calculate key financial ratios and return a summary."""

    gross_margin    = (gross_profit / revenue) * 100
    net_margin      = (net_profit / revenue) * 100
    current_ratio   = current_assets / current_liabilities
    de_ratio        = total_debt / total_equity
    roe             = (net_profit / total_equity) * 100

    print('--- Financial Ratios Analysis ---')
    print(f'Gross Profit Margin : {gross_margin:.2f}%')
    print(f'Net Profit Margin   : {net_margin:.2f}%')
    print(f'Current Ratio       : {current_ratio:.2f}x')
    print(f'Debt-to-Equity      : {de_ratio:.2f}x')
    print(f'Return on Equity    : {roe:.2f}%')

    # Quick health check
    print()
    print('Quick Assessment:')
    print(' Liquidity:', 'Good ✓' if current_ratio >= 1.5 else 'Monitor ⚠')
    print(' Leverage :', 'Safe ✓' if de_ratio <= 2.0 else 'High Risk ✗')
    print(' Profit   :', 'Good ✓' if net_margin >= 10 else 'Low ⚠')


# Call the function with sample data
financial_ratios(
    revenue            = 5000000,
    gross_profit       = 1800000,
    net_profit         = 620000,
    current_assets     = 2200000,
    current_liabilities= 1100000,
    total_debt         = 1800000,
    total_equity       = 2500000
)
```

    --- Financial Ratios Analysis ---
    Gross Profit Margin : 36.00%
    Net Profit Margin   : 12.40%
    Current Ratio       : 2.00x
    Debt-to-Equity      : 0.72x
    Return on Equity    : 24.80%
    
    Quick Assessment:
     Liquidity: Good ✓
     Leverage : Safe ✓
     Profit   : Good ✓


#### ✏️ Mini Exercise 6

Write a function called `depreciation_schedule` that:
- Takes: `asset_name`, `cost`, `salvage_value`, `useful_life` (in years) as inputs
- Calculates annual depreciation using the **Straight Line Method (SLM)**
- Prints a year-wise schedule showing: Year, Depreciation, Accumulated Depreciation, Book Value

Test with: Computer equipment, Cost = NPR 1,50,000, Salvage = NPR 10,000, Useful Life = 5 years


```python
# Write your depreciation_schedule function here



# Call your function
# depreciation_schedule('Computer Equipment', 150000, 10000, 5)

```

## Section 12: Putting It All Together

Let's combine everything we've learned to build a **mini financial report generator**.


```python
# Mini Financial Report Generator
# Uses: variables, data types, lists, dicts, loops, functions, f-strings, conditionals

def generate_pl_report(company_info, pl_data):
    """Generates a simple Profit & Loss statement."""

    separator = '=' * 55
    thin_line = '-' * 55

    # Header
    print(separator)
    print(f"  {company_info['name']}")
    print(f"  Statement of Profit & Loss")
    print(f"  For the year ended {company_info['year_end']}")
    print(f"  (All amounts in NPR )")
    print(separator)

    # Revenue section
    total_revenue = sum(pl_data['revenue'].values())
    print(f"\n  {'I. REVENUE':}")  
    for item, amount in pl_data['revenue'].items():
        print(f"     {item:<35} {amount:>12,}")
    print(thin_line)
    print(f"     {'Total Revenue':<35} {total_revenue:>12,}")

    # Expenses section
    total_expenses = sum(pl_data['expenses'].values())
    print(f"\n  {'II. EXPENEPSES'}")  
    for item, amount in pl_data['expenses'].items():
        print(f"     {item:<35} {amount:>12,}")
    print(thin_line)
    print(f"     {'Total Expenses':<35} {total_expenses:>12,}")

    # Profit calculations
    pbt = total_revenue - total_expenses
    tax = pbt * company_info['tax_rate'] if pbt > 0 else 0
    pat = pbt - tax

    print(f"\n{separator}")
    print(f"  {'Profit Before Tax':<38} {pbt:>12,}")
    print(f"  {'Tax @ {:.0f}%'.format(company_info['tax_rate']*100):<38} {round(tax):>12,}")
    print(separator)
    print(f"  {'PROFIT AFTER TAX':<38} {round(pat):>12,}")
    print(separator)

    # Ratios
    print(f"\n  Key Ratios:")
    print(f"  Net Profit Margin : {pat/total_revenue*100:.2f}%")
    print(f"  Tax Efficiency    : {pat/pbt*100:.2f}%" if pbt > 0 else '')
    status = 'Profitable ✓' if pat > 0 else 'Loss Making ✗'
    print(f"  Financial Status  : {status}")


# ---- Data ----
company_info = {
    'name': 'Sunrise Manufacturing Pvt. Ltd.',
    'year_end': '16th July 2025 (Ashadh 2082 BS)',
    'tax_rate': 0.25
}

pl_data = {
    'revenue': {
        'Revenue from Operations': 8500000,
        'Other Income':             125000,
    },
    'expenses': {
        'Cost of Materials':       4200000,
        'Employee Benefits':       1250000,
        'Finance Costs':            185000,
        'Depreciation':             320000,
        'Other Expenses':           480000,
    }
}

generate_pl_report(company_info, pl_data)
```

    =======================================================
      Sunrise Manufacturing Pvt. Ltd.
      Statement of Profit & Loss
      For the year ended 16th July 2025 (Ashadh 2082 BS)
      (All amounts in NPR )
    =======================================================
    
      I. REVENUE
         Revenue from Operations                8,500,000
         Other Income                             125,000
    -------------------------------------------------------
         Total Revenue                          8,625,000
    
      II. EXPENEPSES
         Cost of Materials                      4,200,000
         Employee Benefits                      1,250,000
         Finance Costs                            185,000
         Depreciation                             320,000
         Other Expenses                           480,000
    -------------------------------------------------------
         Total Expenses                         6,435,000
    
    =======================================================
      Profit Before Tax                         2,190,000
      Tax @ 25%                                   547,500
    =======================================================
      PROFIT AFTER TAX                          1,642,500
    =======================================================
    
      Key Ratios:
      Net Profit Margin : 19.04%
      Tax Efficiency    : 75.00%
      Financial Status  : Profitable ✓


## Section 13: Practice Exercises

Now it's your turn! These exercises will test everything you've learned.

---

#### 🏋️ Exercise 1 — Working Capital Analysis

A company has the following current assets and liabilities:

**Current Assets:** Cash NPR 85,000 | Debtors NPR 3,20,000 | Inventory NPR 4,75,000 | Prepaid Expenses NPR 25,000  
**Current Liabilities:** Creditors NPR 2,80,000 | Short-term Loans NPR 1,50,000 | Accrued Expenses NPR 45,000

Write a program using **lists or dictionaries** to:
1. Calculate Total Current Assets
2. Calculate Total Current Liabilities
3. Calculate Working Capital (CA - CL)
4. Calculate Current Ratio (CA / CL)
5. Calculate Quick Ratio ((CA - Inventory) / CL)
6. Print a formatted summary with assessment (ratios below 1 = warning)


```python
# Exercise 1 — Working Capital Analysis
# Tip: Use a dictionary for assets and liabilities, then loop through them



```

#### 🏋️ Exercise 2 — Ageing Analysis of Debtors

You have the following list of outstanding invoices with their ages (days overdue):

```python
invoices = [
    {'client': 'Alpha Ltd',   'amount': 125000, 'days': 25},
    {'client': 'Beta Corp',   'amount': 85000,  'days': 65},
    {'client': 'Gamma Inc',   'amount': 210000, 'days': 45},
    {'client': 'Delta Pvt',   'amount': 55000,  'days': 95},
    {'client': 'Epsilon Ltd', 'amount': 175000, 'days': 15},
    {'client': 'Zeta Co',     'amount': 92000,  'days': 130},
]
```

Using a `for` loop, classify each invoice into:
- 0–30 days → "Current"
- 31–60 days → "1–2 Months"
- 61–90 days → "2–3 Months"
- 90+ days → "Overdue >3 Months" (flag as high risk)

Print the ageing report and the total outstanding amount in each bucket.


```python
# Exercise 2 — Debtors Ageing Analysis
invoices = [
    {'client': 'Alpha Ltd',   'amount': 125000, 'days': 25},
    {'client': 'Beta Corp',   'amount': 85000,  'days': 65},
    {'client': 'Gamma Inc',   'amount': 210000, 'days': 45},
    {'client': 'Delta Pvt',   'amount': 55000,  'days': 95},
    {'client': 'Epsilon Ltd', 'amount': 175000, 'days': 15},
    {'client': 'Zeta Co',     'amount': 92000,  'days': 130},
]

# Write your ageing analysis here


```

#### 🏋️ Exercise 3 — Housing Allowance Exemption Calculator

Professional/Education Deduction (under old regime) is the **minimum** of three amounts:
1. Actual Housing Allowance received from employer
2. 50% of Basic Salary (metro city) or 40% (outside Kathmandu Valley)
3. Actual Rent Paid **minus** 10% of Basic Salary

Write a **function** called `calculate_hra_exemption` that takes:
- `basic_salary` (annual)
- `hra_received` (annual)
- `rent_paid` (annual)
- `is_metro` (True/False)

And returns the Professional/Education Deduction amount.

Test with:
- Basic Salary: NPR 6,00,000 | Housing Allowance Received: NPR 2,40,000 | Rent Paid: NPR 2,16,000 | Metro: Yes
- Basic Salary: NPR 4,80,000 | Housing Allowance Received: NPR 1,44,000 | Rent Paid: NPR 1,80,000 | Metro: No


```python
# Exercise 3 — Housing Allowance Exemption Calculator
# Tip: Use the min() function to find the minimum of three values



```

---
### 💡 Solutions

Try the exercises on your own first! Run the cells below **only after you've attempted them.**


```python
# SOLUTION — Exercise 1: Working Capital Analysis

current_assets = {
    'Cash':              85000,
    'Debtors':          320000,
    'Inventory':        475000,
    'Prepaid Expenses':  25000,
}

current_liabilities = {
    'Creditors':        280000,
    'Short-term Loans': 150000,
    'Accrued Expenses':  45000,
}

total_ca = sum(current_assets.values())
total_cl = sum(current_liabilities.values())
working_capital = total_ca - total_cl
current_ratio = total_ca / total_cl
quick_ratio = (total_ca - current_assets['Inventory']) / total_cl

print('=== Working Capital Analysis ===')
print('\nCurrent Assets:')
for item, amt in current_assets.items():
    print(f'  {item:<25} NPR {amt:>10,}')
print(f'  {"Total Current Assets":<25} NPR {total_ca:>10,}')

print('\nCurrent Liabilities:')
for item, amt in current_liabilities.items():
    print(f'  {item:<25} NPR {amt:>10,}')
print(f'  {"Total Current Liab.":<25} NPR {total_cl:>10,}')

print(f'\nWorking Capital:  NPR {working_capital:,}')
print(f'Current Ratio:    {current_ratio:.2f}x', '✓' if current_ratio >= 1.5 else '⚠ Below ideal')
print(f'Quick Ratio:      {quick_ratio:.2f}x', '✓' if quick_ratio >= 1.0 else '⚠ Below ideal')
```

    === Working Capital Analysis ===
    
    Current Assets:
      Cash                      NPR     85,000
      Debtors                   NPR    320,000
      Inventory                 NPR    475,000
      Prepaid Expenses          NPR     25,000
      Total Current Assets      NPR    905,000
    
    Current Liabilities:
      Creditors                 NPR    280,000
      Short-term Loans          NPR    150,000
      Accrued Expenses          NPR     45,000
      Total Current Liab.       NPR    475,000
    
    Working Capital:  NPR 430,000
    Current Ratio:    1.91x ✓
    Quick Ratio:      0.91x ⚠ Below ideal



```python
# SOLUTION — Exercise 2: Debtors Ageing Analysis

invoices = [
    {'client': 'Alpha Ltd',   'amount': 125000, 'days': 25},
    {'client': 'Beta Corp',   'amount': 85000,  'days': 65},
    {'client': 'Gamma Inc',   'amount': 210000, 'days': 45},
    {'client': 'Delta Pvt',   'amount': 55000,  'days': 95},
    {'client': 'Epsilon Ltd', 'amount': 175000, 'days': 15},
    {'client': 'Zeta Co',     'amount': 92000,  'days': 130},
]

buckets = {
    'Current (0-30 days)':        0,
    '1-2 Months (31-60 days)':    0,
    '2-3 Months (61-90 days)':    0,
    'Overdue >3 Months (91+ days)': 0
}

print(f"{'Client':<15} {'Amount':>12} {'Days':>6} {'Category':<30}")
print('-' * 68)

for inv in invoices:
    if inv['days'] <= 30:
        category = 'Current (0-30 days)'
        flag = ''
    elif inv['days'] <= 60:
        category = '1-2 Months (31-60 days)'
        flag = ''
    elif inv['days'] <= 90:
        category = '2-3 Months (61-90 days)'
        flag = '⚠'
    else:
        category = 'Overdue >3 Months (91+ days)'
        flag = '🔴 HIGH RISK'

    buckets[category] += inv['amount']
    print(f"{inv['client']:<15} NPR {inv['amount']:>11,} {inv['days']:>5}d  {category} {flag}")

print('\n=== Ageing Summary ===')
total = 0
for category, amount in buckets.items():
    print(f'{category:<35} NPR {amount:>10,}')
    total += amount
print(f'{"TOTAL OUTSTANDING":<35} NPR {total:>10,}')
```

    Client                Amount   Days Category                      
    --------------------------------------------------------------------
    Alpha Ltd       NPR     125,000    25d  Current (0-30 days) 
    Beta Corp       NPR      85,000    65d  2-3 Months (61-90 days) ⚠
    Gamma Inc       NPR     210,000    45d  1-2 Months (31-60 days) 
    Delta Pvt       NPR      55,000    95d  Overdue >3 Months (91+ days) 🔴 HIGH RISK
    Epsilon Ltd     NPR     175,000    15d  Current (0-30 days) 
    Zeta Co         NPR      92,000   130d  Overdue >3 Months (91+ days) 🔴 HIGH RISK
    
    === Ageing Summary ===
    Current (0-30 days)                 NPR    300,000
    1-2 Months (31-60 days)             NPR    210,000
    2-3 Months (61-90 days)             NPR     85,000
    Overdue >3 Months (91+ days)        NPR    147,000
    TOTAL OUTSTANDING                   NPR    742,000



```python
# SOLUTION — Exercise 3: Housing Allowance Exemption Calculator

def calculate_hra_exemption(basic_salary, hra_received, rent_paid, is_metro):
    """Calculate Professional/Education Deduction under Income Tax (Nepal Income Tax)."""

    # Method 1: Actual Housing Allowance received
    limit1 = hra_received

    # Method 2: 50% of Basic (metro) or 40% (outside Kathmandu Valley)
    limit2 = basic_salary * 0.50 if is_metro else basic_salary * 0.40

    # Method 3: Rent paid minus 10% of Basic
    limit3 = max(0, rent_paid - basic_salary * 0.10)   # Cannot be negative

    # Exemption = minimum of all three
    exemption = min(limit1, limit2, limit3)

    city_type = 'Metro' if is_metro else 'Non-Metro'
    print(f'--- Housing Allowance Exemption Calculation ({city_type}) ---')
    print(f'Basic Salary:           NPR {basic_salary:>10,}')
    print(f'Housing Allowance Received:           NPR {hra_received:>10,}')
    print(f'Rent Paid:              NPR {rent_paid:>10,}')
    print()
    print(f'Limit 1 (Actual Housing Allowance):   NPR {limit1:>10,}')
    print(f'Limit 2 (% of Basic):   NPR {limit2:>10,}')
    print(f'Limit 3 (Rent - 10%B):  NPR {limit3:>10,}')
    print(f'Housing Allowance Exemption (min):    NPR {exemption:>10,}')
    print(f'Housing Allowance Taxable:            NPR {hra_received - exemption:>10,}')
    print()
    return exemption


# Test Case 1
calculate_hra_exemption(600000, 240000, 216000, True)

# Test Case 2
calculate_hra_exemption(480000, 144000, 180000, False)
```

    --- Housing Allowance Exemption Calculation (Metro) ---
    Basic Salary:           NPR    600,000
    Housing Allowance Received:           NPR    240,000
    Rent Paid:              NPR    216,000
    
    Limit 1 (Actual Housing Allowance):   NPR    240,000
    Limit 2 (% of Basic):   NPR  300,000.0
    Limit 3 (Rent - 10%B):  NPR  156,000.0
    Housing Allowance Exemption (min):    NPR  156,000.0
    Housing Allowance Taxable:            NPR   84,000.0
    
    --- Housing Allowance Exemption Calculation (Non-Metro) ---
    Basic Salary:           NPR    480,000
    Housing Allowance Received:           NPR    144,000
    Rent Paid:              NPR    180,000
    
    Limit 1 (Actual Housing Allowance):   NPR    144,000
    Limit 2 (% of Basic):   NPR  192,000.0
    Limit 3 (Rent - 10%B):  NPR  132,000.0
    Housing Allowance Exemption (min):    NPR  132,000.0
    Housing Allowance Taxable:            NPR   12,000.0
    





    132000.0



---

## 🎉 Congratulations!

You have completed the **Python for CA Professionals** introductory notebook.

### What you've learned today

| Concept | What you can do now |
|---------|--------------------|
| `print()` & comments | Display output, document your code |
| Variables | Store and reuse financial data |
| Data Types | Work with numbers, text, and True/False |
| Arithmetic | Build calculators (GST, EMI, compound interest) |
| `if/elif/else` | Automate decisions (tax slabs, risk classification) |
| Strings & f-strings | Generate formatted financial reports |
| Lists | Manage collections of invoices, clients, transactions |
| Dictionaries | Create structured records like ledger entries |
| Loops | Process hundreds of transactions automatically |
| Functions | Build reusable tools (tax calculator, ratios) |

### What's Next?

You're ready for the next module:

1. **pandas** — Work with Excel files, large datasets, and financial data
2. **matplotlib / seaborn** — Create charts and visualisations
3. **openpyxl** — Read and write Excel files with Python
4. **NumPy** — Advanced financial mathematics
5. **Automation** — Schedule and automate reports

---

> **Remember:** Every expert was once a beginner.  
> The best way to learn Python is to **experiment** — change the numbers, break things, fix them.  
> Your CA training has already given you the analytical mindset. Python is just the tool.

---
*Python for CA Professionals — Module 1: Python Basics*




