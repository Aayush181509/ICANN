# Notebook 1 — NumPy Basics for CA Professionals

**Goal:** Learn how to do fast number-crunching on financial data using NumPy.

**You will learn:**

1. What NumPy is and why it is useful
2. How to create an array
3. Doing maths on whole columns of data at once
4. Statistical summaries (sum, mean, min, max)
5. Picking values (indexing & slicing)
6. Filtering data with conditions
7. Working with 2D tables
8. A short mini-project at the end

**Tip for class:** Read each concept, run the code cell, then try the small *Practice* cell that follows.

---

## 1. What is NumPy?

NumPy is a Python library used for **fast numerical work**. Think of it as **Excel formulas applied to entire columns at once** — but in Python, and much faster.

In a normal Python list, if you want to add 13% VAT to 1,000 invoices, you would write a loop. In NumPy you write **one line** and it works on the entire column.


```python
import numpy as np   # 'np' is the standard short name everyone uses
print("NumPy version:", np.__version__)
```

    NumPy version: 2.4.6


## 2. Creating your first array

An **array** in NumPy is like a single column of numbers (or a small table).
We create one from a Python list.


```python
# Five monthly revenue figures (in NPR)
revenue = np.array([1250000, 1380000, 1120000, 1450000, 1620000])
print(revenue)
print("Type:", type(revenue))
```

    [1250000 1380000 1120000 1450000 1620000]
    Type: <class 'numpy.ndarray'>


### Practice 1
Create a NumPy array called `expenses` with these 5 monthly expense figures:
`920000, 980000, 870000, 1050000, 1180000`. Then print it.


```python
# Your turn:
# expenses = ...
# print(expenses)
```

<details><summary>Show solution</summary>


```python
expenses = np.array([920000, 980000, 870000, 1050000, 1180000])
print(expenses)
```

    [ 920000  980000  870000 1050000 1180000]


</details>

## 3. Useful array properties

Every array gives you quick info about itself.


```python
revenue = np.array([1250000, 1380000, 1120000, 1450000, 1620000])

print("shape :", revenue.shape)   # (5,) means 5 items in 1 row
print("size  :", revenue.size)    # total number of items
print("ndim  :", revenue.ndim)    # how many dimensions
print("dtype :", revenue.dtype)   # type of data inside
```

    shape : (5,)
    size  : 5
    ndim  : 1
    dtype : int64


### Practice 2
Create an array of any 7 invoice amounts you like. Print its `shape` and `size`.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
invoices = np.array([45000, 82000, 31500, 97000, 54000, 120000, 63000])
print("shape:", invoices.shape)
print("size :", invoices.size)
```

    shape: (7,)
    size : 7


</details>

## 4. Doing maths on the whole array

This is the **magic of NumPy**. You don't need a loop — just write the operation as if the array was a single number.


```python
amounts = np.array([10000, 25000, 50000, 100000, 75000])

# Add 13% VAT to ALL invoices in one line
vat   = amounts * 0.13
total = amounts + vat

print("Amount :", amounts)
print("VAT    :", vat)
print("Total  :", total)
```

    Amount : [ 10000  25000  50000 100000  75000]
    VAT    : [ 1300.  3250.  6500. 13000.  9750.]
    Total  : [ 11300.  28250.  56500. 113000.  84750.]



```python
# Operations between two arrays — element by element
revenue  = np.array([1250000, 1380000, 1120000, 1450000, 1620000])
expenses = np.array([ 920000,  980000,  870000, 1050000, 1180000])

profit = revenue - expenses
margin = (profit / revenue) * 100   # profit margin in %

