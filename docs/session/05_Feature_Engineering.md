# Notebook 5 — Feature Engineering for CA Professionals

**Goal:** Create new, useful columns ("features") from existing data — so that charts, dashboards and machine learning models can give better answers.

**You will learn:**

1. What is a "feature" and why we create new ones
2. Math features — ratios, growth rates, age
3. Date features — month, weekday, festival flag
4. Binning — turning numbers into buckets (e.g. invoice size: Small/Medium/Large)
5. Encoding categorical columns into numbers
6. Scaling numeric columns
7. Aggregated features — per-customer summaries
8. A short mini-project

---

## 1. What is "feature engineering"?

A **feature** is just a column in your dataset. *Feature engineering* means **creating new columns** that make the underlying signal more obvious.

A CA-style example:

| Existing columns                            | New (engineered) feature           |
|---------------------------------------------|------------------------------------|
| `Revenue`, `Expense`                        | `Profit_Margin = (R-E)/R`          |
| `Loan_Amount`, `Annual_Income`              | `Loan_to_Income_Ratio`             |
| `Invoice_Date`, `Today`                     | `Days_Outstanding`                 |
| `Amount`                                    | `Size_Bucket = Small / Medium / Large`|
| `City`                                      | encoded numbers (for ML)           |

Better features → better insights → better models.


```python
import pandas as pd
import numpy as np
print("ready")
```

    ready


## 2. Math features — ratios and percentages


```python
sales = pd.read_csv("data/monthly_sales.csv")

sales["Profit"]        = sales["Revenue_NPR"] - sales["Expense_NPR"]
sales["Profit_Margin"] = (sales["Profit"] / sales["Revenue_NPR"] * 100).round(2)
sales["Expense_Ratio"] = (sales["Expense_NPR"] / sales["Revenue_NPR"] * 100).round(2)
sales["Avg_Price"]     = (sales["Revenue_NPR"] / sales["Units_Sold"]).round(0)

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
      <th>Profit</th>
      <th>Profit_Margin</th>
      <th>Expense_Ratio</th>
      <th>Avg_Price</th>
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
      <td>73.60</td>
      <td>2976.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bhadra</td>
      <td>1380000</td>
      <td>980000</td>
      <td>465</td>
      <td>400000</td>
      <td>28.99</td>
      <td>71.01</td>
      <td>2968.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ashwin</td>
      <td>1120000</td>
      <td>870000</td>
      <td>380</td>
      <td>250000</td>
      <td>22.32</td>
      <td>77.68</td>
      <td>2947.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Kartik</td>
      <td>1450000</td>
      <td>1050000</td>
      <td>498</td>
      <td>400000</td>
      <td>27.59</td>
      <td>72.41</td>
      <td>2912.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mangsir</td>
      <td>1620000</td>
      <td>1180000</td>
      <td>540</td>
      <td>440000</td>
      <td>27.16</td>
      <td>72.84</td>
      <td>3000.0</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 1
Load `data/loans.csv` and create a new feature **`Loan_to_Income`** = `Loan_Amount` ÷ `Annual_Income`. Print the first 5 rows of `Loan_ID`, `Loan_Amount`, `Annual_Income`, `Loan_to_Income`.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
loans = pd.read_csv("data/loans.csv")
loans["Loan_to_Income"] = (loans["Loan_Amount"] / loans["Annual_Income"]).round(2)
loans[["Loan_ID","Loan_Amount","Annual_Income","Loan_to_Income"]].head()
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
      <th>Loan_ID</th>
      <th>Loan_Amount</th>
      <th>Annual_Income</th>
      <th>Loan_to_Income</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>L2000</td>
      <td>100000</td>
      <td>180000</td>
      <td>0.56</td>
    </tr>
    <tr>
      <th>1</th>
      <td>L2001</td>
      <td>500000</td>
      <td>360000</td>
      <td>1.39</td>
    </tr>
    <tr>
      <th>2</th>
      <td>L2002</td>
      <td>1000000</td>
      <td>180000</td>
      <td>5.56</td>
    </tr>
    <tr>
      <th>3</th>
      <td>L2003</td>
      <td>100000</td>
      <td>180000</td>
      <td>0.56</td>
    </tr>
    <tr>
      <th>4</th>
      <td>L2004</td>
      <td>100000</td>
      <td>180000</td>
      <td>0.56</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 3. Growth / change features

`pct_change()` calculates row-over-row % change — handy for month-over-month growth.


```python
sales["MoM_Growth_%"] = (sales["Revenue_NPR"].pct_change() * 100).round(2)
sales[["Month","Revenue_NPR","MoM_Growth_%"]]
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
      <th>MoM_Growth_%</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Shrawan</td>
      <td>1250000</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bhadra</td>
      <td>1380000</td>
      <td>10.40</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ashwin</td>
      <td>1120000</td>
      <td>-18.84</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Kartik</td>
      <td>1450000</td>
      <td>29.46</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mangsir</td>
      <td>1620000</td>
      <td>11.72</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Poush</td>
      <td>1780000</td>
      <td>9.88</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Magh</td>
      <td>1550000</td>
      <td>-12.92</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Falgun</td>
      <td>1420000</td>
      <td>-8.39</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Chaitra</td>
      <td>1680000</td>
      <td>18.31</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Baishakh</td>
      <td>1910000</td>
      <td>13.69</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Jestha</td>
      <td>2030000</td>
      <td>6.28</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Ashadh</td>
      <td>2150000</td>
      <td>5.91</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 2
