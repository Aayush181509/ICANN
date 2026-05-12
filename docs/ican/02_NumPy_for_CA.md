# 🔢 NumPy for CA Professionals

**Fast, Large-Scale Numerical Computing in Python**
---
**Pre-requisite:** 
Module 1 — Python Basics  
**Session Duration:** 3–6 hours  
**Approach:** Concept → Fundamentals → Hands-on Practice

---

## 📋 Table of Contents

| Part | Section | Topic |
|------|---------|-------|
| **Part 1: Why NumPy?** | 1 | The Problem with Plain Python for Numbers |
| | 2 | What is NumPy? — History & Ecosystem |
| **Part 2: Fundamentals** | 3 | The ndarray — NumPy's Core Object |
| | 4 | NumPy Data Types (dtype) |
| | 5 | Creating Arrays — 6 Methods |
| **Part 3: Hands-on** | 6 | Installing & Importing NumPy |
| | 7 | Creating NumPy Arrays |
| | 8 | Array vs Python List — Speed Comparison |
| | 9 | Vectorized Financial Math |
| | 10 | Array Indexing & Slicing |
| | 11 | Statistical Functions |
| | 12 | Boolean Indexing — Filtering |
| | 13 | 2D Arrays — Financial Matrices |
| **Part 4: Finance Applications** | 14 | Returns & Portfolio Analysis |
| | 15 | NPV & IRR Calculations |
| **Part 5: Practice** | 16 | Practice Exercises |

---

---

## Part 1: Why NumPy?

---

## Section 1: The Problem with Plain Python for Numbers

### Python lists are general-purpose — and that's the problem

Python lists are incredibly flexible. They can hold strings, integers, floats, even other lists — all in the same list. But that flexibility comes at a cost when you need to do **mathematical operations on large datasets**.

Consider a real scenario: you have **10,000 invoice amounts** and need to apply 13% VAT to all of them.

**The Python list approach:**
- Python stores each number as a full Python object (with type info, reference counts, etc.)
- Each object sits at a different memory location
- To add 13% VAT, Python must loop through each element one-by-one
- For 10,000 invoices → 10,000 separate operations

**The NumPy approach:**
- Numbers are stored as raw C-level data in a single contiguous block of memory
- Operations apply to the **entire block at once** using optimised C/Fortran code
- For 10,000 invoices → 1 operation

> *"The difference is like processing salary slips one-by-one vs running a payroll batch."*

### Why does this matter for CA professionals?

| Scenario | Records | Python List | NumPy Array |
|----------|---------|-------------|-------------|
| VAT on invoices | 10,000 | ~50 ms | ~0.1 ms (500× faster) |
| Payroll calculations | 50,000 | ~250 ms | ~0.5 ms |
| Stock return analysis | 1,000,000 | ~5 sec | ~10 ms |
| Trial balance ratios | 500 accounts | instant | instant |

The gap widens dramatically as data grows. This is why every serious financial analytics tool is built on NumPy.


```python
import time

# Compare: calculate VAT on 100,000 invoices
n = 100_000
amounts_list  = list(range(1000, n + 1000))   # Python list
import numpy as np
amounts_array = np.arange(1000, n + 1000)      # NumPy array

# Python list — needs a loop
start = time.time()
vat_list = [x * 0.13 for x in amounts_list]
time_list = time.time() - start

# NumPy — no loop, vectorized
start = time.time()
vat_array = amounts_array * 0.13
time_numpy = time.time() - start

print(f'Dataset size:      {n:,} invoices')
print(f'Python list time:  {time_list*1000:.2f} ms')
print(f'NumPy array time:  {time_numpy*1000:.4f} ms')
print(f'NumPy is {time_list/time_numpy:.0f}× faster')
print()
print('Result check (first 5):')
print('  List :', vat_list[:5])
print('  NumPy:', vat_array[:5])

```

    Dataset size:      100,000 invoices
    Python list time:  1.76 ms
    NumPy array time:  0.1130 ms
    NumPy is 16× faster
    
    Result check (first 5):
      List : [130.0, 130.13, 130.26, 130.39000000000001, 130.52]
      NumPy: [130.   130.13 130.26 130.39 130.52]


## Section 2: What is NumPy?

### A brief history

NumPy (**Num**erical **Py**thon) was created by **Travis Oliphant** in 2005 by merging two earlier libraries — `Numeric` and `Numarray`. It has since become the **foundation of virtually every scientific and financial computing tool in Python**.

```
Python Ecosystem (simplified)
─────────────────────────────────────────────────────
  Your Code
      │
  Pandas ──── Matplotlib ──── Seaborn ──── scikit-learn
      │              │                          │
      └──────── NumPy ────────────────────────────
                    │
              C / Fortran (BLAS, LAPACK)
─────────────────────────────────────────────────────
```

Everything in data science and finance analytics sits on top of NumPy. When you do `df['Amount'] * 1.13` in Pandas, Pandas calls NumPy internally.

### Where NumPy fits in your workflow

| Task | Tool |
|------|------|
| Clean & query tabular data | Pandas (built on NumPy) |
| Visualise data | Matplotlib / Seaborn (built on NumPy) |
| Statistical modelling | SciPy (built on NumPy) |
| Machine learning | scikit-learn (built on NumPy) |
| **Raw numerical computation** | **NumPy directly** |
| Portfolio maths, NPV, IRR | NumPy directly |
| Batch calculations on arrays | NumPy directly |

You will use NumPy directly for financial math, and indirectly through Pandas for data analysis.

---

## Part 2: NumPy Fundamentals

---

## Section 3: The `ndarray` — NumPy's Core Object

### What is an ndarray?

`ndarray` stands for **N-Dimensional Array**. It is the fundamental building block of NumPy — everything NumPy does revolves around this object.

Think of it this way:

| Dimension | Also called | Finance analogy |
|-----------|-------------|-----------------|
| 1D array | Vector | A single column of invoice amounts |
| 2D array | Matrix | A table: rows = months, columns = departments |
| 3D array | Tensor | Multiple tables: one per financial year |

### What makes ndarray special?

