# Notebook 2 — Pandas Basics for CA Professionals

**Goal:** Work with real Excel-style data in Python using Pandas.

**You will learn:**

1. What Pandas is and how it relates to Excel
2. Series and DataFrame — the two main objects
3. Loading a CSV file and looking at it
4. Selecting columns and filtering rows
5. Adding new calculated columns (like a new Excel column)
6. Sorting data
7. GroupBy — like a Pivot Table
8. Saving your results back to Excel/CSV
9. A short mini-project at the end

> Throughout the notebook we will use Nepali invoice, sales and payroll data placed in the `data/` folder beside this notebook.

---

## 1. What is Pandas?

Pandas is a Python library that gives you a **DataFrame** — basically an Excel sheet inside Python.

| Excel             | Pandas        |
|-------------------|---------------|
| Workbook          | (your script) |
| Worksheet         | `DataFrame`   |
| Column            | `Series`      |
| Cell              | one value     |
| Pivot Table       | `groupby()`   |
| AutoFilter        | boolean mask  |


```python
import pandas as pd
import numpy as np
print("Pandas version:", pd.__version__)
```

    Pandas version: 3.0.3


## 2. A Series — one column of data

A `Series` is a single column with a **label** for each row (the **index**).


```python
monthly = pd.Series(
    data=[1250000, 1380000, 1120000, 1450000, 1620000],
    index=["Shrawan", "Bhadra", "Ashwin", "Kartik", "Mangsir"],
    name="Revenue_NPR",
)
print(monthly)
print()
print("Total :", monthly.sum())
print("Mean  :", monthly.mean())
```

    Shrawan    1250000
    Bhadra     1380000
    Ashwin     1120000
    Kartik     1450000
    Mangsir    1620000
    Name: Revenue_NPR, dtype: int64
    
    Total : 6820000
    Mean  : 1364000.0


### Practice 1

Create a Series called `expenses` for these 5 months:
- Shrawan: 920000, Bhadra: 980000, Ashwin: 870000, Kartik: 1050000, Mangsir: 1180000

Then print the **total** and the **highest** expense.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
expenses = pd.Series(
    [920000, 980000, 870000, 1050000, 1180000],
    index=["Shrawan","Bhadra","Ashwin","Kartik","Mangsir"],
    name="Expense_NPR",
)
print(expenses)
print("Total :", expenses.sum())
print("Max   :", expenses.max())
```

    Shrawan     920000
    Bhadra      980000
    Ashwin      870000
    Kartik     1050000
    Mangsir    1180000
    Name: Expense_NPR, dtype: int64
    Total : 5000000
    Max   : 1180000


</details>

## 3. A DataFrame — the full table

A `DataFrame` is several Series joined together. Each column has a name; each row has an index.


```python
df = pd.DataFrame({
    "Month":   ["Shrawan", "Bhadra", "Ashwin", "Kartik", "Mangsir"],
    "Revenue": [1250000, 1380000, 1120000, 1450000, 1620000],
    "Expense": [ 920000,  980000,  870000, 1050000, 1180000],
})
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Month</th>
      <th>Revenue</th>
      <th>Expense</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Shrawan</td>
      <td>1250000</td>
      <td>920000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bhadra</td>
      <td>1380000</td>
      <td>980000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ashwin</td>
      <td>1120000</td>
      <td>870000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Kartik</td>
      <td>1450000</td>
      <td>1050000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mangsir</td>
      <td>1620000</td>
      <td>1180000</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 2
