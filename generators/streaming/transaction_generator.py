"""
Transaction Generator
"""

import random
from datetime import datetime

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import transaction_id

from generators.reference.transaction_rules import TRANSACTION_RULES


class TransactionGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    def generate(self):

        rows = []

        rules = TRANSACTION_RULES

        transaction_types = list(
            rules["transaction_types"].keys()
        )

        channels = rules["channels"]

        account_df = self.context.account_df

        batch_size = min(
            len(account_df),
            500
        )

        sampled_accounts = account_df.sample(batch_size)

        for idx, account in sampled_accounts.iterrows():

            txn_type = random.choice(
                transaction_types
            )

            limits = rules["transaction_types"][
                txn_type
            ]

            amount = random.randint(
                limits["min_amount"],
                limits["max_amount"]
            )

            current_balance = float(account.balance)

            status = "SUCCESS"

            if txn_type in [
                "Withdrawal",
                "ATM",
                "Transfer",
                "UPI"
            ]:

                if current_balance >= amount:

                    current_balance -= amount

                else:

                    status = "FAILED"

            else:

                current_balance += amount

            account_df.at[idx, "balance"] = current_balance

            fraud = False

            if amount > 100000:

                fraud = True

            rows.append({

                "transaction_id":
                    transaction_id(),

                "account_id":
                    account.account_id,

                "customer_id":
                    account.customer_id,

                "transaction_type":
                    txn_type,

                "amount":
                    amount,

                "balance_after_transaction":
                    current_balance,

                "channel":
                    random.choice(channels),

                "status":
                    status,

                "fraud_flag":
                    fraud,

                "transaction_timestamp":
                    datetime.now()

            })

        self.context.account_df = account_df

        dataframe = pd.DataFrame(rows)

        return dataframe