import uuid


def customer_id():
    return f"CUST-{uuid.uuid4().hex[:10].upper()}"


def account_id():
    return f"ACC-{uuid.uuid4().hex[:10].upper()}"


def transaction_id():
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


def loan_id():
    return f"LOAN-{uuid.uuid4().hex[:10].upper()}"


def card_id():
    return f"CARD-{uuid.uuid4().hex[:10].upper()}"


def branch_id():
    return f"BR-{uuid.uuid4().hex[:6].upper()}"


def atm_transaction_id():
    return f"ATM-{uuid.uuid4().hex[:10].upper()}"


def login_id():
    return f"LOGIN-{uuid.uuid4().hex[:10].upper()}"