Create a small DataFrame with 4 employees of your choice. Columns:
`Name`, `Department`, `Salary`. Print the DataFrame.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
staff = pd.DataFrame({
    "Name":       ["Ramesh", "Sita", "Hari", "Anita"],
    "Department": ["Audit", "Tax", "Audit", "Advisory"],
    "Salary":     [55000, 72000, 48000, 95000],
})
print(staff)
```

         Name Department  Salary
    0  Ramesh      Audit   55000
    1    Sita        Tax   72000
    2    Hari      Audit   48000
    3   Anita   Advisory   95000


</details>

## 4. Loading data from a CSV file

In real life you don't type the data — you read it from a file. We have a folder called `data/` with several Nepali financial datasets already prepared.


```python
invoices = pd.read_csv("data/invoices.csv")
invoices.head()        # show first 5 rows
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Date</th>
      <th>Customer</th>
      <th>City</th>
      <th>Product</th>
      <th>Quantity</th>
      <th>Unit_Price</th>
      <th>Amount_NPR</th>
      <th>VAT_NPR</th>
      <th>Total_NPR</th>
      <th>Payment_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>INV-20810001</td>
      <td>2024-07-16</td>
      <td>Janakpur Wholesale</td>
      <td>Birgunj</td>
      <td>Food</td>
      <td>39</td>
      <td>1219.0</td>
      <td>47541.0</td>
      <td>6180.33</td>
      <td>53721.33</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>1</th>
      <td>INV-20810002</td>
      <td>2024-07-18</td>
      <td>Kathmandu Distributors</td>
      <td>Kathmandu</td>
      <td>Food</td>
      <td>27</td>
      <td>1418.0</td>
      <td>38286.0</td>
      <td>4977.18</td>
      <td>43263.18</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>2</th>
      <td>INV-20810003</td>
      <td>2024-07-20</td>
      <td>Biratnagar Enterprise</td>
      <td>Butwal</td>
      <td>Stationery</td>
      <td>10</td>
      <td>1309.0</td>
      <td>13090.0</td>
      <td>1701.70</td>
      <td>14791.70</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>3</th>
      <td>INV-20810004</td>
      <td>2024-07-22</td>
      <td>Pokhara Mart</td>
      <td>Birgunj</td>
      <td>Food</td>
      <td>26</td>
      <td>5501.0</td>
      <td>143026.0</td>
      <td>18593.38</td>
      <td>161619.38</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>4</th>
      <td>INV-20810005</td>
      <td>2024-07-24</td>
      <td>Janakpur Wholesale</td>
      <td>Bhaktapur</td>
      <td>Food</td>
      <td>19</td>
      <td>1669.0</td>
      <td>31711.0</td>
      <td>4122.43</td>
      <td>35833.43</td>
      <td>Paid</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 3
Load the file `data/monthly_sales.csv` into a DataFrame called `sales` and show the first 5 rows.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
sales = pd.read_csv("data/monthly_sales.csv")
sales.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Month</th>
      <th>Revenue_NPR</th>
      <th>Expense_NPR</th>
      <th>Units_Sold</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Shrawan</td>
      <td>1250000</td>
      <td>920000</td>
      <td>420</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bhadra</td>
      <td>1380000</td>
      <td>980000</td>
      <td>465</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ashwin</td>
      <td>1120000</td>
      <td>870000</td>
      <td>380</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Kartik</td>
      <td>1450000</td>
      <td>1050000</td>
      <td>498</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mangsir</td>
      <td>1620000</td>
      <td>1180000</td>
      <td>540</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 5. Quick inspection — get to know your data

| Code              | What it does                            |
|-------------------|-----------------------------------------|
| `df.head(n)`      | first n rows                            |
| `df.tail(n)`      | last n rows                             |
| `df.shape`        | (rows, columns)                         |
| `df.columns`      | column names                            |
| `df.dtypes`       | data type of each column                |
| `df.info()`       | full overview                           |
| `df.describe()`   | quick statistics for numeric columns    |


```python
print("Shape   :", invoices.shape)
print("Columns :", list(invoices.columns))
print()
invoices.info()
```

    Shape   : (200, 11)
    Columns : ['Invoice_No', 'Date', 'Customer', 'City', 'Product', 'Quantity', 'Unit_Price', 'Amount_NPR', 'VAT_NPR', 'Total_NPR', 'Payment_Status']
    
    <class 'pandas.DataFrame'>
    RangeIndex: 200 entries, 0 to 199
    Data columns (total 11 columns):
     #   Column          Non-Null Count  Dtype  
    ---  ------          --------------  -----  
     0   Invoice_No      200 non-null    str    
     1   Date            200 non-null    str    
     2   Customer        200 non-null    str    
     3   City            200 non-null    str    
     4   Product         200 non-null    str    
     5   Quantity        200 non-null    int64  
     6   Unit_Price      200 non-null    float64
     7   Amount_NPR      200 non-null    float64
     8   VAT_NPR         200 non-null    float64
     9   Total_NPR       200 non-null    float64
     10  Payment_Status  200 non-null    str    
    dtypes: float64(4), int64(1), str(6)
    memory usage: 17.3 KB



