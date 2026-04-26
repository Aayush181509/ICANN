# Foundation 1: NumPy — From Zero to Confident
### Data Science for Chartered Accountants — Pre-Module

---

## What is this notebook about?

Before we process financial data, we need to understand **NumPy** — the core numerical engine of Python data science.

This notebook assumes:
- ✅ You know basic Python (variables, loops, lists)
- ❌ No prior knowledge of NumPy required

## What will you learn?
1. Why NumPy exists — the problem with plain Python lists
2. Creating NumPy arrays
3. Array attributes and data types
4. Indexing and slicing
5. Arithmetic and broadcasting
6. Useful built-in functions
7. Boolean filtering
8. 2D arrays (matrices)
9. Reshaping arrays
10. Bridge to accounting use-cases

---

> **Think of NumPy as a supercharged Excel column.** Instead of clicking cells one by one, you operate on the entire column at once — instantly.

---
## Section 1: Why NumPy? The Problem with Python Lists


```python
# ── Python list approach ──────────────────────────────────────────────────────
# Suppose we have monthly sales figures (₹ in thousands)
sales_list = [120, 135, 98, 145, 160, 112, 178, 155, 190, 142, 165, 200]

# Problem 1: Can't do math directly on a list
# sales_list * 1.18   →  this REPEATS the list 1.18 times... which is an error!

# To add 18% GST, you'd have to loop:
sales_with_gst = []
for s in sales_list:
    sales_with_gst.append(s * 1.18)

print('With loop:', sales_with_gst[:4], '...')
print('This works, but imagine doing this for 50,000 invoices!')
```


```python
# ── NumPy approach ────────────────────────────────────────────────────────────
import numpy as np

sales_array = np.array([120, 135, 98, 145, 160, 112, 178, 155, 190, 142, 165, 200])

# Add 18% GST — one line, no loop needed!
sales_with_gst_np = sales_array * 1.18

print('NumPy result:', sales_with_gst_np)
print('\nType of sales_array :', type(sales_array))
print('Type of Python list :', type(sales_list))
```

### Key difference: **Vectorized operations**

| | Python List | NumPy Array |
|---|---|---|
| Math on all elements | Need a loop | Just write the math directly |
| Speed (50,000 items) | Slow | ~100x faster |
| Memory | Each item stored separately | Compact, like a C array |
| Data type | Mixed (int, str, etc.) | All elements same type |

---
## Section 2: Creating NumPy Arrays


```python
# ── 2.1 From a Python list ────────────────────────────────────────────────────
a = np.array([10, 20, 30, 40, 50])
print('From list     :', a)

# ── 2.2 Zeros and Ones ───────────────────────────────────────────────────────
zeros  = np.zeros(5)          # 5 zeros
ones   = np.ones(5)           # 5 ones
filled = np.full(5, 99)       # 5 elements all equal to 99
print('All zeros     :', zeros)
print('All ones      :', ones)
print('Filled with 99:', filled)
```


```python
# ── 2.3 Range-based arrays ────────────────────────────────────────────────────
# np.arange(start, stop, step)  — like Python range()
months     = np.arange(1, 13)           # 1 to 12 (months in a year)
even_nums  = np.arange(0, 20, 2)        # 0, 2, 4, ..., 18
countdown  = np.arange(10, 0, -1)       # 10, 9, 8, ..., 1

print('Months :', months)
print('Evens  :', even_nums)
print('Reverse:', countdown)
```


```python
# ── 2.4 np.linspace — evenly spaced values ────────────────────────────────────
# linspace(start, stop, num_points)  — useful for interest rates, tax slabs
interest_rates = np.linspace(6.0, 12.0, 7)  # 7 rates from 6% to 12%
print('Interest rates (linspace):', interest_rates)

# ── 2.5 Random arrays ────────────────────────────────────────────────────────
np.random.seed(42)  # seed = reproducible results (same "random" every time)

rand_int  = np.random.randint(1000, 50000, size=6)    # 6 random integers between ₹1000-₹50000
rand_flt  = np.random.rand(4)                          # 4 random floats between 0 and 1

print('Random invoices (₹):', rand_int)
print('Random fractions   :', rand_flt.round(3))
```