**1. Homogeneous** — all elements are the same data type (unlike Python lists)  
**2. Fixed size** — size is set at creation (memory is pre-allocated)  
**3. Contiguous memory** — elements sit next to each other in RAM (fast access)  
**4. Vectorized** — mathematical operations work on the whole array at once

### Key properties every ndarray has

```
array.shape     → Dimensions as a tuple — (rows, columns)
array.ndim      → Number of dimensions — 1D, 2D, 3D
array.size      → Total number of elements
array.dtype     → Data type of elements — int64, float64, bool, etc.
array.itemsize  → Bytes each element uses in memory
array.nbytes    → Total bytes used (size × itemsize)
```


```python
import numpy as np

# 1D array — one column of data
monthly_revenue = np.array([1250000, 1380000, 1120000, 1450000,
                             1620000, 1780000, 1550000, 1420000,
                             1680000, 1910000, 2030000, 2150000])

print('=== 1D Array Properties ===')
print(f'Data:       {monthly_revenue}')
print(f'shape:      {monthly_revenue.shape}    <- (12,) means 1D with 12 elements')
print(f'ndim:       {monthly_revenue.ndim}       <- 1 dimension')
print(f'size:       {monthly_revenue.size}      <- 12 elements total')
print(f'dtype:      {monthly_revenue.dtype}   <- 64-bit integer')
print(f'itemsize:   {monthly_revenue.itemsize} bytes per element')
print(f'nbytes:     {monthly_revenue.nbytes}  bytes total in memory')
print()

# 2D array — a table: 4 quarters x 4 departments
dept_revenue = np.array([
    [500000, 350000, 120000, 180000],
    [520000, 360000, 125000, 195000],
    [480000, 340000, 118000, 185000],
    [560000, 390000, 132000, 210000],
])

print('=== 2D Array Properties ===')
print(f'shape:  {dept_revenue.shape}  <- 4 rows (quarters), 4 columns (departments)')
print(f'ndim:   {dept_revenue.ndim}           <- 2 dimensions')
print(f'size:   {dept_revenue.size}          <- 16 elements total (4x4)')

```

    === 1D Array Properties ===
    Data:       [1250000 1380000 1120000 1450000 1620000 1780000 1550000 1420000 1680000
     1910000 2030000 2150000]
    shape:      (12,)    <- (12,) means 1D with 12 elements
    ndim:       1       <- 1 dimension
    size:       12      <- 12 elements total
    dtype:      int64   <- 64-bit integer
    itemsize:   8 bytes per element
    nbytes:     96  bytes total in memory
    
    === 2D Array Properties ===
    shape:  (4, 4)  <- 4 rows (quarters), 4 columns (departments)
    ndim:   2           <- 2 dimensions
    size:   16          <- 16 elements total (4x4)


## Section 4: NumPy Data Types (`dtype`)

### Why dtype matters

Unlike Python lists (which hold mixed types), every element in a NumPy array is the **same type**. This is what enables the speed advantage — NumPy knows exactly how many bytes each element needs and can process them all with a single C-level loop.

Choosing the right dtype can also **save significant memory** — important when working with millions of rows.

### Common dtypes in financial work

| dtype | Size | Range / Precision | Use case |
|-------|------|-------------------|----------|
| `int32` | 4 bytes | ±2.1 billion | Invoice counts, quantities |
| `int64` | 8 bytes | ±9.2 × 10¹⁸ | Amounts in paisa (large) |
| `float32` | 4 bytes | ~7 decimal digits | Ratios, percentages |
| `float64` | 8 bytes | ~15 decimal digits | Monetary values, rates |
| `bool` | 1 byte | True / False | Flags, audit status |

> ⚠️ **For monetary calculations, always use `float64` (the default).** `float32` can introduce rounding errors in financial calculations.

### Memory impact — a real example

A dataset of 1 million invoice amounts:
- `float64` → 8 MB
- `float32` → 4 MB (half the memory, but less precision)
- `int32`   → 4 MB (if amounts are whole NPR amounts)


```python
import numpy as np

# Default dtype inference
a = np.array([45000, 82000, 31500])      # Python ints -> int64 by default
b = np.array([18.5, 12.0, 5.0])          # Python floats -> float64 by default
c = np.array([True, False, True])         # Python bools -> bool

print('Integer array dtype:', a.dtype)
print('Float array dtype:  ', b.dtype)
print('Bool array dtype:   ', c.dtype)
print()

# Explicit dtype — control precision and memory
amounts_f64 = np.array([45000.75, 82000.50, 31500.25], dtype=np.float64)
amounts_f32 = np.array([45000.75, 82000.50, 31500.25], dtype=np.float32)

print('float64 precision:', amounts_f64)
print('float32 precision:', amounts_f32)  # Note subtle rounding
print()
print('Memory - float64:', amounts_f64.nbytes, 'bytes')
print('Memory - float32:', amounts_f32.nbytes, 'bytes')
print()

# Type conversion (casting)
invoice_ids = np.array([1001, 1002, 1003, 1004], dtype=np.int32)
print('Invoice IDs (int32):', invoice_ids, '| dtype:', invoice_ids.dtype)
as_float = invoice_ids.astype(np.float64)
print('Converted (float64):', as_float, '| dtype:', as_float.dtype)

```

    Integer array dtype: int64
    Float array dtype:   float64
    Bool array dtype:    bool
    
    float64 precision: [45000.75 82000.5  31500.25]
    float32 precision: [45000.75 82000.5  31500.25]
    
    Memory - float64: 24 bytes
    Memory - float32: 12 bytes
    
    Invoice IDs (int32): [1001 1002 1003 1004] | dtype: int32
    Converted (float64): [1001. 1002. 1003. 1004.] | dtype: float64


## Section 5: Creating Arrays — 6 Methods

Before you can analyse data with NumPy, you need to get your data into an `ndarray`. There are several ways to do this depending on where your data comes from.