```python
invoices.describe()    # statistics for all numeric columns
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Quantity</th>
      <th>Unit_Price</th>
      <th>Amount_NPR</th>
      <th>VAT_NPR</th>
      <th>Total_NPR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>200.000000</td>
      <td>200.000000</td>
      <td>200.000000</td>
      <td>200.000000</td>
      <td>200.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>24.355000</td>
      <td>4012.410000</td>
      <td>93674.160000</td>
      <td>12177.640800</td>
      <td>105851.800800</td>
    </tr>
    <tr>
      <th>std</th>
      <td>14.109371</td>
      <td>2314.909302</td>
      <td>81983.202634</td>
      <td>10657.816342</td>
      <td>92641.018976</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>318.000000</td>
      <td>891.000000</td>
      <td>115.830000</td>
      <td>1006.830000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>12.750000</td>
      <td>1863.250000</td>
      <td>33018.000000</td>
      <td>4292.340000</td>
      <td>37310.340000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>25.000000</td>
      <td>3785.500000</td>
      <td>67947.500000</td>
      <td>8833.175000</td>
      <td>76780.675000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>36.000000</td>
      <td>5984.500000</td>
      <td>135046.750000</td>
      <td>17556.077500</td>
      <td>152602.827500</td>
    </tr>
    <tr>
      <th>max</th>
      <td>49.000000</td>
      <td>8416.000000</td>
      <td>387590.000000</td>
      <td>50386.700000</td>
      <td>437976.700000</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 4
Load `data/loans.csv` into a DataFrame called `loans`. Then:

1. Print its **shape**.
2. Show its **column names**.
3. Show `describe()` for the numeric columns.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
loans = pd.read_csv("data/loans.csv")
print("Shape   :", loans.shape)
print("Columns :", list(loans.columns))
loans.describe()
```

    Shape   : (300, 10)
    Columns : ['Loan_ID', 'Customer', 'Loan_Amount', 'Tenure_Months', 'Interest_Rate', 'Annual_Income', 'Credit_Score', 'Has_Collateral', 'Sector', 'Defaulted']





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Loan_Amount</th>
      <th>Tenure_Months</th>
      <th>Interest_Rate</th>
      <th>Annual_Income</th>
      <th>Credit_Score</th>
      <th>Defaulted</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>3.000000e+02</td>
      <td>300.000000</td>
      <td>300.000000</td>
      <td>3.000000e+02</td>
      <td>300.000000</td>
      <td>300.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>9.315000e+05</td>
      <td>49.720000</td>
      <td>11.916633</td>
      <td>6.734000e+05</td>
      <td>581.816667</td>
      <td>0.413333</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.111396e+06</td>
      <td>37.531547</td>
      <td>2.339863</td>
      <td>6.099118e+05</td>
      <td>158.994109</td>
      <td>0.493254</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000e+05</td>
      <td>12.000000</td>
      <td>8.040000</td>
      <td>1.800000e+05</td>
      <td>300.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>2.500000e+05</td>
      <td>24.000000</td>
      <td>9.882500</td>
      <td>3.600000e+05</td>
      <td>443.500000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>5.000000e+05</td>
      <td>36.000000</td>
      <td>11.830000</td>
      <td>3.600000e+05</td>
      <td>602.500000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1.000000e+06</td>
      <td>60.000000</td>
      <td>13.947500</td>
      <td>6.000000e+05</td>
      <td>718.500000</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>5.000000e+06</td>
      <td>120.000000</td>
      <td>15.920000</td>
      <td>2.400000e+06</td>
      <td>849.000000</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 6. Selecting columns

You can pick a single column (gives a Series), or several columns (gives a DataFrame).


```python
# Single column → Series
invoices["Amount_NPR"].head()
```




    0     47541.0
    1     38286.0
    2     13090.0
    3    143026.0
    4     31711.0
    Name: Amount_NPR, dtype: float64