---
## Section 3: Array Attributes — Understanding Your Data


```python
# Create a sample array
invoices = np.array([15000, 28000, 9500, 42000, 3200, 67000, 18500, 31000])

print('Array     :', invoices)
print('Shape     :', invoices.shape)    # number of elements in each dimension
print('Size      :', invoices.size)     # total number of elements
print('Dimensions:', invoices.ndim)     # number of dimensions (1D = 1, 2D = 2)
print('Data type :', invoices.dtype)    # int64, float64, etc.
print('Bytes used:', invoices.nbytes)   # memory in bytes
```


```python
# ── Data Types ────────────────────────────────────────────────────────────────
# NumPy is strict about data types — unlike Python lists

int_arr   = np.array([100, 200, 300])             # integers
float_arr = np.array([100.5, 200.75, 300.0])      # floats
str_arr   = np.array(['Sales', 'Purchase', 'Tax']) # strings

print('int64  dtype:', int_arr.dtype)
print('float64 dtype:', float_arr.dtype)
print('string dtype:', str_arr.dtype)

# Convert type using .astype()
int_to_float = int_arr.astype(float)
print('\nConverted to float:', int_to_float)
```

---
## Section 4: Indexing & Slicing — Accessing Elements


```python
# Our sample: 8 invoice amounts
invoices = np.array([15000, 28000, 9500, 42000, 3200, 67000, 18500, 31000])
#                      [0]    [1]   [2]   [3]   [4]   [5]    [6]    [7]
#                      [-8]   [-7]  [-6]  [-5]  [-4]  [-3]   [-2]   [-1]

# Single element
print('First invoice  :', invoices[0])    # index 0
print('Third invoice  :', invoices[2])    # index 2
print('Last invoice   :', invoices[-1])   # last element
print('2nd from last  :', invoices[-2])
```


```python
# ── Slicing: array[start : stop : step] ───────────────────────────────────────
# stop is EXCLUSIVE (just like Python range)

print('First 3         :', invoices[0:3])   # indices 0,1,2
print('Index 2 to 5    :', invoices[2:6])   # indices 2,3,4,5
print('Last 3          :', invoices[-3:])   # last 3 elements
print('Every other     :', invoices[::2])   # step=2: every alternate
print('Reversed        :', invoices[::-1])  # step=-1: reverse entire array

# Practical: get Q1 data (first 3 months)
monthly_rev = np.array([80, 92, 75, 110, 105, 98, 120, 115, 130, 95, 108, 140])
q1 = monthly_rev[0:3]
q2 = monthly_rev[3:6]
q3 = monthly_rev[6:9]
q4 = monthly_rev[9:12]
print('\nQ1 Revenue :', q1, '→ Total:', q1.sum())
print('Q2 Revenue :', q2, '→ Total:', q2.sum())
print('Q3 Revenue :', q3, '→ Total:', q3.sum())
print('Q4 Revenue :', q4, '→ Total:', q4.sum())
```

---
## Section 5: Arithmetic & Broadcasting


```python
# ── Element-wise arithmetic ───────────────────────────────────────────────────
revenue = np.array([500, 620, 480, 710, 590])
cogs    = np.array([300, 370, 290, 430, 355])

gross_profit = revenue - cogs                   # subtract arrays
gp_margin    = gross_profit / revenue * 100     # divide + multiply
tax          = gross_profit * 0.25              # multiply by scalar

print('Revenue      :', revenue)
print('COGS         :', cogs)
print('Gross Profit :', gross_profit)
print('GP Margin %  :', gp_margin.round(1))
print('Tax @25%     :', tax)
```