| Method | Use when... |
|--------|-------------|
| `np.array(list)` | You already have a Python list |
| `np.zeros(n)` | Initialising a blank result container |
| `np.ones(n)` | Setting up a uniform weights array |
| `np.arange(start, stop, step)` | Generating a sequence (like Excel's SEQUENCE) |
| `np.linspace(start, stop, n)` | Evenly spaced values between two numbers |
| `np.full(shape, value)` | Filling an array with a constant |

These are the foundations — in practice you'll most often load data via Pandas (Module 3), which stores its columns as NumPy arrays internally.

## Section 6: Installing & Importing NumPy


```python
# Run this cell ONCE to install NumPy (if not already installed)
# !pip install numpy

# Import NumPy — 'np' is the universal shorthand (everyone uses this)
import numpy as np

print('NumPy version:', np.__version__)
print('NumPy imported successfully!')
```

    NumPy version: 2.2.6
    NumPy imported successfully!


## Section 7: Creating NumPy Arrays

A NumPy **array** is like an Excel column — it holds a sequence of numbers (all of the same type).  
Unlike Python lists, NumPy arrays are designed for **mathematical operations**.

### Ways to create arrays


```python
# Method 1: From a Python list
invoice_amounts = np.array([45000, 82000, 31500, 97000, 54000, 120000, 63000])
print('Invoice Amounts:', invoice_amounts)
print('Type:', type(invoice_amounts))
print('Data type inside array:', invoice_amounts.dtype)   # int64 = whole numbers
print('Number of invoices:', invoice_amounts.size)
```

    Invoice Amounts: [ 45000  82000  31500  97000  54000 120000  63000]
    Type: <class 'numpy.ndarray'>
    Data type inside array: int64
    Number of invoices: 7



```python
# Method 2: np.zeros() — start with all zeros (useful for initializing tables)
tax_buckets = np.zeros(5)   # 5 tax slabs, all starting at 0
print('Empty tax buckets:', tax_buckets)

# Method 3: np.arange() — like range() but returns an array
# Create months 1 to 12
months = np.arange(1, 13)
print('Months:', months)

# Method 4: np.linspace() — evenly spaced values between two numbers
# Create 5 equally-spaced interest rates between 6% and 12%
rates = np.linspace(6.0, 12.0, 5)
print('Interest rate range:', rates, '%')
```

    Empty tax buckets: [0. 0. 0. 0. 0.]
    Months: [ 1  2  3  4  5  6  7  8  9 10 11 12]
    Interest rate range: [ 6.   7.5  9.  10.5 12. ] %



```python
# Monthly revenue data for FY 2081-82 BS (Shrawan to Ashadh)
month_names = ['Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra', 'Baishakh', 'Jestha', 'Ashadh']

monthly_revenue = np.array([
    1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
    1550000, 1420000, 1680000, 1910000, 2030000, 2150000
])

monthly_expenses = np.array([
     920000,  980000,  870000, 1050000, 1180000, 1250000,
    1100000, 1020000, 1190000, 1320000, 1410000, 1490000
])

print('Revenue data loaded:', len(monthly_revenue), 'months')
print('Shape:', monthly_revenue.shape)   # (12,) means 1D array with 12 elements
```

    Revenue data loaded: 12 months
    Shape: (12,)


## Section 8: Array vs Python List — Why NumPy is Faster

The key difference: with Python lists, operations happen **one item at a time**.  
With NumPy arrays, operations happen on **the entire array at once** (vectorization).


```python
# Python list — calculating GST (you need a loop)
amounts_list = [45000, 82000, 31500, 97000, 54000]
vat_list = []
for amount in amounts_list:
    vat_list.append(amount * 0.13)
print('GST (list method):', vat_list)

# NumPy array — same operation, NO loop needed!
amounts_array = np.array([45000, 82000, 31500, 97000, 54000])
vat_array = amounts_array * 0.13    # Applies to ALL elements at once
print('GST (NumPy method):', vat_array)

# With NumPy you can also do element-wise operations between two arrays
total_with_gst = amounts_array + vat_array
print('Total with GST:', total_with_gst)
```

    GST (list method): [5850.0, 10660.0, 4095.0, 12610.0, 7020.0]
    GST (NumPy method): [ 5850. 10660.  4095. 12610.  7020.]
    Total with GST: [ 50850.  92660.  35595. 109610.  61020.]


## Section 9: Array Operations — Vectorized Financial Math

With NumPy, you can do **arithmetic on entire columns of data** without writing a single loop.  
This is called **vectorization** — operations are applied element-by-element automatically.


```python
# Monthly P&L calculated from arrays
monthly_revenue = np.array([
    1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
    1550000, 1420000, 1680000, 1910000, 2030000, 2150000
])
monthly_expenses = np.array([
     920000,  980000,  870000, 1050000, 1180000, 1250000,
    1100000, 1020000, 1190000, 1320000, 1410000, 1490000
])

month_names = ['Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra', 'Baishakh', 'Jestha', 'Ashadh']

# All these are vectorized — no loop needed!
monthly_profit = monthly_revenue - monthly_expenses
profit_margin  = (monthly_profit / monthly_revenue) * 100
vat_collected  = monthly_revenue * 0.13

print(f"{'Month':<6} {'Revenue':>12} {'Expenses':>12} {'Profit':>12} {'Margin':>8}")
print('-' * 54)
for i, month in enumerate(month_names):
    print(f"{month:<6} NPR {monthly_revenue[i]:>10,} NPR {monthly_expenses[i]:>10,} "
          f"NPR {monthly_profit[i]:>10,} {profit_margin[i]:>7.1f}%")
```

    Month       Revenue     Expenses       Profit   Margin
    ------------------------------------------------------
    Shrawan NPR  1,250,000 NPR    920,000 NPR    330,000    26.4%
    Bhadra NPR  1,380,000 NPR    980,000 NPR    400,000    29.0%
    Ashwin NPR  1,120,000 NPR    870,000 NPR    250,000    22.3%
    Kartik NPR  1,450,000 NPR  1,050,000 NPR    400,000    27.6%
    Mangsir NPR  1,620,000 NPR  1,180,000 NPR    440,000    27.2%
    Poush  NPR  1,780,000 NPR  1,250,000 NPR    530,000    29.8%
    Magh   NPR  1,550,000 NPR  1,100,000 NPR    450,000    29.0%
    Falgun NPR  1,420,000 NPR  1,020,000 NPR    400,000    28.2%
    Chaitra NPR  1,680,000 NPR  1,190,000 NPR    490,000    29.2%
    Baishakh NPR  1,910,000 NPR  1,320,000 NPR    590,000    30.9%
    Jestha NPR  2,030,000 NPR  1,410,000 NPR    620,000    30.5%
    Ashadh NPR  2,150,000 NPR  1,490,000 NPR    660,000    30.7%



```python
# Year-on-year growth calculation
fy2024_revenue = np.array([980000, 1050000, 890000, 1100000, 1250000, 1380000,
                           1200000, 1100000, 1350000, 1560000, 1700000, 1820000])
fy2025_revenue = np.array([1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
                           1550000, 1420000, 1680000, 1910000, 2030000, 2150000])

# Growth rate — calculated for ALL 12 months at once
growth_pct = ((fy2025_revenue - fy2024_revenue) / fy2024_revenue) * 100

month_names = ['Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra', 'Baishakh', 'Jestha', 'Ashadh']

print('Month-wise Year-on-Year Revenue Growth')
print(f"{'Month':<6} {'FY 2081 BS':>12} {'FY 2082 BS':>12} {'Growth':>8}")
print('-' * 42)
for i, m in enumerate(month_names):
    arrow = '↑' if growth_pct[i] > 0 else '↓'
    print(f"{m:<6} NPR {fy2024_revenue[i]:>10,} NPR {fy2025_revenue[i]:>10,} {arrow}{abs(growth_pct[i]):>6.1f}%")
```

    Month-wise Year-on-Year Revenue Growth
    Month    FY 2081 BS   FY 2082 BS   Growth
    ------------------------------------------
    Shrawan NPR    980,000 NPR  1,250,000 ↑  27.6%
    Bhadra NPR  1,050,000 NPR  1,380,000 ↑  31.4%
    Ashwin NPR    890,000 NPR  1,120,000 ↑  25.8%
    Kartik NPR  1,100,000 NPR  1,450,000 ↑  31.8%
    Mangsir NPR  1,250,000 NPR  1,620,000 ↑  29.6%
    Poush  NPR  1,380,000 NPR  1,780,000 ↑  29.0%
    Magh   NPR  1,200,000 NPR  1,550,000 ↑  29.2%
    Falgun NPR  1,100,000 NPR  1,420,000 ↑  29.1%
    Chaitra NPR  1,350,000 NPR  1,680,000 ↑  24.4%
    Baishakh NPR  1,560,000 NPR  1,910,000 ↑  22.4%
    Jestha NPR  1,700,000 NPR  2,030,000 ↑  19.4%
    Ashadh NPR  1,820,000 NPR  2,150,000 ↑  18.1%


## Section 10: Array Indexing & Slicing

Accessing specific elements or ranges from a NumPy array — same logic as Python lists, but more powerful.


```python
monthly_revenue = np.array([
    1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
    1550000, 1420000, 1680000, 1910000, 2030000, 2150000
])
# Index:       0        1        2        3        4        5
#              6        7        8        9       10       11

# Single element
print('Shrawan revenue:     NPR ', monthly_revenue[0])    # First month
print('Ashadh revenue:     NPR ', monthly_revenue[-1])   # Last month
print('Chaitra revenue:  NPR ', monthly_revenue[8])    # 9th element (index 8)

# Slicing — ranges
q1 = monthly_revenue[0:3]   # Shrawan, Bhadra, Ashwin (Q1)
q2 = monthly_revenue[3:6]   # Kartik, Mangsir, Poush (Q2)
q3 = monthly_revenue[6:9]   # Magh, Falgun, Chaitra (Q3)
q4 = monthly_revenue[9:]    # Baishakh, Jestha, Ashadh (Q4)

print('\nQuarterly Revenue:')
print(f'Q1 Shrawan-Ashwin: NPR {sum(q1):,}')
print(f'Q2 Kartik-Poush:   NPR {sum(q2):,}')
print(f'Q3 Magh-Chaitra:   NPR {sum(q3):,}')
print(f'Q4 Baishakh-Ashadh: NPR {sum(q4):,}')
```

    Shrawan revenue:     NPR  1250000
    Ashadh revenue:     NPR  2150000
    Chaitra revenue:  NPR  1680000
    
    Quarterly Revenue:
    Q1 Shrawan-Ashwin: NPR 3,750,000
    Q2 Kartik-Poush:   NPR 4,850,000
    Q3 Magh-Chaitra:   NPR 4,650,000
    Q4 Baishakh-Ashadh: NPR 6,090,000


## Section 11: Statistical Functions

NumPy has built-in functions for all common statistical measures — essential for financial analysis.


```python
monthly_revenue = np.array([
    1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
    1550000, 1420000, 1680000, 1910000, 2030000, 2150000
])

print('=== Revenue Statistical Summary (FY 2081-82 BS) ===')
print(f'Total Annual Revenue:   NPR {np.sum(monthly_revenue):>15,}')
print(f'Average Monthly:        NPR {np.mean(monthly_revenue):>15,.2f}')
print(f'Median Monthly:         NPR {np.median(monthly_revenue):>15,.2f}')
print(f'Best Month:             NPR {np.max(monthly_revenue):>15,}')
print(f'Worst Month:            NPR {np.min(monthly_revenue):>15,}')
print(f'Std Deviation:          NPR {np.std(monthly_revenue):>15,.2f}')
print(f'Variance:               NPR {np.var(monthly_revenue):>15,.2f}')
print()
print(f'Best month index:       Month {np.argmax(monthly_revenue) + 1} (March)')  
print(f'Worst month index:      Month {np.argmin(monthly_revenue) + 1} (June)')

# Percentile — useful for bonus calculations or risk thresholds
p25 = np.percentile(monthly_revenue, 25)
p75 = np.percentile(monthly_revenue, 75)
print(f'\n25th Percentile:        NPR {p25:>15,.2f}')
print(f'75th Percentile:        NPR {p75:>15,.2f}')
print(f'Interquartile Range:    NPR {p75-p25:>15,.2f}  (measure of spread)')
```

    === Revenue Statistical Summary (FY 2081-82 BS) ===
    Total Annual Revenue:   NPR      19,340,000
    Average Monthly:        NPR    1,611,666.67
    Median Monthly:         NPR    1,585,000.00
    Best Month:             NPR       2,150,000
    Worst Month:            NPR       1,120,000
    Std Deviation:          NPR      299,967.59
    Variance:               NPR 89,980,555,555.56
    
    Best month index:       Month 12 (March)
    Worst month index:      Month 3 (June)
    
    25th Percentile:        NPR    1,410,000.00
    75th Percentile:        NPR    1,812,500.00
    Interquartile Range:    NPR      402,500.00  (measure of spread)



```python
# Cumulative sum — like a running total in a ledger
monthly_profit = np.array([330000, 400000, 250000, 400000, 440000, 530000,
                           450000, 400000, 490000, 590000, 620000, 660000])
month_names = ['Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra', 'Baishakh', 'Jestha', 'Ashadh']

cumulative_profit = np.cumsum(monthly_profit)   # Running total

print('Month-wise Cumulative Profit')
print(f"{'Month':<5} {'Monthly Profit':>15} {'Cumulative':>15}")
print('-' * 38)
for i, month in enumerate(month_names):
    print(f"{month:<5} NPR {monthly_profit[i]:>13,} NPR {cumulative_profit[i]:>13,}")
```

    Month-wise Cumulative Profit
    Month  Monthly Profit      Cumulative
    --------------------------------------
    Shrawan NPR       330,000 NPR       330,000
    Bhadra NPR       400,000 NPR       730,000
    Ashwin NPR       250,000 NPR       980,000
    Kartik NPR       400,000 NPR     1,380,000
    Mangsir NPR       440,000 NPR     1,820,000
    Poush NPR       530,000 NPR     2,350,000
    Magh  NPR       450,000 NPR     2,800,000
    Falgun NPR       400,000 NPR     3,200,000
    Chaitra NPR       490,000 NPR     3,690,000
    Baishakh NPR       590,000 NPR     4,280,000
    Jestha NPR       620,000 NPR     4,900,000
    Ashadh NPR       660,000 NPR     5,560,000


## Section 12: Boolean Indexing — Filtering Transactions

One of NumPy's most powerful features — filter data using conditions, without writing a loop.  
This is like **AutoFilter in Excel**, but applied instantly to millions of rows.


```python
# Invoice data
invoice_amounts = np.array([45000, 182000, 31500, 97000, 254000, 18000,
                             320000, 67000, 145000, 9500, 88000, 410000])

# Boolean indexing — creates a True/False mask
high_value_mask = invoice_amounts > 100000
print('High value mask:', high_value_mask)

# Apply mask to get only high-value invoices
high_value_invoices = invoice_amounts[high_value_mask]
print('High value invoices (>NPR 1L):', high_value_invoices)
print('Count:', len(high_value_invoices))
print('Total:', np.sum(high_value_invoices))
```

    High value mask: [False  True False False  True False  True False  True False False  True]
    High value invoices (>NPR 1L): [182000 254000 320000 145000 410000]
    Count: 5
    Total: 1311000



```python
# More filtering examples
invoice_amounts = np.array([45000, 182000, 31500, 97000, 254000, 18000,
                             320000, 67000, 145000, 9500, 88000, 410000])

# Invoices in a specific range (like a tax audit threshold)
audit_sample = invoice_amounts[(invoice_amounts >= 50000) & (invoice_amounts <= 200000)]
print('Audit sample (NPR 50K to NPR 2L):', audit_sample)

# Invoices below threshold — possible small cash transactions
small_transactions = invoice_amounts[invoice_amounts < 20000]
print('Small transactions (<NPR 20K):', small_transactions)

# np.where() — like Excel's IF function — returns values based on condition
risk_flag = np.where(invoice_amounts > 200000, 'HIGH RISK', 'Normal')
print('\nRisk Classification:')
for amt, risk in zip(invoice_amounts, risk_flag):
    print(f'  NPR {amt:>8,}  →  {risk}')
```

    Audit sample (NPR 50K to NPR 2L): [182000  97000  67000 145000  88000]
    Small transactions (<NPR 20K): [18000  9500]
    
    Risk Classification:
      NPR   45,000  →  Normal
      NPR  182,000  →  Normal
      NPR   31,500  →  Normal
      NPR   97,000  →  Normal
      NPR  254,000  →  HIGH RISK
      NPR   18,000  →  Normal
      NPR  320,000  →  HIGH RISK
      NPR   67,000  →  Normal
      NPR  145,000  →  Normal
      NPR    9,500  →  Normal
      NPR   88,000  →  Normal
      NPR  410,000  →  HIGH RISK


## Section 13: 2D Arrays — Financial Matrices

NumPy arrays can be **2-dimensional** — like a table with rows and columns.  
Think of a 2D array as an entire Excel sheet (rows = time periods, columns = items).


```python
# 2D array — Quarterly data for 4 departments
# Rows = Quarters (Q1, Q2, Q3, Q4)
# Columns = Departments (Sales, Operations, HR, IT)

dept_budgets = np.array([
    [500000, 350000, 120000, 180000],   # Q1
    [520000, 360000, 125000, 195000],   # Q2
    [480000, 340000, 118000, 185000],   # Q3
    [560000, 390000, 132000, 210000],   # Q4
])

dept_names = ['Sales', 'Operations', 'HR', 'IT']
quarter_names = ['Q1', 'Q2', 'Q3', 'Q4']

print('Shape:', dept_budgets.shape)   # (4 rows, 4 columns)

# Accessing elements: [row, column]
print('Q1 Sales budget:    NPR ', dept_budgets[0, 0])   # Row 0, Col 0
print('Q3 IT budget:       NPR ', dept_budgets[2, 3])   # Row 2, Col 3

# Get entire row (Q2 data)
print('All Q2 budgets:     ', dept_budgets[1, :])

# Get entire column (all HR budgets)
print('All HR budgets:     ', dept_budgets[:, 2])
```

    Shape: (4, 4)
    Q1 Sales budget:    NPR  500000
    Q3 IT budget:       NPR  185000
    All Q2 budgets:      [520000 360000 125000 195000]
    All HR budgets:      [120000 125000 118000 132000]



```python
# Aggregate across rows and columns — like Excel's SUM
dept_budgets = np.array([
    [500000, 350000, 120000, 180000],
    [520000, 360000, 125000, 195000],
    [480000, 340000, 118000, 185000],
    [560000, 390000, 132000, 210000],
])
dept_names   = ['Sales', 'Operations', 'HR', 'IT']
quarter_names = ['Q1', 'Q2', 'Q3', 'Q4']

# axis=0 → sum down columns (total per department)
dept_totals = np.sum(dept_budgets, axis=0)

# axis=1 → sum across rows (total per quarter)
quarter_totals = np.sum(dept_budgets, axis=1)

print('Annual Budget by Department:')
for dept, total in zip(dept_names, dept_totals):
    print(f'  {dept:<12}: NPR {total:>10,}')

print('\nTotal Budget by Quarter:')
for qtr, total in zip(quarter_names, quarter_totals):
    print(f'  {qtr}: NPR {total:>10,}')

print(f'\nGrand Total: NPR {np.sum(dept_budgets):,}')
```

    Annual Budget by Department:
      Sales       : NPR  2,060,000
      Operations  : NPR  1,440,000
      HR          : NPR    495,000
      IT          : NPR    770,000
    
    Total Budget by Quarter:
      Q1: NPR  1,150,000
      Q2: NPR  1,200,000
      Q3: NPR  1,123,000
      Q4: NPR  1,292,000
    
    Grand Total: NPR 4,765,000


## Section 14: Financial Applications — Returns & Portfolio

NumPy is widely used in finance for **investment analysis**. Here we calculate stock returns and basic portfolio statistics.


```python
# Calculate daily/monthly returns from price data
# Simple return = (Price_today - Price_yesterday) / Price_yesterday

# Monthly closing prices of a stock (NPR )
stock_prices = np.array([1200, 1285, 1190, 1340, 1410, 1380,
                          1455, 1510, 1490, 1620, 1585, 1710])
month_names = ['Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir', 'Poush', 'Magh', 'Falgun', 'Chaitra', 'Baishakh', 'Jestha', 'Ashadh']

# Calculate monthly returns using np.diff()
price_changes = np.diff(stock_prices)          # Price difference month-to-month
returns_pct   = (price_changes / stock_prices[:-1]) * 100   # % return

print('Monthly Stock Returns')
print(f"{'Month':<5} {'Price':>8} {'Return':>8}")
print('-' * 26)
print(f"{'Shrawan':<7} NPR {stock_prices[0]:>6}   Base")
for i, month in enumerate(month_names[1:]):
    arrow = '▲' if returns_pct[i] > 0 else '▼'
    print(f"{month:<5} NPR {stock_prices[i+1]:>6} {arrow}{abs(returns_pct[i]):>6.2f}%")

print(f'\nAverage Monthly Return: {np.mean(returns_pct):.2f}%')
print(f'Volatility (Std Dev):   {np.std(returns_pct):.2f}%')
total_return = (stock_prices[-1] - stock_prices[0]) / stock_prices[0] * 100
print(f'Annual Return (Shrawan-Ashadh): {total_return:.2f}%')
```

    Monthly Stock Returns
    Month    Price   Return
    --------------------------
    Shrawan NPR   1200   Base
    Bhadra NPR   1285 ▲  7.08%
    Ashwin NPR   1190 ▼  7.39%
    Kartik NPR   1340 ▲ 12.61%
    Mangsir NPR   1410 ▲  5.22%
    Poush NPR   1380 ▼  2.13%
    Magh  NPR   1455 ▲  5.43%
    Falgun NPR   1510 ▲  3.78%
    Chaitra NPR   1490 ▼  1.32%
    Baishakh NPR   1620 ▲  8.72%
    Jestha NPR   1585 ▼  2.16%
    Ashadh NPR   1710 ▲  7.89%
    
    Average Monthly Return: 3.43%
    Volatility (Std Dev):   5.68%
    Annual Return (Shrawan-Ashadh): 42.50%



```python
# Portfolio Return Calculation
# A client's portfolio: 3 stocks with different allocations

stocks    = np.array(['NTC',    'Ncell', 'Nabil Bank'])
invested  = np.array([500000,   300000,    200000])       # Amount invested
returns   = np.array([18.5,     22.3,      14.8])         # Annual return %

# Portfolio weights (what fraction is each stock?)
total_investment = np.sum(invested)
weights = invested / total_investment

# Portfolio return = weighted average of individual returns
portfolio_return = np.sum(weights * returns)

# Actual profit from each stock
profit_per_stock = invested * returns / 100
total_profit = np.sum(profit_per_stock)

print('=== Portfolio Analysis ===')
print(f"{'Stock':<12} {'Invested':>12} {'Weight':>8} {'Return':>8} {'Profit':>12}")
print('-' * 56)
for i in range(len(stocks)):
    print(f"{stocks[i]:<12} NPR {invested[i]:>10,} {weights[i]*100:>7.1f}% {returns[i]:>7.1f}% NPR {profit_per_stock[i]:>10,.2f}")
print('-' * 56)
print(f"{'TOTAL':<12} NPR {total_investment:>10,} {'100.0%':>8} {portfolio_return:>7.2f}% NPR {total_profit:>10,.2f}")
```

    === Portfolio Analysis ===
    Stock            Invested   Weight   Return       Profit
    --------------------------------------------------------
    NTC          NPR    500,000    50.0%    18.5% NPR  92,500.00
    Ncell        NPR    300,000    30.0%    22.3% NPR  66,900.00
    Nabil Bank   NPR    200,000    20.0%    14.8% NPR  29,600.00
    --------------------------------------------------------
    TOTAL        NPR  1,000,000   100.0%   18.90% NPR 189,000.00


## Section 15: NPV & IRR Calculations

**Net Present Value (NPV)** and **Internal Rate of Return (IRR)** are fundamental to capital budgeting.  
NumPy provides ready-to-use functions for both — no more manual discounting!


```python
# NPV Calculation
# A company is considering buying a machine for NPR 10,00,000
# Expected cash flows over 5 years:

initial_investment = -1000000   # Negative because it's an outflow

# Cash inflows for years 1-5
cash_inflows = np.array([250000, 300000, 350000, 320000, 280000])

# Combine: Year 0 (investment) + Years 1-5 (inflows)
cash_flows = np.concatenate([[initial_investment], cash_inflows])

discount_rate = 0.12   # 12% cost of capital (WACC)

# np.npv() — wait, NumPy removed this in recent versions
# Let's calculate manually (it's easy!)
years = np.arange(0, len(cash_flows))   # 0, 1, 2, 3, 4, 5
discount_factors = 1 / (1 + discount_rate) ** years
present_values = cash_flows * discount_factors
npv = np.sum(present_values)

print('=== NPV Analysis — Machine Purchase ===')
print(f"{'Year':<6} {'Cash Flow':>12} {'Discount Factor':>16} {'Present Value':>14}")
print('-' * 52)
year_labels = ['0 (Now)', '1', '2', '3', '4', '5']
for i, label in enumerate(year_labels):
    print(f"{label:<6} NPR {cash_flows[i]:>11,} {discount_factors[i]:>16.4f} NPR {present_values[i]:>12,.2f}")
print('-' * 52)
print(f"{'NPV':>38} NPR {npv:>12,.2f}")
print()
if npv > 0:
    print(f'Decision: ACCEPT the investment ✓ (NPV is positive — creates value)')
else:
    print(f'Decision: REJECT the investment ✗ (NPV is negative — destroys value)')
```

    === NPV Analysis — Machine Purchase ===
    Year      Cash Flow  Discount Factor  Present Value
    ----------------------------------------------------
    0 (Now) NPR  -1,000,000           1.0000 NPR -1,000,000.00
    1      NPR     250,000           0.8929 NPR   223,214.29
    2      NPR     300,000           0.7972 NPR   239,158.16
    3      NPR     350,000           0.7118 NPR   249,123.09
    4      NPR     320,000           0.6355 NPR   203,365.79
    5      NPR     280,000           0.5674 NPR   158,879.52
    ----------------------------------------------------
                                       NPV NPR    73,740.84
    
    Decision: ACCEPT the investment ✓ (NPV is positive — creates value)



```python
# IRR Calculation using NumPy's polynomial root finding
# IRR is the discount rate that makes NPV = 0

# Project A: Machine Purchase
cf_a = np.array([-1000000, 250000, 300000, 350000, 320000, 280000])

# Project B: Software Implementation
cf_b = np.array([-800000, 400000, 350000, 300000, 250000, 200000])

# IRR = root of the NPV equation — we use np.roots() on the polynomial coefficients
# For a simpler approach, we iterate (IRR estimation)

def estimate_irr(cash_flows, low=0.0, high=1.0, tolerance=1e-6):
    """Estimate IRR using bisection method."""
    for _ in range(1000):
        mid = (low + high) / 2
        years = np.arange(len(cash_flows))
        npv_mid = np.sum(cash_flows / (1 + mid) ** years)
        if abs(npv_mid) < tolerance:
            break
        npv_low = np.sum(cash_flows / (1 + low) ** years)
        if npv_mid * npv_low < 0:
            high = mid
        else:
            low = mid
    return mid * 100   # Return as percentage

irr_a = estimate_irr(cf_a)
irr_b = estimate_irr(cf_b)
hurdle_rate = 12.0   # Company's minimum acceptable return

print('=== IRR Analysis — Capital Budgeting ===')
print(f'Hurdle Rate (WACC):   {hurdle_rate:.1f}%')
print()
print(f'Project A (Machine):  IRR = {irr_a:.2f}%  ', '✓ Accept' if irr_a > hurdle_rate else '✗ Reject')
print(f'Project B (Software): IRR = {irr_b:.2f}%  ', '✓ Accept' if irr_b > hurdle_rate else '✗ Reject')
print()
print(f'Recommendation: Project {"A" if irr_a > irr_b else "B"} has the higher IRR')
```

    === IRR Analysis — Capital Budgeting ===
    Hurdle Rate (WACC):   12.0%
    
    Project A (Machine):  IRR = 14.86%   ✓ Accept
    Project B (Software): IRR = 29.47%   ✓ Accept
    
    Recommendation: Project B has the higher IRR


## Section 16: Practice Exercises

---

#### 🏋️ Exercise 1 — Payroll Processing

You have the following employee salary data (annual CTC in NPR ):
```python
salaries = np.array([420000, 600000, 840000, 1080000, 1440000, 1800000, 2400000, 3600000])
```
Calculate (using NumPy, without loops):
1. Monthly gross salary for each employee
2. EPF @ 10% of annual salary (employee contribution per Nepal Labour Act 2074)
3. SSF contribution @ 1% of gross salary (employee share, Contributory Social Security Fund, Nepal)
4. Net annual take-home for each employee
5. Total payroll cost for the company


```python
import numpy as np

salaries = np.array([420000, 600000, 840000, 1080000, 1440000, 1800000, 2400000, 3600000])

# Write your solution here


```

#### 🏋️ Exercise 2 — Depreciation Schedule (WDV Method)

A company has 5 assets:
```python
asset_names   = ['Building', 'Machinery', 'Computers', 'Vehicles', 'Furniture']
opening_wdv   = np.array([5000000, 2500000, 800000, 1200000, 350000])
dep_rates     = np.array([5, 15, 40, 15, 10])   # % per annum under WDV method
```
Calculate for 3 years:
1. Annual depreciation for each asset
2. Closing WDV after each year
3. Total depreciation charged each year


```python
import numpy as np

asset_names = ['Building', 'Machinery', 'Computers', 'Vehicles', 'Furniture']
opening_wdv = np.array([5000000, 2500000, 800000, 1200000, 350000])
dep_rates   = np.array([5, 15, 40, 15, 10])   # WDV rates

# Write your 3-year WDV schedule here


```

---
### 💡 Solutions


```python
# SOLUTION — Exercise 1: Payroll Processing (Nepal Labour Act)
import numpy as np

salaries = np.array([420000, 600000, 840000, 1080000, 1440000, 1800000, 2400000, 3600000])

monthly_gross = salaries / 12

# EPF: 10% employee contribution (Nepal Labour Act 2074, Section 102)
# No statutory cap in Nepal unlike Indian EPFO — apply to full salary
epf_annual = salaries * 0.10

# SSF (Social Security Fund): 1% of gross salary (employee share, introduced 2076 BS)
ssf_annual = salaries * 0.01

net_takehome = salaries - epf_annual - ssf_annual

print(f"{'Salary':>10} {'Monthly':>10} {'EPF(10%)':>10} {'SSF(1%)':>9} {'Net CTC':>12}")
print('-' * 57)
for i in range(len(salaries)):
    print(f"NPR {salaries[i]:>9,} NPR {monthly_gross[i]:>8,.0f} "
          f"NPR {epf_annual[i]:>8,.0f} NPR {ssf_annual[i]:>7,.0f} "
          f"NPR {net_takehome[i]:>10,}")
print('-' * 57)
print(f"Total payroll cost (employer): NPR {np.sum(salaries):,}")
print(f"Note: Employer also contributes 10% EPF + 20% SSF on top")

```

        Salary    Monthly   EPF(10%)   SSF(1%)      Net CTC
    ---------------------------------------------------------
    NPR   420,000 NPR   35,000 NPR   42,000 NPR   4,200 NPR  373,800.0
    NPR   600,000 NPR   50,000 NPR   60,000 NPR   6,000 NPR  534,000.0
    NPR   840,000 NPR   70,000 NPR   84,000 NPR   8,400 NPR  747,600.0
    NPR 1,080,000 NPR   90,000 NPR  108,000 NPR  10,800 NPR  961,200.0
    NPR 1,440,000 NPR  120,000 NPR  144,000 NPR  14,400 NPR 1,281,600.0
    NPR 1,800,000 NPR  150,000 NPR  180,000 NPR  18,000 NPR 1,602,000.0
    NPR 2,400,000 NPR  200,000 NPR  240,000 NPR  24,000 NPR 2,136,000.0
    NPR 3,600,000 NPR  300,000 NPR  360,000 NPR  36,000 NPR 3,204,000.0
    ---------------------------------------------------------
    Total payroll cost (employer): NPR 12,180,000
    Note: Employer also contributes 10% EPF + 20% SSF on top



```python
# SOLUTION — Exercise 2: WDV Depreciation Schedule
import numpy as np

asset_names = ['Building', 'Machinery', 'Computers', 'Vehicles', 'Furniture']
wdv = np.array([5000000, 2500000, 800000, 1200000, 350000], dtype=float)
dep_rates = np.array([5, 15, 40, 15, 10]) / 100

for year in range(1, 4):
    depreciation = wdv * dep_rates
    closing_wdv  = wdv - depreciation
    print(f'--- Year {year} ---')
    print(f"{'Asset':<12} {'Opening WDV':>13} {'Depreciation':>13} {'Closing WDV':>13}")
    print('-' * 54)
    for i, name in enumerate(asset_names):
        print(f"{name:<12} NPR {wdv[i]:>11,.0f} NPR {depreciation[i]:>11,.0f} NPR {closing_wdv[i]:>11,.0f}")
    print(f"{'TOTAL':<12} NPR {np.sum(wdv):>11,.0f} NPR {np.sum(depreciation):>11,.0f} NPR {np.sum(closing_wdv):>11,.0f}")
    print()
    wdv = closing_wdv   # Closing becomes opening for next year
```

    --- Year 1 ---
    Asset          Opening WDV  Depreciation   Closing WDV
    ------------------------------------------------------
    Building     NPR   5,000,000 NPR     250,000 NPR   4,750,000
    Machinery    NPR   2,500,000 NPR     375,000 NPR   2,125,000
    Computers    NPR     800,000 NPR     320,000 NPR     480,000
    Vehicles     NPR   1,200,000 NPR     180,000 NPR   1,020,000
    Furniture    NPR     350,000 NPR      35,000 NPR     315,000
    TOTAL        NPR   9,850,000 NPR   1,160,000 NPR   8,690,000
    
    --- Year 2 ---
    Asset          Opening WDV  Depreciation   Closing WDV
    ------------------------------------------------------
    Building     NPR   4,750,000 NPR     237,500 NPR   4,512,500
    Machinery    NPR   2,125,000 NPR     318,750 NPR   1,806,250
    Computers    NPR     480,000 NPR     192,000 NPR     288,000
    Vehicles     NPR   1,020,000 NPR     153,000 NPR     867,000
    Furniture    NPR     315,000 NPR      31,500 NPR     283,500
    TOTAL        NPR   8,690,000 NPR     932,750 NPR   7,757,250
    
    --- Year 3 ---
    Asset          Opening WDV  Depreciation   Closing WDV
    ------------------------------------------------------
    Building     NPR   4,512,500 NPR     225,625 NPR   4,286,875
    Machinery    NPR   1,806,250 NPR     270,938 NPR   1,535,312
    Computers    NPR     288,000 NPR     115,200 NPR     172,800
    Vehicles     NPR     867,000 NPR     130,050 NPR     736,950
    Furniture    NPR     283,500 NPR      28,350 NPR     255,150
    TOTAL        NPR   7,757,250 NPR     770,162 NPR   6,987,088
    


---
## 🎉 Module 2 Complete!

### What you've learned
| Concept | Application |
|---------|-------------|
| Creating arrays | Storing financial data efficiently |
| Vectorized operations | Batch VAT, returns, growth calculations |
| Indexing & slicing | Quarterly breakdowns, period analysis |
| Statistical functions | Revenue analytics, risk measurement |
| Boolean indexing | Transaction filtering, audit sampling |
| 2D arrays | Budget matrices, department-wise analysis |
| Financial math | NPV, IRR, portfolio returns |

**Next up → Module 3: Pandas** — Work with real Excel files and financial datasets!

---
*Python for CA Professionals — Module 2: NumPy*
