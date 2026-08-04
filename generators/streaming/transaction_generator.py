import random
from datetime import datetime

import pandas as pd

from generators.common.base_generator import BaseGenerator
from generators.common.id_generator import transaction_id
from generators.reference.transaction_rules import TRANSACTION_RULES


class TransactionGenerator(BaseGenerator):

    dataset_name = "transactions"

    def generate(self):

        rows = []

        rules = TRANSACTION_RULES

        account_df = self.context.account_df

        transaction_types = list(
            rules["transaction_types"].keys()
        )

        statuses = rules["status"]

        channels = rules["channels"]

        sample = account_df.sample(
            min(500, len(account_df))
        )

        for _, account in sample.iterrows():

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

                "channel":
                    random.choice(channels),

                "status":
                    random.choice(statuses),

                "transaction_timestamp":
                    datetime.now()

            })

        return pd.DataFrame(rows)