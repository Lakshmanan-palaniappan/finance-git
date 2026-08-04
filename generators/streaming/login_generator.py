"""
Login Activity Generator
"""

import random
from datetime import datetime

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.config import SIMULATION
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
    def calculate_risk(
        status,
        failed_count,
        new_device
    ):

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

        if customers.empty:

            raise ValueError(
                "Customer data is empty. Run CustomerGenerator before LoginGenerator."
            )

        streaming = SIMULATION["streaming"]

        batch_size = streaming["login_batch_size"]

        failed_probability = streaming["failed_login_probability"]

        new_device_probability = streaming.get(
            "new_device_probability",
            0.15
        )

        sample_size = min(
            len(customers),
            batch_size
        )

        sampled = customers.sample(sample_size)

        for _, customer in sampled.iterrows():

            status = random.choices(

                [
                    "SUCCESS",
                    "FAILED"
                ],

                weights=[
                    1 - failed_probability,
                    failed_probability
                ]

            )[0]

            failed_count = 0

            if status == "FAILED":

                failed_count = random.randint(
                    1,
                    5
                )

            new_device = (
                random.random()
                < new_device_probability
            )

            risk_score = self.calculate_risk(

                status,

                failed_count,

                new_device

            )

            rows.append({

                "login_id": login_id(),

                "customer_id": customer.customer_id,

                "device": random.choice(
                    DEVICES
                ),

                "browser": random.choice(
                    BROWSERS
                ),

                "ip_address": self.generate_ip(),

                "city": customer.city,

                "status": status,

                "failed_login_count": failed_count,

                "new_device": new_device,

                "risk_score": risk_score,

                "login_timestamp": datetime.now()

            })

        dataframe = pd.DataFrame(rows)

        self.context.login_activity_df = dataframe

        return dataframe