```python
# Several columns → DataFrame
invoices[["Customer", "City", "Total_NPR"]].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Customer</th>
      <th>City</th>
      <th>Total_NPR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Janakpur Wholesale</td>
      <td>Birgunj</td>
      <td>53721.33</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Kathmandu Distributors</td>
      <td>Kathmandu</td>
      <td>43263.18</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Biratnagar Enterprise</td>
      <td>Butwal</td>
      <td>14791.70</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Pokhara Mart</td>
      <td>Birgunj</td>
      <td>161619.38</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Janakpur Wholesale</td>
      <td>Bhaktapur</td>
      <td>35833.43</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 5
From `invoices`, show only the columns `Invoice_No`, `Product`, `Quantity`, `Amount_NPR` — first 10 rows.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
invoices[["Invoice_No","Product","Quantity","Amount_NPR"]].head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Product</th>
      <th>Quantity</th>
      <th>Amount_NPR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>INV-20810001</td>
      <td>Food</td>
      <td>39</td>
      <td>47541.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>INV-20810002</td>
      <td>Food</td>
      <td>27</td>
      <td>38286.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>INV-20810003</td>
      <td>Stationery</td>
      <td>10</td>
      <td>13090.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>INV-20810004</td>
      <td>Food</td>
      <td>26</td>
      <td>143026.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>INV-20810005</td>
      <td>Food</td>
      <td>19</td>
      <td>31711.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>INV-20810006</td>
      <td>Cosmetics</td>
      <td>39</td>
      <td>118404.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>INV-20810007</td>
      <td>Food</td>
      <td>3</td>
      <td>22914.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>INV-20810008</td>
      <td>Textile</td>
      <td>45</td>
      <td>184860.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>INV-20810009</td>
      <td>Hardware</td>
      <td>13</td>
      <td>74412.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>INV-20810010</td>
      <td>Electronics</td>
      <td>28</td>
      <td>44492.0</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 7. Filtering rows — the AutoFilter of Pandas

Just like `np.array[condition]`, but on a whole table.


```python
# Invoices with amount over NPR 1 lakh
big = invoices[invoices["Amount_NPR"] > 100000]
print("Found", len(big), "high-value invoices")
big.head()
```

    Found 75 high-value invoices





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Date</th>
      <th>Customer</th>
      <th>City</th>
      <th>Product</th>
      <th>Quantity</th>
      <th>Unit_Price</th>
      <th>Amount_NPR</th>
      <th>VAT_NPR</th>
      <th>Total_NPR</th>
      <th>Payment_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3</th>
      <td>INV-20810004</td>
      <td>2024-07-22</td>
      <td>Pokhara Mart</td>
      <td>Birgunj</td>
      <td>Food</td>
      <td>26</td>
      <td>5501.0</td>
      <td>143026.0</td>
      <td>18593.38</td>
      <td>161619.38</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>5</th>
      <td>INV-20810006</td>
      <td>2024-07-26</td>
      <td>Birgunj Cargo</td>
      <td>Pokhara</td>
      <td>Cosmetics</td>
      <td>39</td>
      <td>3036.0</td>
      <td>118404.0</td>
      <td>15392.52</td>
      <td>133796.52</td>
      <td>Pending</td>
    </tr>
    <tr>
      <th>7</th>
      <td>INV-20810008</td>
      <td>2024-07-30</td>
      <td>Janakpur Wholesale</td>
      <td>Bhaktapur</td>
      <td>Textile</td>
      <td>45</td>
      <td>4108.0</td>
      <td>184860.0</td>
      <td>24031.80</td>
      <td>208891.80</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>13</th>
      <td>INV-20810014</td>
      <td>2024-08-11</td>
      <td>Annapurna Stores</td>
      <td>Pokhara</td>
      <td>Stationery</td>
      <td>41</td>
      <td>2476.0</td>
      <td>101516.0</td>
      <td>13197.08</td>
      <td>114713.08</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>19</th>
      <td>INV-20810020</td>
      <td>2024-08-23</td>
      <td>Everest Suppliers</td>
      <td>Nepalgunj</td>
      <td>Cosmetics</td>
      <td>49</td>
      <td>3192.0</td>
      <td>156408.0</td>
      <td>20333.04</td>
      <td>176741.04</td>
      <td>Overdue</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Combine conditions with & (and) and | (or) — wrap each in ()
overdue_big = invoices[(invoices["Payment_Status"] == "Overdue") &
                       (invoices["Amount_NPR"] > 50000)]
overdue_big.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Date</th>
      <th>Customer</th>
      <th>City</th>
      <th>Product</th>
      <th>Quantity</th>
      <th>Unit_Price</th>
      <th>Amount_NPR</th>
      <th>VAT_NPR</th>
      <th>Total_NPR</th>
      <th>Payment_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>7</th>
      <td>INV-20810008</td>
      <td>2024-07-30</td>
      <td>Janakpur Wholesale</td>
      <td>Bhaktapur</td>
      <td>Textile</td>
      <td>45</td>
      <td>4108.0</td>
      <td>184860.0</td>
      <td>24031.80</td>
      <td>208891.80</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>8</th>
      <td>INV-20810009</td>
      <td>2024-08-01</td>
      <td>Biratnagar Enterprise</td>
      <td>Hetauda</td>
      <td>Hardware</td>
      <td>13</td>
      <td>5724.0</td>
      <td>74412.0</td>
      <td>9673.56</td>
      <td>84085.56</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>18</th>
      <td>INV-20810019</td>
      <td>2024-08-21</td>
      <td>Lumbini Imports</td>
      <td>Lalitpur</td>
      <td>Stationery</td>
      <td>28</td>
      <td>1873.0</td>
      <td>52444.0</td>
      <td>6817.72</td>
      <td>59261.72</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>19</th>
      <td>INV-20810020</td>
      <td>2024-08-23</td>
      <td>Everest Suppliers</td>
      <td>Nepalgunj</td>
      <td>Cosmetics</td>
      <td>49</td>
      <td>3192.0</td>
      <td>156408.0</td>
      <td>20333.04</td>
      <td>176741.04</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>26</th>
      <td>INV-20810027</td>
      <td>2024-09-06</td>
      <td>Birgunj Cargo</td>
      <td>Bhaktapur</td>
      <td>Electronics</td>
      <td>32</td>
      <td>7444.0</td>
      <td>238208.0</td>
      <td>30967.04</td>
      <td>269175.04</td>
      <td>Overdue</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 6
From `invoices`:

1. Find all invoices from the city **"Kathmandu"**.
2. Find all **"Pending"** invoices above NPR 30,000.
3. Count how many invoices have `Quantity` > 30.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
ktm = invoices[invoices["City"] == "Kathmandu"]
pending = invoices[(invoices["Payment_Status"] == "Pending") &
                   (invoices["Amount_NPR"] > 30000)]
print("KTM invoices    :", len(ktm))
print("Pending > 30K   :", len(pending))
print("Qty > 30 count  :", (invoices["Quantity"] > 30).sum())
```

    KTM invoices    : 26
    Pending > 30K   : 31
    Qty > 30 count  : 73