print("Profit :", profit)
print("Margin :", margin.round(2), "%")
```

    Profit : [330000 400000 250000 400000 440000]
    Margin : [26.4  28.99 22.32 27.59 27.16] %


### Practice 3
You sold these quantities of a product: `[5, 12, 8, 20, 15]` at a unit price of NPR 450 each.

1. Create the quantity array.
2. Multiply by 450 to get sales amount per row.
3. Add 13% VAT.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
qty   = np.array([5, 12, 8, 20, 15])
sales = qty * 450
vat   = sales * 0.13
print("Sales:", sales)
print("VAT  :", vat)
print("Total:", sales + vat)
```

    Sales: [2250 5400 3600 9000 6750]
    VAT  : [ 292.5  702.   468.  1170.   877.5]
    Total: [ 2542.5  6102.   4068.  10170.   7627.5]


</details>

## 5. Statistical summary functions

These are the "Excel-style" summary functions you'll use every day.

| Function       | What it does                |
|----------------|-----------------------------|
| `np.sum(a)`    | total                       |
| `np.mean(a)`   | average                     |
| `np.median(a)` | middle value                |
| `np.min(a)`    | smallest                    |
| `np.max(a)`    | largest                     |
| `np.std(a)`    | standard deviation (spread) |
| `a.cumsum()`   | running total               |


```python
revenue = np.array([1250000, 1380000, 1120000, 1450000, 1620000,
                    1780000, 1550000, 1420000, 1680000, 1910000,
                    2030000, 2150000])   # full year, 12 months

print("Total annual revenue  : NPR", np.sum(revenue))
print("Average monthly       : NPR", np.mean(revenue).round(0))
print("Best month            : NPR", np.max(revenue))
print("Worst month           : NPR", np.min(revenue))
print("Standard deviation    : NPR", np.std(revenue).round(0))
print("Running total (YTD)   :", revenue.cumsum())
```

    Total annual revenue  : NPR 19340000
    Average monthly       : NPR 1611667.0
    Best month            : NPR 2150000
    Worst month           : NPR 1120000
    Standard deviation    : NPR 299968.0
    Running total (YTD)   : [ 1250000  2630000  3750000  5200000  6820000  8600000 10150000 11570000
     13250000 15160000 17190000 19340000]


### Practice 4
For these 6 quarterly expense figures:
`[820000, 950000, 1080000, 1190000, 1310000, 1490000]`

Find: total, average, max, min, and the running total (`cumsum`).


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
exp = np.array([820000, 950000, 1080000, 1190000, 1310000, 1490000])
print("Total  :", np.sum(exp))
print("Average:", np.mean(exp))
print("Max    :", np.max(exp))
print("Min    :", np.min(exp))
print("Cumsum :", exp.cumsum())
```

    Total  : 6840000
    Average: 1140000.0
    Max    : 1490000
    Min    : 820000
    Cumsum : [ 820000 1770000 2850000 4040000 5350000 6840000]


</details>

## 6. Picking values — indexing & slicing

Position numbers (called **index**) in Python start from **0**, not 1.

```
revenue:  [1250000, 1380000, 1120000, 1450000, 1620000, 1780000, ...]
index  :     0        1        2        3        4        5
```


```python
months = ["Shrawan","Bhadra","Ashwin","Kartik","Mangsir","Poush",
          "Magh","Falgun","Chaitra","Baishakh","Jestha","Ashadh"]
revenue = np.array([1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
                    1550000, 1420000, 1680000, 1910000, 2030000, 2150000])

print("First month (Shrawan):", revenue[0])
print("Last  month (Ashadh) :", revenue[-1])
print("3rd month  (Ashwin)  :", revenue[2])

# Slicing  →  array[start : end]   (end is NOT included)
q1 = revenue[0:3]      # months 1,2,3
q4 = revenue[9:12]     # months 10,11,12

print("Q1 :", q1, "→ total NPR", q1.sum())
print("Q4 :", q4, "→ total NPR", q4.sum())
```

    First month (Shrawan): 1250000
    Last  month (Ashadh) : 2150000
    3rd month  (Ashwin)  : 1120000
    Q1 : [1250000 1380000 1120000] → total NPR 3750000
    Q4 : [1910000 2030000 2150000] → total NPR 6090000


### Practice 5
Using the `revenue` array above:

1. Print the revenue for **Poush** (6th month, so index 5).
2. Print the **last 3 months** using slicing.
3. Find the average of Q2 (Kartik, Mangsir, Poush → index 3 to 6).


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print("Poush       :", revenue[5])
print("Last 3      :", revenue[-3:])
print("Q2 average  :", revenue[3:6].mean())
```

    Poush       : 1780000
    Last 3      : [1910000 2030000 2150000]
    Q2 average  : 1616666.6666666667