```python
# ── Broadcasting: operations between arrays of different shapes ───────────────
# Scalar broadcast: applies one value to ALL elements
prices    = np.array([100, 200, 150, 300, 250])
gst_rate  = 0.18  # scalar

gst_amount   = prices * gst_rate      # 0.18 is "broadcast" across all 5 prices
total_price  = prices + gst_amount

print('Base Price  :', prices)
print('GST (18%)   :', gst_amount)
print('Total Price :', total_price)

# ── Power and other operations ────────────────────────────────────────────────
principal = np.array([1_00_000, 2_50_000, 5_00_000])
rate      = 0.08
years     = 5
fv        = principal * (1 + rate) ** years   # compound interest formula
print('\nCompound value of ₹1L, 2.5L, 5L at 8% for 5 years:')
for p, f in zip(principal, fv):
    print(f'  ₹{p:>8,.0f}  →  ₹{f:>10,.0f}')
```

---
## Section 6: Aggregate Functions


```python
scores = np.array([78, 92, 65, 88, 73, 91, 55, 84, 79, 95])

# Basic statistics
print(f'Count  : {scores.size}')
print(f'Sum    : {scores.sum()}')
print(f'Mean   : {scores.mean():.2f}')
print(f'Median : {np.median(scores):.2f}')
print(f'Min    : {scores.min()}  at index {scores.argmin()}')
print(f'Max    : {scores.max()}  at index {scores.argmax()}')
print(f'Std Dev: {scores.std():.2f}')
print(f'Var    : {scores.var():.2f}')
print(f'Range  : {scores.max() - scores.min()}')
```


```python
# ── cumsum: running total ─────────────────────────────────────────────────────
# Very useful for running balance, cumulative revenue, etc.
monthly_cf = np.array([50, -30, 80, 20, -40, 60, 35, -10, 70, 45, 25, 90])
# Positive = cash inflow, Negative = cash outflow

cumulative = np.cumsum(monthly_cf)

print('Monthly CF   :', monthly_cf)
print('Running total:', cumulative)
print(f'\nYTD at month 6: {cumulative[5]}')
print(f'Year-end total: {cumulative[-1]}')
```


```python
# ── Sorting ───────────────────────────────────────────────────────────────────
invoice_amounts = np.array([5000, 28000, 1200, 45000, 8500, 32000, 500, 15000])

sorted_asc  = np.sort(invoice_amounts)           # smallest first
sorted_desc = np.sort(invoice_amounts)[::-1]     # largest first
sort_idx    = np.argsort(invoice_amounts)         # indices that would sort the array

print('Original    :', invoice_amounts)
print('Ascending   :', sorted_asc)
print('Descending  :', sorted_desc)
print('Sort indices:', sort_idx)
print('\nSmallest invoice index:', sort_idx[0], '→ amount:', invoice_amounts[sort_idx[0]])
print('Largest  invoice index:', sort_idx[-1], '→ amount:', invoice_amounts[sort_idx[-1]])
```

---
## Section 7: Boolean Filtering — Select What You Need


```python
# Boolean array: compare each element → returns True/False for each
expenses = np.array([1500, 45000, 800, 12000, 99000, 3200, 75000, 4500, 22000, 500])

high_value = expenses > 20000   # creates a boolean array
print('Original  :', expenses)
print('Is > 20000:', high_value)

# Use the boolean array to FILTER the data
high_expenses = expenses[high_value]
print('\nHigh value expenses (>20,000):', high_expenses)
```


```python
# ── Combining conditions with & (AND) and | (OR) ───────────────────────────────
amounts = np.array([500, 5000, 15000, 25000, 50000, 75000, 90000, 99500, 1_20_000])

# Amounts between ₹10,000 and ₹1,00,000
mid_range = amounts[(amounts >= 10_000) & (amounts <= 1_00_000)]
print('₹10K–₹1L   :', mid_range)

# Amounts either very small (<1000) or very large (>90000)
extremes  = amounts[(amounts < 1_000) | (amounts > 90_000)]
print('Extremes   :', extremes)

# np.where: conditional replacement
# np.where(condition, value_if_true, value_if_false)
labels = np.where(amounts > 50_000, 'Large', 'Small')
print('Labels     :', labels)
```