</details>

## 8. Sorting

`sort_values(by="ColumnName")` is your friend — just like Data → Sort in Excel.


```python
# Top 5 highest invoices
top5 = invoices.sort_values("Total_NPR", ascending=False).head(5)
top5[["Invoice_No","Customer","Total_NPR","Payment_Status"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Customer</th>
      <th>Total_NPR</th>
      <th>Payment_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>96</th>
      <td>INV-20810097</td>
      <td>Nepalgunj Goods</td>
      <td>437976.70</td>
      <td>Pending</td>
    </tr>
    <tr>
      <th>132</th>
      <td>INV-20810133</td>
      <td>Annapurna Stores</td>
      <td>406037.25</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>27</th>
      <td>INV-20810028</td>
      <td>Annapurna Stores</td>
      <td>398613.15</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>163</th>
      <td>INV-20810164</td>
      <td>Kathmandu Distributors</td>
      <td>352471.86</td>
      <td>Pending</td>
    </tr>
    <tr>
      <th>154</th>
      <td>INV-20810155</td>
      <td>Nepalgunj Goods</td>
      <td>346756.32</td>
      <td>Pending</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 7
Sort `invoices` by `Quantity` (largest first) and show the top 10.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
invoices.sort_values("Quantity", ascending=False).head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Invoice_No</th>
      <th>Date</th>
      <th>Customer</th>
      <th>City</th>
      <th>Product</th>
      <th>Quantity</th>
      <th>Unit_Price</th>
      <th>Amount_NPR</th>
      <th>VAT_NPR</th>
      <th>Total_NPR</th>
      <th>Payment_Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>136</th>
      <td>INV-20810137</td>
      <td>2025-04-14</td>
      <td>Nepalgunj Goods</td>
      <td>Lalitpur</td>
      <td>Stationery</td>
      <td>49</td>
      <td>4947.0</td>
      <td>242403.0</td>
      <td>31512.39</td>
      <td>273915.39</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>41</th>
      <td>INV-20810042</td>
      <td>2024-10-06</td>
      <td>Everest Suppliers</td>
      <td>Bhaktapur</td>
      <td>Electronics</td>
      <td>49</td>
      <td>2258.0</td>
      <td>110642.0</td>
      <td>14383.46</td>
      <td>125025.46</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>96</th>
      <td>INV-20810097</td>
      <td>2025-01-24</td>
      <td>Nepalgunj Goods</td>
      <td>Biratnagar</td>
      <td>Hardware</td>
      <td>49</td>
      <td>7910.0</td>
      <td>387590.0</td>
      <td>50386.70</td>
      <td>437976.70</td>
      <td>Pending</td>
    </tr>
    <tr>
      <th>19</th>
      <td>INV-20810020</td>
      <td>2024-08-23</td>
      <td>Everest Suppliers</td>
      <td>Nepalgunj</td>
      <td>Cosmetics</td>
      <td>49</td>
      <td>3192.0</td>
      <td>156408.0</td>
      <td>20333.04</td>
      <td>176741.04</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>103</th>
      <td>INV-20810104</td>
      <td>2025-02-07</td>
      <td>Janakpur Wholesale</td>
      <td>Biratnagar</td>
      <td>Food</td>
      <td>49</td>
      <td>3702.0</td>
      <td>181398.0</td>
      <td>23581.74</td>
      <td>204979.74</td>
      <td>Overdue</td>
    </tr>
    <tr>
      <th>196</th>
      <td>INV-20810197</td>
      <td>2025-08-12</td>
      <td>Pokhara Mart</td>
      <td>Lalitpur</td>
      <td>Hardware</td>
      <td>48</td>
      <td>1666.0</td>
      <td>79968.0</td>
      <td>10395.84</td>
      <td>90363.84</td>
      <td>Pending</td>
    </tr>
    <tr>
      <th>76</th>
      <td>INV-20810077</td>
      <td>2024-12-15</td>
      <td>Nepalgunj Goods</td>
      <td>Kathmandu</td>
      <td>Textile</td>
      <td>48</td>
      <td>1000.0</td>
      <td>48000.0</td>
      <td>6240.00</td>
      <td>54240.00</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>154</th>
      <td>INV-20810155</td>
      <td>2025-05-20</td>
      <td>Nepalgunj Goods</td>
      <td>Hetauda</td>
      <td>Food</td>
      <td>48</td>
      <td>6393.0</td>
      <td>306864.0</td>
      <td>39892.32</td>
      <td>346756.32</td>
      <td>Pending</td>
    </tr>
    <tr>
      <th>111</th>
      <td>INV-20810112</td>
      <td>2025-02-23</td>
      <td>Annapurna Stores</td>
      <td>Lalitpur</td>
      <td>Cosmetics</td>
      <td>48</td>
      <td>4168.0</td>
      <td>200064.0</td>
      <td>26008.32</td>
      <td>226072.32</td>
      <td>Paid</td>
    </tr>
    <tr>
      <th>28</th>
      <td>INV-20810029</td>
      <td>2024-09-10</td>
      <td>Janakpur Wholesale</td>
      <td>Hetauda</td>
      <td>Hardware</td>
      <td>47</td>
      <td>660.0</td>
      <td>31020.0</td>
      <td>4032.60</td>
      <td>35052.60</td>
      <td>Paid</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 9. Creating new columns

You can build new columns from existing ones — like adding a new column with an Excel formula.


```python
sales = pd.read_csv("data/monthly_sales.csv")

