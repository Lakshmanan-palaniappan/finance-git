"""
Card Generator
"""

import random
from datetime import timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.config import SIMULATION
from generators.common.id_generator import card_id

from generators.reference.card_rules import CARD_RULES


class CardGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def generate_card_number(existing_numbers):

        while True:

            number = "".join(
                random.choices(
                    "0123456789",
                    k=16
                )
            )

            if number not in existing_numbers:

                existing_numbers.add(number)

                return number

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

    @staticmethod
    def calculate_credit_limit(income):

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

        account_df = self.context.account_df

        customer_df = self.context.customer_df

        if account_df.empty:

            raise ValueError(
                "Account data is empty. Run AccountGenerator before CardGenerator."
            )

        if customer_df.empty:

            raise ValueError(
                "Customer data is empty. Run CustomerGenerator before CardGenerator."
            )

        customer_lookup = {

            row.customer_id: row

            for _, row in customer_df.iterrows()

        }

        networks = CARD_RULES["networks"]

        statuses = CARD_RULES["status"]

        debit_limit = CARD_RULES["card_types"]["Debit"]["daily_limit"]

        credit_limit_daily = CARD_RULES["card_types"]["Credit"]["daily_limit"]

        credit_income_threshold = SIMULATION["master"].get(
            "credit_card_income",
            700000
        )

        generated_numbers = set()

        for _, account in account_df.iterrows():

            customer = customer_lookup[account.customer_id]

            # --------------------------------------------------
            # Debit Card
            # --------------------------------------------------

            if account.account_type in [

                "Savings",

                "Salary"

            ]:

                rows.append({

                    "card_id": card_id(),

                    "account_id": account.account_id,

                    "customer_id": account.customer_id,

                    "card_number": self.generate_card_number(
                        generated_numbers
                    ),

                    "card_type": "Debit",

                    "network": random.choice(networks),

                    "credit_limit": 0,

                    "daily_limit": debit_limit,

                    "cvv": self.generate_cvv(),

                    "issue_date": account.opened_date,

                    "expiry_date": (
                        account.opened_date
                        + timedelta(days=5 * 365)
                    ),

                    "status": random.choices(

                        statuses,

                        weights=[92, 5, 3]

                    )[0]

                })

            # --------------------------------------------------
            # Credit Card
            # --------------------------------------------------

            if (

                customer.annual_income >= credit_income_threshold

                and random.random() < 0.45

            ):

                rows.append({

                    "card_id": card_id(),

                    "account_id": account.account_id,

                    "customer_id": account.customer_id,

                    "card_number": self.generate_card_number(
                        generated_numbers
                    ),

                    "card_type": "Credit",

                    "network": random.choice(networks),

                    "credit_limit": self.calculate_credit_limit(
                        customer.annual_income
                    ),

                    "daily_limit": credit_limit_daily,

                    "cvv": self.generate_cvv(),

                    "issue_date": account.opened_date,

                    "expiry_date": (
                        account.opened_date
                        + timedelta(days=5 * 365)
                    ),

                    "status": random.choices(

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