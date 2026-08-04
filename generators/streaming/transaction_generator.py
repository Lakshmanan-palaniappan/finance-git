"""
Transaction Generator
"""

import random
from datetime import datetime

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.config import SIMULATION
from generators.common.account_service import AccountService
from generators.common.id_generator import transaction_id

from generators.reference.transaction_rules import TRANSACTION_RULES


class TransactionGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.account_service = AccountService(context)

    ###############################################################

    def generate(self):

        rows = []

        rules = TRANSACTION_RULES

        transaction_types = list(
            rules["transaction_types"].keys()
        )

        channels = rules["channels"]

        streaming = SIMULATION["streaming"]

        batch_size = min(

            streaming["transaction_batch_size"],

            len(self.context.account_df)

        )

        sampled = self.context.account_df.sample(batch_size)

        for index, account in sampled.iterrows():

            txn_type = random.choice(transaction_types)

            limits = rules["transaction_types"][txn_type]

            amount = random.randint(

                limits["min_amount"],

                limits["max_amount"]

            )

            txn_id = transaction_id()

            success = self.account_service.update_balance(

                account_index=index,

                amount=amount,

                transaction_id=txn_id,

                operation=txn_type

            )

            updated_balance = self.context.account_df.at[
                index,
                "balance"
            ]

            status = "SUCCESS" if success else "FAILED"

            fraud = (

                amount >= streaming["high_value_transaction"]

                and

                random.random()
                < streaming["fraud_probability"]

            )

            rows.append({

                "transaction_id": txn_id,

                "account_id": account.account_id,

                "customer_id": account.customer_id,

                "transaction_type": txn_type,

                "amount": amount,

                "balance_after_transaction": updated_balance,

                "channel": random.choice(channels),

                "status": status,

                "fraud_flag": fraud,

                "transaction_timestamp": datetime.now()

            })

        dataframe = pd.DataFrame(rows)

        self.context.transaction_df = dataframe

        return dataframe