# New calculated columns
sales["Profit"]      = sales["Revenue_NPR"] - sales["Expense_NPR"]
sales["Margin_pct"]  = (sales["Profit"] / sales["Revenue_NPR"] * 100).round(2)
sales["VAT_NPR"]     = sales["Revenue_NPR"] * 0.13

sales
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Month</th>
      <th>Revenue_NPR</th>
      <th>Expense_NPR</th>
      <th>Units_Sold</th>
      <th>Profit</th>
      <th>Margin_pct</th>
      <th>VAT_NPR</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Shrawan</td>
      <td>1250000</td>
      <td>920000</td>
      <td>420</td>
      <td>330000</td>
      <td>26.40</td>
      <td>162500.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bhadra</td>
      <td>1380000</td>
      <td>980000</td>
      <td>465</td>
      <td>400000</td>
      <td>28.99</td>
      <td>179400.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ashwin</td>
      <td>1120000</td>
      <td>870000</td>
      <td>380</td>
      <td>250000</td>
      <td>22.32</td>
      <td>145600.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Kartik</td>
      <td>1450000</td>
      <td>1050000</td>
      <td>498</td>
      <td>400000</td>
      <td>27.59</td>
      <td>188500.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mangsir</td>
      <td>1620000</td>
      <td>1180000</td>
      <td>540</td>
      <td>440000</td>
      <td>27.16</td>
      <td>210600.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Poush</td>
      <td>1780000</td>
      <td>1250000</td>
      <td>605</td>
      <td>530000</td>
      <td>29.78</td>
      <td>231400.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Magh</td>
      <td>1550000</td>
      <td>1100000</td>
      <td>515</td>
      <td>450000</td>
      <td>29.03</td>
      <td>201500.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Falgun</td>
      <td>1420000</td>
      <td>1020000</td>
      <td>478</td>
      <td>400000</td>
      <td>28.17</td>
      <td>184600.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Chaitra</td>
      <td>1680000</td>
      <td>1190000</td>
      <td>560</td>
      <td>490000</td>
      <td>29.17</td>
      <td>218400.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Baishakh</td>
      <td>1910000</td>
      <td>1320000</td>
      <td>640</td>
      <td>590000</td>
      <td>30.89</td>
      <td>248300.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Jestha</td>
      <td>2030000</td>
      <td>1410000</td>
      <td>690</td>
      <td>620000</td>
      <td>30.54</td>
      <td>263900.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Ashadh</td>
      <td>2150000</td>
      <td>1490000</td>
      <td>720</td>
      <td>660000</td>
      <td>30.70</td>
      <td>279500.0</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 8
