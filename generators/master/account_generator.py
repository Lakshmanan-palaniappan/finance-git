"""
Account Generator
"""

import random
from datetime import date, timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.config import SIMULATION
from generators.common.id_generator import account_id

from generators.reference.account_rules import ACCOUNT_RULES


class AccountGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def generate_account_number(existing_numbers):

        while True:

            number = "".join(
                random.choices(
                    "0123456789",
                    k=12
                )
            )

            if number not in existing_numbers:

                existing_numbers.add(number)

                return number

    ###############################################################

    def generate(self):

        rows = []

        customers = self.context.customer_df

        if customers.empty:

            raise ValueError(
                "Customer data is empty. Run CustomerGenerator before AccountGenerator."
            )

        account_types = ACCOUNT_RULES["account_types"]

        statuses = ACCOUNT_RULES["status"]

        interest_rates = ACCOUNT_RULES["interest_rates"]

        balance_config = SIMULATION["master"].get(
            "account_balance",
            {
                "maximum": 2500000
            }
        )

        maximum_balance = balance_config["maximum"]

        account_numbers = set()

        for _, customer in customers.iterrows():

            customer_accounts = ["Savings"]

            if random.random() < 0.40:

                customer_accounts.append("Salary")

            if (
                customer.annual_income >= 800000
                and random.random() < 0.20
            ):

                customer_accounts.append("Current")

            for account_type in customer_accounts:

                minimum_balance = account_types[account_type]["min_balance"]

                balance = random.randint(
                    minimum_balance,
                    maximum_balance
                )

                opened_date = (
                    date.today()
                    - timedelta(
                        days=random.randint(
                            30,
                            3650
                        )
                    )
                )

                rows.append({

                    "account_id": account_id(),

                    "account_number": self.generate_account_number(
                        account_numbers
                    ),

                    "customer_id": customer.customer_id,

                    "branch_id": customer.branch_id,

                    "account_type": account_type,

                    "balance": balance,

                    "minimum_balance": minimum_balance,

                    "interest_rate": interest_rates[account_type],

                    "opened_date": opened_date,

                    "account_status": random.choices(

                        statuses,

                        weights=[
                            92,
                            6,
                            2
                        ]

                    )[0]

                })

        dataframe = pd.DataFrame(rows)

        self.context.account_df = dataframe

        self.context.account_lookup = {

            row.account_id: row

            for _, row in dataframe.iterrows()

        }

        return dataframe