"""
ID Generator
"""

import uuid


def _generate(prefix: str, length: int):

    return f"{prefix}{uuid.uuid4().hex[:length].upper()}"


def customer_id():

    return _generate("CUST", 10)


def account_id():

    return _generate("ACC", 10)


def transaction_id():

    return _generate("TXN", 12)


def card_id():

    return _generate("CARD", 10)


def loan_id():

    return _generate("LOAN", 10)


def branch_id():

    return _generate("BR", 6)


def kyc_id():

    return _generate("KYC", 10)


def atm_transaction_id():

    return _generate("ATM", 12)


def login_id():

    return _generate("LOGIN", 10)