Compute the month-over-month % change of `Units_Sold` in the `sales` DataFrame.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
sales["Units_Growth_%"] = (sales["Units_Sold"].pct_change() * 100).round(2)
sales[["Month","Units_Sold","Units_Growth_%"]]
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
      <th>Units_Sold</th>
      <th>Units_Growth_%</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Shrawan</td>
      <td>420</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Bhadra</td>
      <td>465</td>
      <td>10.71</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ashwin</td>
      <td>380</td>
      <td>-18.28</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Kartik</td>
      <td>498</td>
      <td>31.05</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Mangsir</td>
      <td>540</td>
      <td>8.43</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Poush</td>
      <td>605</td>
      <td>12.04</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Magh</td>
      <td>515</td>
      <td>-14.88</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Falgun</td>
      <td>478</td>
      <td>-7.18</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Chaitra</td>
      <td>560</td>
      <td>17.15</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Baishakh</td>
      <td>640</td>
      <td>14.29</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Jestha</td>
      <td>690</td>
      <td>7.81</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Ashadh</td>
      <td>720</td>
      <td>4.35</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 4. Date features

Most date columns hide useful information: month, day of week, weekend or not, quarter, year-end indicator. Once parsed, you can extract any of these.


```python
inv = pd.read_csv("data/invoices.csv")
inv["Date"] = pd.to_datetime(inv["Date"])

inv["Year"]       = inv["Date"].dt.year
inv["Month"]      = inv["Date"].dt.month
inv["Quarter"]    = inv["Date"].dt.quarter
inv["Weekday"]    = inv["Date"].dt.day_name()
inv["Is_Weekend"] = inv["Date"].dt.weekday >= 5

# Days outstanding — assuming today is 2025-04-01
today = pd.Timestamp("2025-04-01")
inv["Days_Old"] = (today - inv["Date"]).dt.days

inv[["Date","Year","Month","Quarter","Weekday","Is_Weekend","Days_Old"]].head()
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
      <th>Date</th>
      <th>Year</th>
      <th>Month</th>
      <th>Quarter</th>
      <th>Weekday</th>
      <th>Is_Weekend</th>
      <th>Days_Old</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2024-07-16</td>
      <td>2024</td>
      <td>7</td>
      <td>3</td>
      <td>Tuesday</td>
      <td>False</td>
      <td>259</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2024-07-18</td>
      <td>2024</td>
      <td>7</td>
      <td>3</td>
      <td>Thursday</td>
      <td>False</td>
      <td>257</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2024-07-20</td>
      <td>2024</td>
      <td>7</td>
      <td>3</td>
      <td>Saturday</td>
      <td>True</td>
      <td>255</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2024-07-22</td>
      <td>2024</td>
      <td>7</td>
      <td>3</td>
      <td>Monday</td>
      <td>False</td>
      <td>253</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2024-07-24</td>
      <td>2024</td>
      <td>7</td>
      <td>3</td>
      <td>Wednesday</td>
      <td>False</td>
      <td>251</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 3
Load `data/customers.csv` and use the `Onboarded_Date` column to compute, for each customer, **how many days they've been a customer** (use `pd.Timestamp("2025-04-01")` as "today").


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
cust = pd.read_csv("data/customers.csv")
cust["Onboarded_Date"] = pd.to_datetime(cust["Onboarded_Date"])
cust["Customer_Age_Days"] = (pd.Timestamp("2025-04-01") - cust["Onboarded_Date"]).dt.days
cust[["Customer_ID","Onboarded_Date","Customer_Age_Days"]].head()
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
      <th>Customer_ID</th>
      <th>Onboarded_Date</th>
      <th>Customer_Age_Days</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>C500</td>
      <td>2024-03-29</td>
      <td>368</td>
    </tr>
    <tr>
      <th>1</th>
      <td>C501</td>
      <td>2023-05-31</td>
      <td>671</td>
    </tr>
    <tr>
      <th>2</th>
      <td>C502</td>
      <td>2023-06-28</td>
      <td>643</td>
    </tr>
    <tr>
      <th>3</th>
      <td>C503</td>
      <td>2023-05-06</td>
      <td>696</td>
    </tr>
    <tr>
      <th>4</th>
      <td>C504</td>
      <td>2024-05-10</td>
      <td>326</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 5. Binning — turning numbers into categories

Sometimes a category is more useful than the raw number. For example, we might want every invoice classified as **Small / Medium / Large**.

`pd.cut()` does this for you.


```python
bins   = [0, 50000, 200000, np.inf]            # the cut-points
labels = ["Small", "Medium", "Large"]

