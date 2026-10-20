# Interview notes: Telco customer churn

Short answers I can give in my own words. Numbers are from the notebook.

**What problem does the project solve?**
A telecom company loses about 26% of customers in a period. The project finds which customer groups
leave most, and builds a simple model to flag customers who are likely to leave so the retention team
can contact them first.

**Why this dataset?**
It is small (7,043 rows), clean enough to finish in one sitting, and it is about churn, which is the
metric I spent years watching as a mobile app developer. Every row is a customer with their plan and
billing details, which is exactly the shape of data a product analytics team works with.

**What cleaning did you do?**
Two things. `TotalCharges` came in as text because 11 rows were blank. Those 11 customers had tenure 0,
meaning they had never been billed, so I set the total to 0 instead of dropping them. And `SeniorCitizen`
was 0/1 while every other yes/no column used words, so I mapped it to Yes/No for consistency.

**What analysis did you do?**
Churn rate per group for contract type, tenure, payment method, internet service and every other
category column, plus a histogram of monthly charges for churners vs non churners. Then a logistic
regression to predict churn.

**Why logistic regression?**
It is the simplest model that gives a probability, it trains in under a second, and the coefficients
tell you which features push toward churn and which push toward staying. For a first model and a
business audience that matters more than a few points of accuracy.

**Why these metrics?**
Accuracy alone is misleading because 73% of customers stay, so "always say stayed" already scores 0.73.
Recall tells the retention team what share of real churners they would reach. Precision tells them how
many calls would be wasted. ROC AUC says how well the model ranks customers regardless of the threshold.

**What do the results mean in practice?**
Month-to-month customers churn at 43% vs 3% for two year contracts. Half of customers leave within their
first six months. Fiber customers on expensive plans who pay by electronic check are the highest risk
group. The model catches 56% of churners with 66% precision, which is useful for prioritising outreach
but not good enough to act on blindly.

**Limitations?**
No dates, so no trends. The model shows correlation, not cause: electronic check users may churn for a
reason that has nothing to do with the payment method. Tenure, monthly and total charges are tightly
linked, so I would not read their individual coefficients too literally.

**What would you improve with more time?**
Try class weights or a lower threshold to raise recall, compare against a gradient boosted tree,
and put a cost on false alarms vs missed churners so the threshold is chosen on money rather than
on a default 50%.

**One line summary**
"Contract type and tenure explain most churn; a simple logistic regression gets 0.84 AUC and the
coefficients point at the same groups, so the business knows exactly who to call."