```python
# ── Counting and percentage ───────────────────────────────────────────────────
invoices = np.random.randint(1000, 1_50_000, size=200)
above_threshold = invoices > 50_000

count = above_threshold.sum()         # True = 1, False = 0
pct   = above_threshold.mean() * 100  # mean of True/False = proportion

print(f'Total invoices   : {len(invoices)}')
print(f'Above ₹50,000    : {count}')
print(f'Percentage       : {pct:.1f}%')
print(f'Total value >50K : ₹{invoices[above_threshold].sum():,.0f}')
```

---
## Section 8: 2D Arrays (Matrices)


```python
# A 2D array = a table (like a spreadsheet)
# Think: rows = months, columns = departments

# 4 quarters × 3 departments (Sales, HR, IT)
quarterly_expense = np.array([
    [45, 12, 18],   # Q1: Sales=45L, HR=12L, IT=18L
    [52, 13, 20],   # Q2
    [61, 14, 25],   # Q3
    [70, 15, 28],   # Q4
])

print('Shape:', quarterly_expense.shape)   # (4 rows, 3 cols)
print('Array:\n', quarterly_expense)
```


```python
# ── 2D Indexing: array[row, col] ──────────────────────────────────────────────
print('Q1 Sales     :', quarterly_expense[0, 0])   # row 0, col 0
print('Q3 IT        :', quarterly_expense[2, 2])   # row 2, col 2
print('All Q2 data  :', quarterly_expense[1, :])   # row 1, all columns
print('Sales all Qtrs:', quarterly_expense[:, 0])  # all rows, column 0
print('IT dept Q2-Q4:', quarterly_expense[1:, 2])  # rows 1-3, col 2

# ── Axis-wise aggregation ─────────────────────────────────────────────────────
# axis=0 → across rows (column totals)
# axis=1 → across columns (row totals)
print('\nDept totals  :', quarterly_expense.sum(axis=0))   # [228, 54, 91]
print('Qtr totals   :', quarterly_expense.sum(axis=1))    # [75, 85, 100, 113]
print('Grand total  :', quarterly_expense.sum())
```

---
## Section 9: Reshaping Arrays


```python
# ── reshape ───────────────────────────────────────────────────────────────────
# Use case: 12 monthly figures → 4×3 quarterly layout
monthly = np.array([80, 92, 75, 110, 105, 98, 120, 115, 130, 95, 108, 140])

quarterly_layout = monthly.reshape(4, 3)   # 4 quarters, 3 months each
print('Monthly (1D):\n', monthly)
print('\nQuarterly (2D, 4×3):\n', quarterly_layout)
print('Q1 average:', quarterly_layout[0].mean().round(1))
print('Q4 average:', quarterly_layout[3].mean().round(1))

# reshape back
flat_again = quarterly_layout.flatten()
print('\nFlattened back:', flat_again)
```


```python
# ── Transpose ─────────────────────────────────────────────────────────────────
# .T flips rows and columns (like Excel's TRANSPOSE function)

data = np.array([[100, 200, 300],   # 3 rows, 2 cols
                 [150, 250, 350],
                 [120, 220, 320]])

print('Original (3x3):\n', data)
print('\nTransposed (3x3):\n', data.T)  # rows become cols

# ── np.hstack / np.vstack — joining arrays ─────────────────────────────────────
q1_data = np.array([[80, 92, 75]])
q2_data = np.array([[110, 105, 98]])
combined = np.vstack([q1_data, q2_data])   # stack vertically (add rows)
print('\nCombined Q1+Q2:\n', combined)
```

---
## Section 10: Useful Math Functions


