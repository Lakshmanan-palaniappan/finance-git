"""
Transaction Generator
"""

import random
from datetime import datetime

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.config import SIMULATION
from generators.common.id_generator import transaction_id

from generators.reference.transaction_rules import TRANSACTION_RULES


class TransactionGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    def generate(self):

        rows = []

        account_df = self.context.account_df

        if account_df.empty:

            raise ValueError(
                "Account data is empty. Run AccountGenerator before TransactionGenerator."
            )

        transaction_rules = TRANSACTION_RULES["transaction_types"]

        transaction_types = list(transaction_rules.keys())

        channels = TRANSACTION_RULES["channels"]

        streaming = SIMULATION["streaming"]

        batch_size = streaming["transaction_batch_size"]

        fraud_threshold = streaming["high_value_transaction"]

        sample_size = min(

            len(account_df),

            batch_size

        )

        sampled_accounts = account_df.sample(sample_size)

        for idx, account in sampled_accounts.iterrows():

            transaction_type = random.choice(
                transaction_types
            )

            limits = transaction_rules[
                transaction_type
            ]

            amount = random.randint(

                limits["min_amount"],

                limits["max_amount"]

            )

            balance = float(account.balance)

            status = "SUCCESS"

            if transaction_type in [

                "Withdrawal",

                "ATM",

                "Transfer",

                "UPI"

            ]:

                if balance >= amount:

                    balance -= amount

                else:

                    status = "FAILED"

            else:

                balance += amount

            account_df.at[idx, "balance"] = balance

            rows.append({

                "transaction_id":
                    transaction_id(),

                "account_id":
                    account.account_id,

                "customer_id":
                    account.customer_id,

                "transaction_type":
                    transaction_type,

                "amount":
                    amount,

                "balance_after_transaction":
                    balance,

                "channel":
                    random.choice(channels),

                "status":
                    status,

                "fraud_flag":
                    amount >= fraud_threshold,

                "transaction_timestamp":
                    datetime.now()

            })

        self.context.account_df = account_df

        dataframe = pd.DataFrame(rows)

        self.context.transaction_df = dataframe

        return dataframe