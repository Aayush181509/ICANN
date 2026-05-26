"""Build session/07_Classification.ipynb"""
from pathlib import Path
from _nb_helper import md, code, save_notebook

C = []

C.append(md(r"""
# Notebook 7 — Classification for CA Professionals

**Goal:** Predict a **category** — for example "will this loan default — Yes or No?"

**You will learn:**
1. What classification is and how it differs from regression
2. Preparing the data (X / y, encoding, train/test split)
3. Logistic Regression — a simple, interpretable classifier
4. Decision Tree — a model your manager can read
5. Measuring quality: Accuracy, Confusion Matrix, Precision/Recall
6. Which features matter most
7. A short mini-project on loan default

> The dataset is `data/loans.csv` — 300 loans with a known `Defaulted` (1/0) flag.

---
"""))

# Section 1
C.append(md(r"""
## 1. Classification vs Regression

| Question                                 | Type            |
|------------------------------------------|-----------------|
| "What will next month's revenue be?"     | Regression (number) |
| "Will this client default? Yes / No"     | Classification (category) |
| "Is this transaction fraudulent?"        | Classification |
| "Which risk bucket does the customer fall in: Low/Med/High?" | Classification (3 classes) |

The data preparation steps are the **same**. Only the model and the evaluation metrics change.
"""))

C.append(code(r"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")

loans = pd.read_csv("data/loans.csv")
print("Shape :", loans.shape)
print("Default rate :", f"{loans['Defaulted'].mean()*100:.1f}%")
loans.head()
"""))

# Section 2
C.append(md(r"""
## 2. Preparing the data

Two preparation steps:

1. **Encode** any text column into numbers (so the model can read it).
2. **Split** into a feature matrix `X` and a target vector `y`.
"""))

C.append(code(r"""
# Encode text columns
loans["Has_Coll_Code"] = loans["Has_Collateral"].map({"Yes": 1, "No": 0})

# One-hot encode the Sector column
sector_dummies = pd.get_dummies(loans["Sector"], prefix="Sec").astype(int)
data = pd.concat([loans, sector_dummies], axis=1)

# Pick the features we will use
feature_cols = [
    "Loan_Amount", "Tenure_Months", "Interest_Rate",
    "Annual_Income", "Credit_Score", "Has_Coll_Code",
] + list(sector_dummies.columns)

X = data[feature_cols]
y = data["Defaulted"]

X.head()
"""))

C.append(code(r"""
from sklearn.model_selection import train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
print("Train:", len(X_tr), "  Test:", len(X_te))
print("Default rate (train):", f"{y_tr.mean()*100:.1f}%")
print("Default rate (test) :", f"{y_te.mean()*100:.1f}%")
"""))

# Section 3
C.append(md(r"""
## 3. Logistic Regression — the simplest classifier

Despite the name "regression", logistic regression is a **classification** model. It outputs a probability between 0 and 1 — anything above 0.5 means "predict default".
"""))

C.append(code(r"""
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Scaling helps logistic regression converge cleanly
scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_te_s = scaler.transform(X_te)

logit = LogisticRegression(max_iter=1000)
logit.fit(X_tr_s, y_tr)

print("Training accuracy :", round(logit.score(X_tr_s, y_tr), 3))
print("Test accuracy     :", round(logit.score(X_te_s, y_te), 3))
"""))

# Section 4: evaluation
C.append(md(r"""
## 4. Confusion Matrix — where the model is right and wrong

The confusion matrix is the heart of classification evaluation:

```
                  Predicted: No   Predicted: Yes
Actual: No   →    TN  (good)       FP  (false alarm)
Actual: Yes  →    FN  (missed!)    TP  (caught)
```

| Metric    | Formula              | Meaning                              |
|-----------|----------------------|--------------------------------------|
| Accuracy  | (TP+TN)/all          | overall % correct                    |
| Precision | TP / (TP+FP)         | "of those predicted default, % correct" |
| Recall    | TP / (TP+FN)         | "of actual defaults, % caught"       |

For loan default the **most expensive mistake** is FN — missing a real defaulter. So we care most about **Recall**.
"""))

C.append(code(r"""
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

y_pred = logit.predict(X_te_s)

cm = confusion_matrix(y_te, y_pred)
print("Confusion matrix:")
print(cm)
print()
print(classification_report(y_te, y_pred, target_names=["No Default","Default"]))
"""))

C.append(code(r"""
ConfusionMatrixDisplay(cm, display_labels=["No Default","Default"]).plot(cmap="Blues")
plt.title("Logistic Regression — confusion matrix")
plt.tight_layout()
plt.show()
"""))

C.append(md(r"""
### Practice 1
Compute the **accuracy** by hand from the confusion matrix above:

`accuracy = (TN + TP) / total`

Print the result and check it matches `accuracy_score(y_te, y_pred)`.
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
from sklearn.metrics import accuracy_score
tn, fp, fn, tp = cm.ravel()
print(f"By hand : {(tn+tp)/(tn+fp+fn+tp):.3f}")
print(f"Sklearn : {accuracy_score(y_te, y_pred):.3f}")
"""))
C.append(md(r"""</details>"""))

# Section 5: decision tree
C.append(md(r"""
## 5. Decision Tree — a model you can read

A Decision Tree builds a flowchart of yes/no questions. Easy to explain to non-technical clients.
"""))

C.append(code(r"""
from sklearn.tree import DecisionTreeClassifier, plot_tree

tree = DecisionTreeClassifier(max_depth=4, random_state=0)
tree.fit(X_tr, y_tr)   # trees don't need scaling

print("Train accuracy:", round(tree.score(X_tr, y_tr), 3))
print("Test  accuracy:", round(tree.score(X_te, y_te), 3))
"""))

C.append(code(r"""
plt.figure(figsize=(15, 7))
plot_tree(tree,
          feature_names=X.columns,
          class_names=["No Default","Default"],
          filled=True, rounded=True, fontsize=8)
plt.title("Decision Tree (depth 4)")
plt.show()
"""))

C.append(md(r"""
### Practice 2
Build another Decision Tree with `max_depth=2` (a very shallow tree). Print its train and test accuracy. Is it better or worse than the depth-4 tree?
"""))

C.append(code(r"""
# Your turn:
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))
C.append(code(r"""
t2 = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_tr, y_tr)
print("depth=2 train:", round(t2.score(X_tr, y_tr), 3))
print("depth=2 test :", round(t2.score(X_te, y_te), 3))
"""))
C.append(md(r"""</details>"""))

