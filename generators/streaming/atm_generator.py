import random
from datetime import datetime

import pandas as pd

from generators.common.base_generator import BaseGenerator
from generators.common.id_generator import atm_transaction_id


class ATMGenerator(BaseGenerator):

    dataset_name = "atm_transactions"

    def generate(self):

        rows = []

        cards = self.context.card_df

        debit_cards = cards[
            cards.card_type == "Debit"
        ]

        sample = debit_cards.sample(
            min(200, len(debit_cards))
        )

        for _, card in sample.iterrows():

            rows.append({

                "atm_transaction_id":
                    atm_transaction_id(),

                "card_id":
                    card.card_id,

                "account_id":
                    card.account_id,

                "customer_id":
                    card.customer_id,

                "amount":
                    random.randint(
                        100,
                        20000
                    ),

                "status":
                    random.choice(
                        [
                            "SUCCESS",
                            "FAILED"
                        ]
                    ),

                "atm_id":
                    f"ATM{random.randint(1000,9999)}",

                "timestamp":
                    datetime.now()

            })

        return pd.DataFrame(rows)