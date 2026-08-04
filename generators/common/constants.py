"""
Project Constants
"""

DATE_FORMAT = "%Y-%m-%d"

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

CURRENCY = "INR"

COUNTRY = "India"

CSV_EXTENSION = ".csv"

ENCODING = "utf-8"

OVERWRITE = True

MASTER_DATASETS = [

    "branches",
    "customers",
    "accounts",
    "cards",
    "loans",
    "customer_kyc",
    "exchange_rates"

]

STREAMING_DATASETS = [

    "transactions",
    "atm_transactions",
    "login_activity"

]