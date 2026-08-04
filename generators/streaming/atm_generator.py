"""
ATM Transaction Generator
"""

import random
from datetime import datetime

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import atm_transaction_id


class ATMGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def generate_atm_id():

        return f"ATM{random.randint(10000,99999)}"

    ###############################################################

    def generate(self):

        rows = []

        account_df = self.context.account_df

        card_df = self.context.card_df

        debit_cards = card_df[
            card_df.card_type == "Debit"
        ]

        if debit_cards.empty:

            return pd.DataFrame()

        sample_size = min(
            len(debit_cards),
            200
        )

        sampled_cards = debit_cards.sample(sample_size)

        for _, card in sampled_cards.iterrows():

            account_index = account_df[
                account_df.account_id == card.account_id
            ].index

            if len(account_index) == 0:
                continue

            idx = account_index[0]

            balance = float(
                account_df.at[idx, "balance"]
            )

            amount = random.randint(
                100,
                20000
            )

            status = "SUCCESS"

            if balance >= amount:

                balance -= amount

            else:

                status = "FAILED"

                amount = 0

            account_df.at[idx, "balance"] = balance

            fraud_flag = False

            if amount >= 10000:

                fraud_flag = True

            rows.append({

                "atm_transaction_id":
                    atm_transaction_id(),

                "card_id":
                    card.card_id,

                "account_id":
                    card.account_id,

                "customer_id":
                    card.customer_id,

                "atm_id":
                    self.generate_atm_id(),

                "withdrawal_amount":
                    amount,

                "available_balance":
                    balance,

                "status":
                    status,

                "fraud_flag":
                    fraud_flag,

                "transaction_timestamp":
                    datetime.now()

            })

        self.context.account_df = account_df

        return pd.DataFrame(rows)