inv["Size_Bucket"] = pd.cut(inv["Amount_NPR"], bins=bins, labels=labels)
inv["Size_Bucket"].value_counts()
```




    Size_Bucket
    Medium    94
    Small     80
    Large     26
    Name: count, dtype: int64



### Practice 4
Bin the `Credit_Score` column in `loans` into 3 buckets:

| Range            | Label    |
|------------------|----------|
| 300 – 580        | Poor     |
| 581 – 720        | Fair     |
| 721 – 850        | Good     |

Then count how many loans fall in each bucket.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
loans["Score_Bucket"] = pd.cut(loans["Credit_Score"],
                                bins=[299, 580, 720, 850],
                                labels=["Poor","Fair","Good"])
print(loans["Score_Bucket"].value_counts())
```

    Score_Bucket
    Poor    140
    Fair     86
    Good     74
    Name: count, dtype: int64


</details>

## 6. Encoding categorical columns into numbers

Machine learning models only understand **numbers**. So a column like `Payment_Status = "Paid" / "Pending" / "Overdue"` must be converted.

Two common methods:

| Method            | When to use                                      |
|-------------------|--------------------------------------------------|
| `map()`           | A small fixed list (e.g. Yes/No, M/F)           |
| `pd.get_dummies()`| Many unordered categories (one column per value)|


