# Telco customer churn: who leaves and why?

**Role focus:** Data Analyst / Data Scientist (customer retention)
**Tools:** Python, pandas, matplotlib, scikit-learn, Jupyter

## The problem

A telecom company loses about a quarter of its customers in a given period. Winning a new customer costs
far more than keeping an existing one, so the business wants to know two things:

1. Which kinds of customers cancel most often?
2. Can we flag customers who are likely to cancel, so the retention team can reach out first?

I worked on mobile and FinTech apps for years, where retention and churn are the metrics everyone
watches. This project is the same question from the data side: once you have a table of customers
and their plans, what can you actually learn from it?

## The data

- Kaggle: [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (7,043 rows, 21 columns)
- Original source: IBM sample data, published in the [IBM/telco-customer-churn-on-icp4d](https://github.com/IBM/telco-customer-churn-on-icp4d) repository (Apache 2.0 licence). `get_data.py` downloads the file from there.

Each row is one customer. The columns fall into four groups:

| Group | Columns |
|---|---|
| Who they are | `gender`, `SeniorCitizen`, `Partner`, `Dependents` |
| What they bought | `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies` |
| How they pay | `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`, `tenure` (months as a customer) |
| Target | `Churn` (Yes / No: did they leave in the last month) |

The dataset is not committed to this repo. Run `get_data.py` to fetch it (see below).

## Data cleaning

Only two fixes were needed:

- `TotalCharges` was stored as text because 11 rows were blank. All 11 are brand new customers
  with `tenure` = 0 who have not been billed yet, so I set their total to 0 rather than dropping them.
- `SeniorCitizen` was 0/1 while every other yes/no column used the words "Yes"/"No". I mapped it to words
  so the columns are consistent.

`customerID` was dropped because it carries no information about churn.

## What I found

| Question | Answer from the data |
|---|---|
| How many churn? | 26.5% (1,869 of 7,043 customers) |
| By contract | Month-to-month 43%, one year 11%, two year 3% |
| By tenure | First 6 months 53%, drops steadily to under 10% after 4 years |
| By monthly charge | Churners pay more: median $79.65 vs $64.43 for customers who stayed |
| By internet service | Fiber optic 42%, DSL 19%, no internet 7% |
| By payment method | Electronic check 45%, the three other methods 15 to 19% |
| Add-ons | No online security 42%, no tech support 42% |

In short: the typical churner is a newer, month-to-month fiber customer on an expensive plan who pays
by electronic check and has no add-ons.

## The model

A logistic regression trained on 80% of the customers and tested on the other 20%:

| Metric | Test set | What it means |
|---|---|---|
| Accuracy | 0.81 | Share of customers classified correctly. A model that always says "stayed" would get 0.73, so this is only a modest gain. |
| ROC AUC | 0.84 | How well the model ranks churners above non churners (0.5 is random, 1.0 is perfect). |
| Precision | 0.66 | Of the customers flagged as churn, 66% really churned. |
| Recall | 0.56 | Of the customers who really churned, the model caught 56%. |

The largest coefficients agree with the exploratory analysis: two year and one year contracts and long
tenure push toward staying; fiber optic internet and electronic check push toward churn.

I chose logistic regression on purpose. It is fast, it rarely overfits a dataset this size, and the
coefficients can be explained to a product manager in one sentence each.

## What a business could do

- Offer month-to-month customers in their first year a discount for moving to an annual contract.
  That is where most of the churn is.
- Nudge electronic check customers toward automatic payment. Whether electronic check causes churn or
  just goes with it is unknown, but it is a cheap thing to test.
- Bundle online security and tech support into fiber plans. Customers with those add-ons leave less.
- Use the model's churn probability to rank customers for outreach. The retention team can pick the
  cut-off that fits their capacity instead of using the default 50% threshold.

## How to run it

```bash
pip install -r requirements.txt
python get_data.py           # downloads data/Telco-Customer-Churn.csv (about 1 MB)
jupyter notebook churn_analysis.ipynb
```

Then run all cells from the top. The notebook takes a few seconds on a laptop.

## Limitations and next steps

- One snapshot in time with no dates, so no trend analysis and no way to say what happened after a price change.
- The model finds patterns, not causes. High monthly charges may just be a stand-in for "fiber plan with add-ons".
- `tenure`, `MonthlyCharges` and `TotalCharges` are tightly related (total is roughly tenure times monthly),
  so their individual coefficients should not be over-read.
- No tuning was done. Next steps I would try: class weights or a lower decision threshold to raise recall,
  a gradient boosted tree model for comparison, and a cost based evaluation (what does a false alarm cost vs a missed churner).

## Files

```
churn_analysis.ipynb   the full analysis with outputs, runs top to bottom
get_data.py            downloads the dataset into data/
requirements.txt       Python packages used
INTERVIEW.md           short notes for talking through this project in an interview
```