Load `data/payroll.csv` into `pay`. Add a new column `Annual_Net` = `Net_Salary` × 12. Then sort by `Annual_Net` (descending) and show the top 5 employees.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
pay = pd.read_csv("data/payroll.csv")
pay["Annual_Net"] = pay["Net_Salary"] * 12
pay.sort_values("Annual_Net", ascending=False).head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Emp_ID</th>
      <th>Name</th>
      <th>Department</th>
      <th>Designation</th>
      <th>Years_Exp</th>
      <th>Basic_Salary</th>
      <th>Allowance</th>
      <th>Gross</th>
      <th>EPF_10pct</th>
      <th>SSF_1pct</th>
      <th>Net_Salary</th>
      <th>Annual_Net</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>24</th>
      <td>E1024</td>
      <td>Bishnu Paudel</td>
      <td>Advisory</td>
      <td>Manager</td>
      <td>22</td>
      <td>250000</td>
      <td>100000.0</td>
      <td>350000.0</td>
      <td>25000.0</td>
      <td>3500.0</td>
      <td>321500.0</td>
      <td>3858000.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>E1007</td>
      <td>Kabita Rai</td>
      <td>Advisory</td>
      <td>Senior</td>
      <td>8</td>
      <td>250000</td>
      <td>100000.0</td>
      <td>350000.0</td>
      <td>25000.0</td>
      <td>3500.0</td>
      <td>321500.0</td>
      <td>3858000.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>E1014</td>
      <td>Manoj Rana</td>
      <td>Tax</td>
      <td>Senior</td>
      <td>17</td>
      <td>250000</td>
      <td>100000.0</td>
      <td>350000.0</td>
      <td>25000.0</td>
      <td>3500.0</td>
      <td>321500.0</td>
      <td>3858000.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>E1015</td>
      <td>Kalpana Pokhrel</td>
      <td>Audit</td>
      <td>Senior</td>
      <td>2</td>
      <td>180000</td>
      <td>72000.0</td>
      <td>252000.0</td>
      <td>18000.0</td>
      <td>2520.0</td>
      <td>231480.0</td>
      <td>2777760.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>E1004</td>
      <td>Bikash Gurung</td>
      <td>Tax</td>
      <td>Junior</td>
      <td>4</td>
      <td>180000</td>
      <td>72000.0</td>
      <td>252000.0</td>
      <td>18000.0</td>
      <td>2520.0</td>
      <td>231480.0</td>
      <td>2777760.0</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 10. GroupBy — the Pandas Pivot Table

`groupby()` is the most powerful feature you'll use. It splits data into groups, applies a function to each group, and combines the result. Exactly like a Pivot Table.


```python
# Total invoice amount per city
invoices.groupby("City")["Total_NPR"].sum().sort_values(ascending=False)
```




    City
    Bhaktapur     2608959.82
    Biratnagar    2432223.30
    Kathmandu     2299763.57
    Hetauda       2175177.68
    Lalitpur      2024371.27
    Butwal        1997602.70
    Birgunj       1989168.38
    Janakpur      1975963.20
    Nepalgunj     1934153.20
    Pokhara       1732977.04
    Name: Total_NPR, dtype: float64




