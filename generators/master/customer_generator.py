"""
Customer Generator
"""

import random
import string

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.config import SIMULATION
from generators.common.faker_provider import fake
from generators.common.id_generator import customer_id

from generators.reference.cities import CITIES
from generators.reference.occupations import OCCUPATIONS


class CustomerGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def generate_pan():

        return (
            "".join(random.choices(string.ascii_uppercase, k=5))
            + "".join(random.choices(string.digits, k=4))
            + random.choice(string.ascii_uppercase)
        )

    ###############################################################

    @staticmethod
    def generate_aadhaar():

        return "".join(random.choices(string.digits, k=12))

    ###############################################################

    def generate(self):

        rows = []

        customers = SIMULATION["master"]["customers"]

        branches = self.context.branch_df

        occupations = OCCUPATIONS["occupations"]

        cities = CITIES["cities"]

        for _ in range(customers):

            branch = branches.sample(1).iloc[0]

            city = random.choice(cities)

            rows.append({

                "customer_id": customer_id(),

                "branch_id": branch.branch_id,

                "first_name": fake.first_name(),

                "last_name": fake.last_name(),

                "gender": random.choice(
                    [
                        "Male",
                        "Female"
                    ]
                ),

                "dob": fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=80
                ),

                "mobile_number": (
                    "9"
                    + "".join(
                        random.choices(
                            string.digits,
                            k=9
                        )
                    )
                ),

                "email": fake.email(),

                "pan_number": self.generate_pan(),

                "aadhaar_number": self.generate_aadhaar(),

                "occupation": random.choice(
                    occupations
                ),

                "annual_income": random.randint(
                    250000,
                    5000000
                ),

                "city": city["city"],

                "state": city["state"],

                "customer_status": random.choices(
                    [
                        "ACTIVE",
                        "INACTIVE",
                        "BLOCKED"
                    ],
                    weights=[
                        92,
                        6,
                        2
                    ]
                )[0]

            })

        dataframe = pd.DataFrame(rows)

        self.context.customer_df = dataframe

        self.context.customer_lookup = {

            row.customer_id: row

            for _, row in dataframe.iterrows()

        }

        return dataframe