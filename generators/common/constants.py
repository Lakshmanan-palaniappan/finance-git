"""
Project-wide constants.
"""

# -------------------------
# Batch Sizes
# -------------------------

BRANCH_COUNT = 25

CUSTOMER_COUNT = 500

ACCOUNT_COUNT = 1000

LOAN_COUNT = 250

CARD_COUNT = 700

TRANSACTION_BATCH_SIZE = 500

ATM_BATCH_SIZE = 100

LOGIN_BATCH_SIZE = 300


# -------------------------
# Transaction Types
# -------------------------

TRANSACTION_TYPES = [
    "DEPOSIT",
    "WITHDRAWAL",
    "TRANSFER",
    "UPI",
    "NEFT",
    "RTGS",
    "IMPS"
]


ACCOUNT_TYPES = [
    "SAVINGS",
    "CURRENT",
    "SALARY"
]


CARD_TYPES = [
    "DEBIT",
    "CREDIT"
]


CARD_NETWORKS = [
    "VISA",
    "MASTERCARD",
    "RUPAY"
]


LOAN_TYPES = [
    "HOME",
    "CAR",
    "PERSONAL",
    "EDUCATION"
]


ACCOUNT_STATUS = [
    "ACTIVE",
    "INACTIVE"
]


CUSTOMER_STATUS = [
    "ACTIVE",
    "INACTIVE"
]


TRANSACTION_STATUS = [
    "SUCCESS",
    "FAILED"
]


LOGIN_STATUS = [
    "SUCCESS",
    "FAILED"
]


CURRENCY = [
    "INR"
]