```python
# Method 1 — simple mapping
status_map = {"Paid": 0, "Pending": 1, "Overdue": 2}
inv["Status_Code"] = inv["Payment_Status"].map(status_map)
inv[["Payment_Status","Status_Code"]].head()
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
      <th>Payment_Status</th>
      <th>Status_Code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Paid</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Overdue</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Paid</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Paid</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Paid</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Method 2 — one-hot encoding (good for unordered categories)
city_dummies = pd.get_dummies(inv["City"], prefix="City").astype(int)
city_dummies.head()
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
      <th>City_Bhaktapur</th>
      <th>City_Biratnagar</th>
      <th>City_Birgunj</th>
      <th>City_Butwal</th>
      <th>City_Hetauda</th>
      <th>City_Janakpur</th>
      <th>City_Kathmandu</th>
      <th>City_Lalitpur</th>
      <th>City_Nepalgunj</th>
      <th>City_Pokhara</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 5
In the `loans` DataFrame:

1. Map `Has_Collateral` to numbers: `"Yes"` → 1, `"No"` → 0. Store as `Has_Coll_Code`.
2. One-hot encode the `Sector` column with prefix `"Sec"` and show the first 5 rows.


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
loans["Has_Coll_Code"] = loans["Has_Collateral"].map({"Yes": 1, "No": 0})
sec = pd.get_dummies(loans["Sector"], prefix="Sec").astype(int)
print(loans[["Has_Collateral","Has_Coll_Code"]].head())
sec.head()
```

      Has_Collateral  Has_Coll_Code
    0             No              0
    1            Yes              1
    2            Yes              1
    3            Yes              1
    4            Yes              1





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
      <th>Sec_Agriculture</th>
      <th>Sec_Manufacturing</th>
      <th>Sec_Personal</th>
      <th>Sec_Service</th>
      <th>Sec_Trade</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 7. Scaling numeric columns

When one column is in *lakhs* and another in *percentage points*, models can get confused by the difference in magnitude.

The fix is to **scale** all numeric columns to a similar range.

| Scaler             | Output range          |
|--------------------|-----------------------|
| **Min-Max**        | 0 to 1                |
| **Standard (Z-score)** | mean 0, std 1     |


```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Pick the numeric columns we want to scale
num_cols = ["Loan_Amount", "Annual_Income", "Credit_Score"]

mm = MinMaxScaler()
loans_mm = pd.DataFrame(mm.fit_transform(loans[num_cols]),
                        columns=[c+"_mm" for c in num_cols])

sd = StandardScaler()
loans_sd = pd.DataFrame(sd.fit_transform(loans[num_cols]),
                        columns=[c+"_z" for c in num_cols])

pd.concat([loans[num_cols].head(),
           loans_mm.head(),
           loans_sd.head().round(2)], axis=1)
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
      <th>Loan_Amount</th>
      <th>Annual_Income</th>
      <th>Credit_Score</th>
      <th>Loan_Amount_mm</th>
      <th>Annual_Income_mm</th>
      <th>Credit_Score_mm</th>
      <th>Loan_Amount_z</th>
      <th>Annual_Income_z</th>
      <th>Credit_Score_z</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>100000</td>
      <td>180000</td>
      <td>300</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>-0.75</td>
      <td>-0.81</td>
      <td>-1.78</td>
    </tr>
    <tr>
      <th>1</th>
      <td>500000</td>
      <td>360000</td>
      <td>451</td>
      <td>0.081633</td>
      <td>0.081081</td>
      <td>0.275046</td>
      <td>-0.39</td>
      <td>-0.51</td>
      <td>-0.82</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1000000</td>
      <td>180000</td>
      <td>521</td>
      <td>0.183673</td>
      <td>0.000000</td>
      <td>0.402550</td>
      <td>0.06</td>
      <td>-0.81</td>
      <td>-0.38</td>
    </tr>
    <tr>
      <th>3</th>
      <td>100000</td>
      <td>180000</td>
      <td>403</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.187614</td>
      <td>-0.75</td>
      <td>-0.81</td>
      <td>-1.13</td>
    </tr>
    <tr>
      <th>4</th>
      <td>100000</td>
      <td>180000</td>
      <td>750</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.819672</td>
      <td>-0.75</td>
      <td>-0.81</td>
      <td>1.06</td>
    </tr>
  </tbody>
</table>
</div>



## 8. Aggregated features — per-customer summaries

Sometimes the right "feature" lives at a higher level. For example: instead of looking at each invoice, build a row per customer summarising their entire behaviour.


```python
cust_feat = inv.groupby("Customer").agg(
    Total_Invoices = ("Invoice_No",  "count"),
    Total_Amount   = ("Amount_NPR",  "sum"),
    Avg_Amount     = ("Amount_NPR",  "mean"),
    Max_Amount     = ("Amount_NPR",  "max"),
    Pending_Count  = ("Payment_Status", lambda s: (s != "Paid").sum()),
).round(0)

