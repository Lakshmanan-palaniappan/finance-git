"""
Exchange Rate Generator
"""

from datetime import date

import pandas as pd


class ExchangeRateGenerator:

    def __init__(self, context):

        self.context = context

    ###############################################################

    def generate(self):

        rows = [

            {

                "base_currency": "INR",

                "target_currency": "USD",

                "exchange_rate": 0.0118,

                "effective_date": date.today()

            },

            {

                "base_currency": "INR",

                "target_currency": "EUR",

                "exchange_rate": 0.0109,

                "effective_date": date.today()

            },

            {

                "base_currency": "INR",

                "target_currency": "GBP",

                "exchange_rate": 0.0094,

                "effective_date": date.today()

            },

            {

                "base_currency": "INR",

                "target_currency": "AED",

                "exchange_rate": 0.0432,

                "effective_date": date.today()

            },

            {

                "base_currency": "INR",

                "target_currency": "SGD",

                "exchange_rate": 0.0157,

                "effective_date": date.today()

            }

        ]

        dataframe = pd.DataFrame(rows)

        self.context.exchange_rate_df = dataframe

        return dataframe