"""
Card Generator
"""

import random
from datetime import date, timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import card_id

from generators.reference.card_rules import CARD_RULES


class CardGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def generate_card_number():

        return "".join(
            random.choices(
                "0123456789",
                k=16
            )
        )

    ###############################################################

    @staticmethod
    def generate_cvv():

        return "".join(
            random.choices(
                "0123456789",
                k=3
            )
        )

    ###############################################################

    def calculate_credit_limit(self, income):

        if income < 500000:
            return 50000

        if income < 1000000:
            return 100000

        if income < 2000000:
            return 250000

        if income < 5000000:
            return 500000

        return 1000000

    ###############################################################

    def generate(self):

        rows = []

        networks = CARD_RULES["networks"]

        statuses = CARD_RULES["status"]

        account_df = self.context.account_df

        customer_df = self.context.customer_df

        customer_lookup = {

            row.customer_id: row

            for _, row in customer_df.iterrows()

        }

        for _, account in account_df.iterrows():

            customer = customer_lookup[
                account.customer_id
            ]

            # ------------------------------------------------------
            # Debit Card
            # Savings and Salary accounts always get Debit cards
            # ------------------------------------------------------

            if account.account_type in [
                "Savings",
                "Salary"
            ]:

                rows.append({

                    "card_id": card_id(),

                    "account_id": account.account_id,

                    "customer_id": account.customer_id,

                    "card_number": self.generate_card_number(),

                    "card_type": "Debit",

                    "network": random.choice(networks),

                    "credit_limit": 0,

                    "daily_limit":
                        CARD_RULES["card_types"]["Debit"]["daily_limit"],

                    "cvv": self.generate_cvv(),

                    "issue_date":
                        account.opened_date,

                    "expiry_date":
                        account.opened_date +
                        timedelta(days=5 * 365),

                    "status":
                        random.choices(
                            statuses,
                            weights=[92, 5, 3]
                        )[0]

                })

            # ------------------------------------------------------
            # Credit Card
            # Higher income customers only
            # ------------------------------------------------------

            if (

                customer.annual_income > 700000

                and random.random() < 0.45

            ):

                rows.append({

                    "card_id": card_id(),

                    "account_id": account.account_id,

                    "customer_id": account.customer_id,

                    "card_number": self.generate_card_number(),

                    "card_type": "Credit",

                    "network": random.choice(networks),

                    "credit_limit":
                        self.calculate_credit_limit(
                            customer.annual_income
                        ),

                    "daily_limit":
                        CARD_RULES["card_types"]["Credit"]["daily_limit"],

                    "cvv": self.generate_cvv(),

                    "issue_date":
                        account.opened_date,

                    "expiry_date":
                        account.opened_date +
                        timedelta(days=5 * 365),

                    "status":
                        random.choices(
                            statuses,
                            weights=[94, 3, 3]
                        )[0]

                })

        dataframe = pd.DataFrame(rows)

        self.context.card_df = dataframe

        self.context.card_lookup = {

            row.card_id: row

            for _, row in dataframe.iterrows()

        }

        return dataframe