cust_feat["Pending_Ratio"] = (cust_feat["Pending_Count"] /
                              cust_feat["Total_Invoices"]).round(2)
cust_feat.head()
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
      <th>Total_Invoices</th>
      <th>Total_Amount</th>
      <th>Avg_Amount</th>
      <th>Max_Amount</th>
      <th>Pending_Count</th>
      <th>Pending_Ratio</th>
    </tr>
    <tr>
      <th>Customer</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Annapurna Stores</th>
      <td>19</td>
      <td>2042877.0</td>
      <td>107520.0</td>
      <td>359325.0</td>
      <td>5</td>
      <td>0.26</td>
    </tr>
    <tr>
      <th>Biratnagar Enterprise</th>
      <td>23</td>
      <td>1337239.0</td>
      <td>58141.0</td>
      <td>215209.0</td>
      <td>8</td>
      <td>0.35</td>
    </tr>
    <tr>
      <th>Birgunj Cargo</th>
      <td>19</td>
      <td>1779339.0</td>
      <td>93649.0</td>
      <td>269451.0</td>
      <td>9</td>
      <td>0.47</td>
    </tr>
    <tr>
      <th>Everest Suppliers</th>
      <td>17</td>
      <td>1669287.0</td>
      <td>98193.0</td>
      <td>273714.0</td>
      <td>6</td>
      <td>0.35</td>
    </tr>
    <tr>
      <th>Himalayan Traders</th>
      <td>23</td>
      <td>2056517.0</td>
      <td>89414.0</td>
      <td>243441.0</td>
      <td>10</td>
      <td>0.43</td>
    </tr>
  </tbody>
</table>
</div>



### Practice 6
Build a per-**City** summary from `inv` containing: `Total_Invoices`, `Total_Amount`, `Avg_Amount`. Sort by `Total_Amount` (largest first).


```python
# Your turn:
```

<details><summary>Show solution</summary>


