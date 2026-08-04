"""
Loan Generator
"""

import math
import random
from datetime import date, timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import loan_id

from generators.reference.loan_rules import LOAN_RULES


class LoanGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def calculate_emi(
        principal,
        annual_rate,
        tenure_years
    ):

        months = tenure_years * 12

        monthly_rate = annual_rate / 12 / 100

        emi = (

            principal

            * monthly_rate

            * math.pow(
                1 + monthly_rate,
                months
            )

        ) / (

            math.pow(
                1 + monthly_rate,
                months
            ) - 1

        )

        return round(emi, 2)

    ###############################################################

    def generate(self):

        rows = []

        customers = self.context.customer_df

        rules = LOAN_RULES["loan_types"]

        statuses = LOAN_RULES["status"]

        for _, customer in customers.iterrows():

            income = customer.annual_income

            # ------------------------------
            # Loan Eligibility
            # ------------------------------

            probability = 0.15

            if income > 700000:
                probability = 0.30

            if income > 1500000:
                probability = 0.50

            if random.random() > probability:
                continue

            loan_type = random.choice(
                list(rules.keys())
            )

            rule = rules[loan_type]

            amount = random.randint(

                rule["min_amount"],

                rule["max_amount"]

            )

            tenure = random.choice(
                rule["tenure_years"]
            )

            rate = round(
                random.uniform(
                    7.5,
                    12.5
                ),
                2
            )

            emi = self.calculate_emi(

                amount,

                rate,

                tenure

            )

            total_months = tenure * 12

            paid = random.randint(
                0,
                total_months
            )

            remaining = total_months - paid

            outstanding = round(

                emi * remaining,

                2

            )

            sanction_date = (

                date.today()

                - timedelta(

                    days=random.randint(
                        30,
                        3650
                    )

                )

            )

            rows.append({

                "loan_id": loan_id(),

                "customer_id":
                    customer.customer_id,

                "branch_id":
                    customer.branch_id,

                "loan_type":
                    loan_type,

                "loan_amount":
                    amount,

                "interest_rate":
                    rate,

                "tenure_years":
                    tenure,

                "monthly_emi":
                    emi,

                "paid_emi":
                    paid,

                "remaining_emi":
                    remaining,

                "outstanding_balance":
                    outstanding,

                "loan_to_income_ratio":
                    round(
                        amount / income,
                        2
                    ),

                "sanction_date":
                    sanction_date,

                "status":
                    random.choices(

                        statuses,

                        weights=[
                            85,
                            10,
                            5
                        ]

                    )[0]

            })

        dataframe = pd.DataFrame(rows)

        self.context.loan_df = dataframe

        self.context.loan_lookup = {

            row.loan_id: row

            for _, row in dataframe.iterrows()

        }

        return dataframe