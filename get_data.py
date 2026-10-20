"""Download the Telco Customer Churn CSV into data/ if it is not already there.

The file is small (about 1 MB). It comes from IBM's public sample repository on GitHub,
which is the same file that is published on Kaggle as "Telco Customer Churn".
"""
import os
import urllib.request

URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
TARGET = os.path.join("data", "Telco-Customer-Churn.csv")

if os.path.exists(TARGET):
    print(f"{TARGET} already exists, nothing to do")
else:
    os.makedirs("data", exist_ok=True)
    print(f"downloading {URL} ...")
    urllib.request.urlretrieve(URL, TARGET)
    print(f"saved to {TARGET}")