</details>

## 7. Filtering data with conditions

This is like **AutoFilter in Excel** — but on entire columns. You write a condition and NumPy gives you back only the values that match.


```python
invoices = np.array([45000, 182000, 31500, 97000, 254000, 18000,
                     320000, 67000, 145000, 9500, 88000, 410000])

# Step 1: condition gives True/False for each element
mask = invoices > 100000
print("Mask :", mask)

# Step 2: use the mask to pick values
big = invoices[mask]
print("Invoices > NPR 1 lakh:", big)
print("How many?", big.size)
print("Their total: NPR", big.sum())
```

    Mask : [False  True False False  True False  True False  True False False  True]
    Invoices > NPR 1 lakh: [182000 254000 320000 145000 410000]
    How many? 5
    Their total: NPR 1311000



```python
# You can combine conditions with & (and) and | (or)
audit_range = invoices[(invoices >= 50000) & (invoices <= 200000)]
print("Audit sample (NPR 50K to 2L):", audit_range)
```

    Audit sample (NPR 50K to 2L): [182000  97000  67000 145000  88000]


### Practice 6
From the `invoices` array above, find:

1. All invoices **below NPR 20,000** (small / cash-style).
2. All invoices **above NPR 3 lakh** (high value).
3. How many invoices are between NPR 50,000 and NPR 1 lakh.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print("Below 20K  :", invoices[invoices < 20000])
print("Above 3L   :", invoices[invoices > 300000])
mid = invoices[(invoices >= 50000) & (invoices <= 100000)]
print("Mid count  :", mid.size)
```

    Below 20K  : [18000  9500]
    Above 3L   : [320000 410000]
    Mid count  : 3


</details>

## 8. 2D arrays — a small table

A 2D array is a table with **rows** and **columns**. Useful for things like *months × departments*.


```python
# Rows = Quarters, Columns = Departments
#                    Audit    Tax  Advisory  Finance
budget = np.array([[500000, 350000, 220000, 180000],   # Q1
                   [520000, 360000, 230000, 195000],   # Q2
                   [480000, 340000, 215000, 185000],   # Q3
                   [560000, 390000, 245000, 210000]])  # Q4

print("Shape:", budget.shape)        # (4 rows, 4 cols)
print("Q1 Audit  :", budget[0, 0])    # row 0, col 0
print("Q3 Finance:", budget[2, 3])

# Whole row → all departments in Q2
print("Q2 row    :", budget[1, :])

# Whole column → Audit across all quarters
print("Audit col :", budget[:, 0])
```

    Shape: (4, 4)
    Q1 Audit  : 500000
    Q3 Finance: 185000
    Q2 row    : [520000 360000 230000 195000]
    Audit col : [500000 520000 480000 560000]



```python
# axis=0 → sum DOWN each column     (yearly total per dept)
# axis=1 → sum ACROSS each row      (total per quarter)
print("By dept   :", budget.sum(axis=0))
print("By quarter:", budget.sum(axis=1))
print("Grand     :", budget.sum())
```

    By dept   : [2060000 1440000  910000  770000]
    By quarter: [1250000 1305000 1220000 1405000]
    Grand     : 5180000


### Practice 7
Given the `budget` table above:

1. Print the **Tax department's** budget for all four quarters.
2. Print the **average** of Q4 across all departments.
3. Calculate the **total annual budget**.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print("Tax   :", budget[:, 1])
print("Q4 avg:", budget[3, :].mean())
print("Grand :", budget.sum())
```

    Tax   : [350000 360000 340000 390000]
    Q4 avg: 351250.0
    Grand : 5180000


