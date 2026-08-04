from datetime import date

import pandas as pd


def generate():

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

            "exchange_rate": 0.043,

            "effective_date": date.today()

        },

        {

            "base_currency": "INR",

            "target_currency": "SGD",

            "exchange_rate": 0.015,

            "effective_date": date.today()

        }

    ]

    return pd.DataFrame(rows)