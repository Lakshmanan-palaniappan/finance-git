import random
from datetime import date, timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import account_id
from generators.reference.account_rules import ACCOUNT_RULES


def generate(
    context: GenerationContext,
    max_accounts_per_customer=3
):

    rows = []

    account_ids = []

    account_types = ACCOUNT_RULES["account_types"]

    statuses = ACCOUNT_RULES["status"]

    interest_rates = ACCOUNT_RULES["interest_rates"]

    for customer in context.customer_ids:

        number_of_accounts = random.randint(
            1,
            max_accounts_per_customer
        )

        for _ in range(number_of_accounts):

            acc_type = random.choice(
                list(account_types.keys())
            )

            aid = account_id()

            account_ids.append(aid)

            context.account_ids.append(aid)

            minimum_balance = account_types[
                acc_type
            ]["min_balance"]

            balance = random.randint(
                minimum_balance,
                2000000
            )

            rows.append({

                "account_id": aid,

                "customer_id": customer,

                "branch_id": random.choice(
                    context.branch_ids
                ),

                "account_type": acc_type,

                "balance": balance,

                "interest_rate":
                    interest_rates[acc_type],

                "opened_date":
                    date.today() -
                    timedelta(
                        days=random.randint(30, 3650)
                    ),

                "status":
                    random.choice(statuses)

            })

    df = pd.DataFrame(rows)

    context.account_df = df

    return df