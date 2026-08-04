"""
Exchange Rate Generator
"""

from datetime import date

import pandas as pd

from generators.common.context import GenerationContext
from generators.reference.exchange_rates import EXCHANGE_RATES


class ExchangeRateGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    def generate(self):

        rows = []

        for rate in EXCHANGE_RATES["exchange_rates"]:

            rows.append({

                "base_currency": rate["base_currency"],

                "target_currency": rate["target_currency"],

                "exchange_rate": rate["exchange_rate"],

                "effective_date": date.today()

            })

        dataframe = pd.DataFrame(rows)

        self.context.exchange_rate_df = dataframe

        return dataframe