```python
city_feat = inv.groupby("City").agg(
    Total_Invoices = ("Invoice_No","count"),
    Total_Amount   = ("Amount_NPR","sum"),
    Avg_Amount     = ("Amount_NPR","mean"),
).round(0).sort_values("Total_Amount", ascending=False)
city_feat
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
      <th>Total_Invoices</th>
      <th>Total_Amount</th>
      <th>Avg_Amount</th>
    </tr>
    <tr>
      <th>City</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bhaktapur</th>
      <td>26</td>
      <td>2308814.0</td>
      <td>88801.0</td>
    </tr>
    <tr>
      <th>Biratnagar</th>
      <td>15</td>
      <td>2152410.0</td>
      <td>143494.0</td>
    </tr>
    <tr>
      <th>Kathmandu</th>
      <td>26</td>
      <td>2035189.0</td>
      <td>78276.0</td>
    </tr>
    <tr>
      <th>Hetauda</th>
      <td>20</td>
      <td>1924936.0</td>
      <td>96247.0</td>
    </tr>
    <tr>
      <th>Lalitpur</th>
      <td>16</td>
      <td>1791479.0</td>
      <td>111967.0</td>
    </tr>
    <tr>
      <th>Butwal</th>
      <td>18</td>
      <td>1767790.0</td>
      <td>98211.0</td>
    </tr>
    <tr>
      <th>Birgunj</th>
      <td>21</td>
      <td>1760326.0</td>
      <td>83825.0</td>
    </tr>
    <tr>
      <th>Janakpur</th>
      <td>18</td>
      <td>1748640.0</td>
      <td>97147.0</td>
    </tr>
    <tr>
      <th>Nepalgunj</th>
      <td>20</td>
      <td>1711640.0</td>
      <td>85582.0</td>
    </tr>
    <tr>
      <th>Pokhara</th>
      <td>20</td>
      <td>1533608.0</td>
      <td>76680.0</td>
    </tr>
  </tbody>
</table>
</div>



</details>

## 9. Mini-Project — Customer Feature Set

Goal: prepare a **per-customer feature table** ready for the regression / classification notebooks.

Steps:
1. Load `data/invoices.csv` and parse the `Date` column.
2. For each customer build these features:
   - `Total_Invoices`
   - `Total_Amount`
   - `Avg_Amount`
   - `First_Invoice_Date`
   - `Last_Invoice_Date`
   - `Days_Active` = `Last - First` in days
   - `Pending_Ratio` (share of invoices not paid)
3. Bin `Total_Amount` into Small / Medium / Large buckets (decide your own cut-points).
4. Save the result as `customer_features.csv`.


```python
df = pd.read_csv("data/invoices.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Your code here
```

<details><summary>Show solution</summary>


```python
df = pd.read_csv("data/invoices.csv")
df["Date"] = pd.to_datetime(df["Date"])

cf = df.groupby("Customer").agg(
    Total_Invoices = ("Invoice_No","count"),
    Total_Amount   = ("Amount_NPR","sum"),
    Avg_Amount     = ("Amount_NPR","mean"),
    First_Invoice  = ("Date","min"),
    Last_Invoice   = ("Date","max"),
    Pending_Cnt    = ("Payment_Status", lambda s: (s != "Paid").sum()),
).round(0)

cf["Days_Active"]   = (cf["Last_Invoice"] - cf["First_Invoice"]).dt.days
cf["Pending_Ratio"] = (cf["Pending_Cnt"] / cf["Total_Invoices"]).round(2)
cf["Customer_Size"] = pd.cut(cf["Total_Amount"],
                              bins=[0, 1_000_000, 5_000_000, np.inf],
                              labels=["Small","Medium","Large"])

cf.to_csv("customer_features.csv")
cf.head()
```

    /var/folders/cm/07z8g9cd5r3092d58mr51l3w0000gn/T/ipykernel_59834/1824703694.py:11: UserWarning: obj.round has no effect with datetime, timedelta, or period dtypes. Use obj.dt.round(...) instead.
      ).round(0)





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
      <th>Total_Invoices</th>
      <th>Total_Amount</th>
      <th>Avg_Amount</th>
      <th>First_Invoice</th>
      <th>Last_Invoice</th>
      <th>Pending_Cnt</th>
      <th>Days_Active</th>
      <th>Pending_Ratio</th>
      <th>Customer_Size</th>
    </tr>
    <tr>
      <th>Customer</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Annapurna Stores</th>
      <td>19</td>
      <td>2042877.0</td>
      <td>107520.0</td>
      <td>2024-07-28</td>
      <td>2025-07-19</td>
      <td>5</td>
      <td>356</td>
      <td>0.26</td>
      <td>Medium</td>
    </tr>
    <tr>
      <th>Biratnagar Enterprise</th>
      <td>23</td>
      <td>1337239.0</td>
      <td>58141.0</td>
      <td>2024-07-20</td>
      <td>2025-08-10</td>
      <td>8</td>
      <td>386</td>
      <td>0.35</td>
      <td>Medium</td>
    </tr>
    <tr>
      <th>Birgunj Cargo</th>
      <td>19</td>
      <td>1779339.0</td>
      <td>93649.0</td>
      <td>2024-07-26</td>
      <td>2025-07-25</td>
      <td>9</td>
      <td>364</td>
      <td>0.47</td>
      <td>Medium</td>
    </tr>
    <tr>
      <th>Everest Suppliers</th>
      <td>17</td>
      <td>1669287.0</td>
      <td>98193.0</td>
      <td>2024-08-17</td>
      <td>2025-08-16</td>
      <td>6</td>
      <td>364</td>
      <td>0.35</td>
      <td>Medium</td>
    </tr>
    <tr>
      <th>Himalayan Traders</th>
      <td>23</td>
      <td>2056517.0</td>
      <td>89414.0</td>
      <td>2024-08-27</td>
      <td>2025-08-06</td>
      <td>10</td>
      <td>344</td>
      <td>0.43</td>
      <td>Medium</td>
    </tr>
  </tbody>
</table>
</div>



</details>

---
### What's next?
You now know how to **shape** raw data into model-ready features.
In `06_Regression` we will use these features to **predict numbers** (like next month's revenue),
and in `07_Classification` we will **predict categories** (like loan default).