# Section 6: feature importance
C.append(md(r"""
## 6. Which features matter most?

A Decision Tree (and other tree models) can tell us which inputs were most useful.
"""))

C.append(code(r"""
imp = pd.Series(tree.feature_importances_, index=X.columns)
imp = imp.sort_values(ascending=False)

sns.barplot(x=imp.values, y=imp.index, color="steelblue")
plt.title("Feature Importance — Decision Tree")
plt.xlabel("Importance")
plt.tight_layout()
plt.show()

imp.round(3)
"""))

# Section 7: predict new
C.append(md(r"""
## 7. Predicting for a new loan application

Given a brand-new application, the model tells us the **probability of default**.
"""))

C.append(code(r"""
new_loan = pd.DataFrame({
    "Loan_Amount":   [1500000],
    "Tenure_Months": [36],
    "Interest_Rate": [12.5],
    "Annual_Income": [600000],
    "Credit_Score":  [610],
    "Has_Coll_Code": [0],            # no collateral
    "Sec_Agriculture":[0], "Sec_Manufacturing":[0],
    "Sec_Personal":[1],  "Sec_Service":[0], "Sec_Trade":[0],
})

# Make sure the columns match X exactly
new_loan = new_loan[X.columns]

prob = tree.predict_proba(new_loan)[0, 1]
print(f"Default probability : {prob*100:.1f}%")
print("Decision           :", "REJECT / High risk" if prob > 0.5 else "Approve")
"""))

# Mini Project
C.append(md(r"""
## 8. Mini-Project — Build your own default-risk classifier

Steps:

1. Re-load `data/loans.csv`.
2. Encode `Has_Collateral` and one-hot encode `Sector`.
3. Build `X` and `y` (target = `Defaulted`).
4. Split 70 / 30 with `random_state=1`.
5. Train **both** a `LogisticRegression` (with scaling) and a `DecisionTreeClassifier(max_depth=5)`.
6. Print test accuracy and the **classification report** for each.
7. Plot the confusion matrix for the better model.
8. Write a one-line conclusion: which model would you pick and why?
"""))

C.append(code(r"""
# Your code here
"""))

C.append(md(r"""<details><summary>Show solution</summary>"""))

C.append(code(r"""
df = pd.read_csv("data/loans.csv")
df["Has_Coll_Code"] = df["Has_Collateral"].map({"Yes":1,"No":0})
dum = pd.get_dummies(df["Sector"], prefix="Sec").astype(int)
df = pd.concat([df, dum], axis=1)

feat = ["Loan_Amount","Tenure_Months","Interest_Rate","Annual_Income",
        "Credit_Score","Has_Coll_Code"] + list(dum.columns)
X, y = df[feat], df["Defaulted"]

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

sc = StandardScaler()
X_tr_s = sc.fit_transform(X_tr); X_te_s = sc.transform(X_te)

lr = LogisticRegression(max_iter=1000).fit(X_tr_s, y_tr)
dt = DecisionTreeClassifier(max_depth=5, random_state=1).fit(X_tr, y_tr)

for name, m, Xt in [("LogReg", lr, X_te_s), ("Tree", dt, X_te)]:
    p = m.predict(Xt)
    print(f"\n=== {name} ===")
    print("Accuracy:", round(m.score(Xt, y_te), 3))
    print(classification_report(y_te, p, target_names=["No Def","Def"]))

# pick the better one to show CM
better = lr if lr.score(X_te_s, y_te) >= dt.score(X_te, y_te) else dt
cm = confusion_matrix(y_te, better.predict(X_te_s if better is lr else X_te))
ConfusionMatrixDisplay(cm, display_labels=["No Def","Def"]).plot(cmap="Greens")
plt.tight_layout(); plt.show()

print("\nConclusion: pick the model with higher *recall* on Default class —")
print("missing a real defaulter (FN) costs more than a false alarm.")
"""))
C.append(md(r"""</details>"""))

C.append(md(r"""
---
## 🎉 Session Complete!

| Notebook | What you learned |
|----------|------------------|
| 1. NumPy | Fast array maths on financial data |
| 2. Pandas | Excel-style tables in Python |
| 3. Charts | Visualising trends, breakdowns, distributions |
| 4. Data Cleaning | Making messy real-world data analysis-ready |
| 5. Feature Engineering | Building useful columns from existing ones |
| 6. Regression | Predicting numbers (revenue, expense) |
| 7. Classification | Predicting categories (default, fraud, churn) |

You now have the **complete toolkit** to:

- Pull data from any CSV / Excel file
- Clean and shape it
- Visualise it for a client deck
- Run predictive models for forecasting & risk

Keep practising on **your own audit files** — the same skills generalise directly.
"""))

save_notebook(C, Path(__file__).parent / "07_Classification.ipynb")
