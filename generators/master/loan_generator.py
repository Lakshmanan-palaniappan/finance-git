import random
from datetime import date, timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import loan_id

from generators.reference.loan_rules import LOAN_RULES


def generate(
    context: GenerationContext
):

    rows = []

    rules = LOAN_RULES["loan_types"]

    statuses = LOAN_RULES["status"]

    for customer in context.customer_ids:

        if random.random() < 0.35:

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
                random.uniform(7.5, 13.5),
                2
            )

            years = tenure

            emi = round(
                amount /
                (years * 12),
                2
            )

            lid = loan_id()

            context.loan_ids.append(lid)

            rows.append({

                "loan_id": lid,

                "customer_id": customer,

                "branch_id":
                    random.choice(
                        context.branch_ids
                    ),

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

                "sanction_date":
                    date.today() -
                    timedelta(
                        days=random.randint(
                            100,
                            3000
                        )
                    ),

                "status":
                    random.choice(statuses)

            })

    df = pd.DataFrame(rows)

    context.loan_df = df

    return df