```python
# Multiple metrics at once
invoices.groupby("Payment_Status").agg(
    Count        = ("Invoice_No", "count"),
    Total_Amount = ("Total_NPR", "sum"),
    Avg_Amount   = ("Total_NPR", "mean"),
).round(0)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Count</th>
      <th>Total_Amount</th>
      <th>Avg_Amount</th>
    </tr>
    <tr>
      <th>Payment_Status</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Overdue</th>
      <td>28</td>
      <td>3268298.0</td>
      <td>116725.0</td>
    </tr>
    <tr>
      <th>Paid</th>
      <td>133</td>
      <td>13633958.0</td>
      <td>102511.0</td>
    </tr>
    <tr>
      <th>Pending</th>
      <td>39</td>
      <td>4268104.0</td>
      <td>109439.0</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 9
Using `invoices`:

1. Find the **total Amount_NPR per Product**.
2. Find the **average Quantity per Customer**.
3. Count how many invoices each `City` has.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
print(invoices.groupby("Product")["Amount_NPR"].sum())
print()
print(invoices.groupby("Customer")["Quantity"].mean().round(1))
print()
print(invoices.groupby("City").size())
```

    Product
    Cosmetics      2304572.0
    Electronics    2802522.0
    Food           4614269.0
    Hardware       3289388.0
    Stationery     2863125.0
    Textile        2860956.0
    Name: Amount_NPR, dtype: float64
    
    Customer
    Annapurna Stores          24.0
    Biratnagar Enterprise     20.9
    Birgunj Cargo             26.6
    Everest Suppliers         25.0
    Himalayan Traders         22.0
    Janakpur Wholesale        24.2
    Kathmandu Distributors    27.8
    Lumbini Imports           26.1
    Nepalgunj Goods           27.0
    Pokhara Mart              21.8
    Name: Quantity, dtype: float64
    
    City
    Bhaktapur     26
    Biratnagar    15
    Birgunj       21
    Butwal        18
    Hetauda       20
    Janakpur      18
    Kathmandu     26
    Lalitpur      16
    Nepalgunj     20
    Pokhara       20
    dtype: int64


</details>

## 11. Saving your work to a file

Once you have cleaned / processed data, you can save the result.


```python
top5 = invoices.sort_values("Total_NPR", ascending=False).head(5)

top5.to_csv("top5_invoices.csv", index=False)   # save as CSV
# top5.to_excel("top5_invoices.xlsx", index=False)   # needs openpyxl

print("Saved top5_invoices.csv")
```

    Saved top5_invoices.csv


## 12. Mini-Project — Sales Analysis

Using `data/invoices.csv`, answer the following:

1. **Which city has the highest total sales?**
2. **Which product is sold the most (by quantity)?**
3. **What % of invoices are still pending or overdue?**
4. **List the top 3 customers by total revenue.**
5. **Find the average invoice amount city-wise.**


```python
inv = pd.read_csv("data/invoices.csv")

# Your code here
```

<details><summary>Show solution</summary>


```python
# 1
print("Top city by sales:")
print(inv.groupby("City")["Total_NPR"].sum().sort_values(ascending=False).head(1))
print()

# 2
print("Top product by qty:")
print(inv.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(1))
print()

# 3
pending_or_over = inv[inv["Payment_Status"] != "Paid"]
print(f"Pending+Overdue: {len(pending_or_over)/len(inv)*100:.1f}%")
print()

# 4
print("Top 3 customers:")
print(inv.groupby("Customer")["Total_NPR"].sum().sort_values(ascending=False).head(3))
print()

# 5
print("Average invoice per city:")
print(inv.groupby("City")["Total_NPR"].mean().round(0).sort_values(ascending=False))
```

    Top city by sales:
    City
    Bhaktapur    2608959.82
    Name: Total_NPR, dtype: float64
    
    Top product by qty:
    Product
    Food    1018
    Name: Quantity, dtype: int64
    
    Pending+Overdue: 33.5%
    
    Top 3 customers:
    Customer
    Nepalgunj Goods           2634935.13
    Kathmandu Distributors    2464900.64
    Janakpur Wholesale        2335671.58
    Name: Total_NPR, dtype: float64
    
    Average invoice per city:
    City
    Biratnagar    162148.0
    Lalitpur      126523.0
    Butwal        110978.0
    Janakpur      109776.0
    Hetauda       108759.0
    Bhaktapur     100345.0
    Nepalgunj      96708.0
    Birgunj        94722.0
    Kathmandu      88452.0
    Pokhara        86649.0
    Name: Total_NPR, dtype: float64


</details>

---
### What's next?
Pandas is now your everyday tool for working with tabular data.
In the next notebook (`03_Matplotlib_Seaborn`) we will turn this data into **charts** — line graphs, bar charts, heatmaps — so we can present it to clients and partners.
