import random
from datetime import date, timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import card_id

from generators.reference.card_rules import CARD_RULES


def generate(
    context: GenerationContext
):

    rows = []

    card_types = CARD_RULES["card_types"]

    networks = CARD_RULES["networks"]

    statuses = CARD_RULES["status"]

    for _, account in context.account_df.iterrows():

        if random.random() < 0.85:

            cid = card_id()

            context.card_ids.append(cid)

            ctype = random.choice(
                list(card_types.keys())
            )

            rows.append({

                "card_id": cid,

                "account_id":
                    account.account_id,

                "customer_id":
                    account.customer_id,

                "card_type":
                    ctype,

                "network":
                    random.choice(networks),

                "daily_limit":
                    card_types[ctype][
                        "daily_limit"
                    ],

                "issue_date":
                    date.today() -
                    timedelta(
                        days=random.randint(
                            30,
                            2000
                        )
                    ),

                "expiry_date":
                    date.today() +
                    timedelta(days=1825),

                "status":
                    random.choice(statuses)

            })

    df = pd.DataFrame(rows)

    context.card_df = df

    return df