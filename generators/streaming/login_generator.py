"""
Login Activity Generator
"""

import random
from datetime import datetime

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import login_id


DEVICES = [
    "Android",
    "iPhone",
    "Windows",
    "MacBook",
    "iPad"
]

BROWSERS = [
    "Chrome",
    "Edge",
    "Safari",
    "Firefox"
]


class LoginGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def generate_ip():

        return ".".join(
            str(random.randint(1, 255))
            for _ in range(4)
        )

    ###############################################################

    @staticmethod
    def calculate_risk(status, failed_count, new_device):

        score = 0

        if status == "FAILED":
            score += 40

        score += failed_count * 10

        if new_device:
            score += 20

        return min(score, 100)

    ###############################################################

    def generate(self):

        rows = []

        customers = self.context.customer_df

        sample_size = min(
            len(customers),
            300
        )

        sampled = customers.sample(sample_size)

        for _, customer in sampled.iterrows():

            status = random.choices(

                [

                    "SUCCESS",

                    "FAILED"

                ],

                weights=[92, 8]

            )[0]

            failed_count = 0

            if status == "FAILED":

                failed_count = random.randint(
                    1,
                    5
                )

            new_device = random.random() < 0.15

            risk_score = self.calculate_risk(

                status,

                failed_count,

                new_device

            )

            rows.append({

                "login_id":
                    login_id(),

                "customer_id":
                    customer.customer_id,

                "device":
                    random.choice(
                        DEVICES
                    ),

                "browser":
                    random.choice(
                        BROWSERS
                    ),

                "ip_address":
                    self.generate_ip(),

                "city":
                    customer.city,

                "status":
                    status,

                "failed_login_count":
                    failed_count,

                "new_device":
                    new_device,

                "risk_score":
                    risk_score,

                "login_timestamp":
                    datetime.now()

            })

        return pd.DataFrame(rows)