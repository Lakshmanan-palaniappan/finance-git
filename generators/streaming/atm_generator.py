"""
ATM Transaction Generator
"""

import random
from datetime import datetime

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.account_service import AccountService
from generators.common.config import SIMULATION
from generators.common.id_generator import atm_transaction_id


class ATMGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.account_service = AccountService(context)

    ###############################################################

    @staticmethod
    def generate_atm_id():

        return f"ATM{random.randint(10000,99999)}"

    ###############################################################

    def generate(self):

        rows = []

        card_df = self.context.card_df

        debit_cards = card_df[
            card_df.card_type == "Debit"
        ]

        if debit_cards.empty:

            dataframe = pd.DataFrame()

            self.context.atm_transaction_df = dataframe

            return dataframe

        streaming = SIMULATION["streaming"]

        batch_size = min(

            streaming["atm_batch_size"],

            len(debit_cards)

        )

        sampled = debit_cards.sample(batch_size)

        for _, card in sampled.iterrows():

            account_rows = self.context.account_df[

                self.context.account_df.account_id
                == card.account_id

            ]

            if account_rows.empty:

                continue

            index = account_rows.index[0]

            amount = random.randint(

                streaming["atm"]["minimum_amount"],

                streaming["atm"]["maximum_amount"]

            )

            txn_id = atm_transaction_id()

            success = self.account_service.update_balance(

                account_index=index,

                amount=amount,

                transaction_id=txn_id,

                operation="ATM"

            )

            balance = self.context.account_df.at[
                index,
                "balance"
            ]

            fraud = (

                amount >= streaming["atm_high_value"]

                and

                random.random()
                < streaming["fraud_probability"]

            )

            rows.append({

                "atm_transaction_id": txn_id,

                "card_id": card.card_id,

                "account_id": card.account_id,

                "customer_id": card.customer_id,

                "atm_id": self.generate_atm_id(),

                "withdrawal_amount": amount,

                "available_balance": balance,

                "status": "SUCCESS" if success else "FAILED",

                "fraud_flag": fraud,

                "transaction_timestamp": datetime.now()

            })

        dataframe = pd.DataFrame(rows)

        self.context.atm_transaction_df = dataframe

        return dataframe