</details>

## 9. Quick array creators

Sometimes you don't have a list of values — you need to **generate** one.

| Code                         | Result                       |
|------------------------------|------------------------------|
| `np.zeros(5)`                | `[0, 0, 0, 0, 0]`            |
| `np.ones(4)`                 | `[1, 1, 1, 1]`               |
| `np.arange(1, 6)`            | `[1, 2, 3, 4, 5]`            |
| `np.arange(0, 20, 5)`        | `[0, 5, 10, 15]`             |
| `np.linspace(0, 10, 5)`      | 5 equally-spaced numbers     |


```python
print("zeros   :", np.zeros(5))
print("ones    :", np.ones(4))
print("arange  :", np.arange(1, 13))     # months 1 to 12
print("step 5  :", np.arange(0, 25, 5))
print("linspace:", np.linspace(6, 12, 5)) # 5 interest rates between 6% and 12%
```

    zeros   : [0. 0. 0. 0. 0.]
    ones    : [1. 1. 1. 1.]
    arange  : [ 1  2  3  4  5  6  7  8  9 10 11 12]
    step 5  : [ 0  5 10 15 20]
    linspace: [ 6.   7.5  9.  10.5 12. ]


### Practice 8
1. Create an array of all integers from **1 to 12** (representing months).
2. Create an array of **5 interest rates** equally spaced between **8% and 16%**.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print("Months:", np.arange(1, 13))
print("Rates :", np.linspace(8, 16, 5))
```

    Months: [ 1  2  3  4  5  6  7  8  9 10 11 12]
    Rates : [ 8. 10. 12. 14. 16.]


</details>

## 10. Mini-Project — Annual P&L Summary

You have monthly revenue and expense figures for FY 2081-82 BS. Using only NumPy:

1. Calculate **monthly profit** (revenue − expenses).
2. Calculate **profit margin %** for each month.
3. Find the **best and worst month** (highest/lowest profit).
4. Calculate **total annual revenue, total expenses, total profit**.
5. Identify **how many months had profit margin above 25%**.


```python
months = np.array(["Shrawan","Bhadra","Ashwin","Kartik","Mangsir","Poush",
                   "Magh","Falgun","Chaitra","Baishakh","Jestha","Ashadh"])

revenue = np.array([1250000, 1380000, 1120000, 1450000, 1620000, 1780000,
                    1550000, 1420000, 1680000, 1910000, 2030000, 2150000])

expenses = np.array([ 920000,  980000,  870000, 1050000, 1180000, 1250000,
                     1100000, 1020000, 1190000, 1320000, 1410000, 1490000])

# Your code here
```

<details><summary>Show solution</summary>


```python
profit  = revenue - expenses
margin  = (profit / revenue) * 100

print("Monthly profit :", profit)
print("Margin %       :", margin.round(1))
print()
print("Best month  :", months[np.argmax(profit)], "→ NPR", profit.max())
print("Worst month :", months[np.argmin(profit)], "→ NPR", profit.min())
print()
print("Total revenue  : NPR", revenue.sum())
print("Total expenses : NPR", expenses.sum())
print("Total profit   : NPR", profit.sum())
print()
print("Months with margin > 25%:", (margin > 25).sum())
```

    Monthly profit : [330000 400000 250000 400000 440000 530000 450000 400000 490000 590000
     620000 660000]
    Margin %       : [26.4 29.  22.3 27.6 27.2 29.8 29.  28.2 29.2 30.9 30.5 30.7]
    
    Best month  : Ashadh → NPR 660000
    Worst month : Ashwin → NPR 250000
    
    Total revenue  : NPR 19340000
    Total expenses : NPR 13780000
    Total profit   : NPR 5560000
    
    Months with margin > 25%: 11


</details>

---
### What's next?
You now know enough NumPy to do fast number-crunching on financial data.
In the next notebook (`02_Pandas_Basics`) we will use **Pandas**, which is built on top of NumPy and lets us work with **labelled tables** — almost exactly like Excel sheets.