```python
x = np.array([1, 4, 9, 16, 25, 100])

print('Square root :', np.sqrt(x))         # useful for std deviation
print('Absolute    :', np.abs(np.array([-5, 3, -8, 2])))  # useful for variance
print('Log base 10 :', np.log10(x).round(3))  # useful for Benford\'s Law
print('Natural log :', np.log(x).round(3))     # useful for growth rates

# Rounding
amounts = np.array([1234.5678, 999.124, 55555.999])
print('Round 2dp   :', np.round(amounts, 2))
print('Floor       :', np.floor(amounts))      # round down
print('Ceil        :', np.ceil(amounts))        # round up
print('Round -3    :', np.round(amounts, -3))   # nearest 1000 — useful for MIS
```

---
## Section 11: Quick Reference Summary

```python
import numpy as np

# Create
np.array([1,2,3])            # from list
np.zeros(n)                  # n zeros
np.ones(n)                   # n ones
np.arange(start, stop, step) # like range()
np.linspace(start, stop, n)  # n evenly spaced points
np.random.randint(low, high, size=n)  # n random integers

# Attributes
a.shape     # dimensions
a.dtype     # data type
a.size      # total elements
a.ndim      # number of dimensions

# Indexing
a[0]        # first element
a[-1]       # last element
a[2:5]      # slice
a[r, c]     # 2D: row r, column c
a[:, c]     # all rows, column c

# Aggregation
a.sum()     a.mean()    a.min()    a.max()
a.std()     a.var()     np.median(a)
np.cumsum(a)            # running total
np.sort(a)              # sorted copy

# Boolean filter
a[a > 100]              # elements > 100
a[(a > 10) & (a < 50)]  # between 10 and 50
np.where(a > 0, 'Pos', 'Neg')  # conditional labels

# Shape
a.reshape(r, c)  # change shape
a.flatten()      # to 1D
a.T              # transpose
```

---
## Practice Exercises

1. Create an array of 12 monthly salaries: `[45000, 45000, 47000, 47000, 47000, 48000, 48000, 50000, 50000, 50000, 52000, 55000]`. Compute total, average, and the month with the highest salary.

2. Given a 5-year revenue array `[120, 145, 138, 162, 185]` (₹ in Lakhs), compute year-on-year growth% for each year.

3. An expense array has 20 items. Select only those expenses between ₹5,000 and ₹25,000. Count them and compute their total.

4. Create a 3×4 array representing 3 products × 4 quarters of sales. Compute total sales per product (row sum) and total sales per quarter (column sum).

5. Given `principal = 5,00,000`, `rate = 0.09`, compute the compound interest for years 1 through 10 using `np.arange()`.


```python
# ── Exercise Solutions ─────────────────────────────────────────────────────────

# Exercise 1: Salary analysis
salaries = np.array([45000, 45000, 47000, 47000, 47000, 48000,
                     48000, 50000, 50000, 50000, 52000, 55000])
print('Ex 1:')
print(f'  Total annual salary : ₹{salaries.sum():,.0f}')
print(f'  Average monthly     : ₹{salaries.mean():,.0f}')
print(f'  Highest salary month: Month {salaries.argmax()+1} (₹{salaries.max():,})')

# Exercise 2: YoY growth
revenue = np.array([120, 145, 138, 162, 185])
yoy_growth = (revenue[1:] - revenue[:-1]) / revenue[:-1] * 100
print('\nEx 2: Year-on-Year Revenue Growth%:')
for yr, g in enumerate(yoy_growth, start=2):
    print(f'  Year {yr}: {g:+.1f}%')

# Exercise 5: Compound Interest
principal = 5_00_000
rate      = 0.09
years     = np.arange(1, 11)
amounts   = principal * (1 + rate) ** years
print('\nEx 5: Compound Growth at 9%')
for yr, amt in zip(years, amounts):
    ci = amt - principal
    print(f'  Year {yr:2d}: ₹{amt:>10,.0f}  (interest: ₹{ci:>8,.0f})')
```
