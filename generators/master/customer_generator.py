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

        number_of_customers = SIMULATION["master"]["customers"]

        income_config = SIMULATION["master"].get(
            "customer_income",
            {
                "minimum": 250000,
                "maximum": 5000000
            }
        )

        branches = self.context.branch_df

        if branches.empty:

            raise ValueError(
                "Branch data is empty. Run BranchGenerator before CustomerGenerator."
            )

        occupations = OCCUPATIONS["occupations"]

        cities = CITIES["cities"]

        for _ in range(number_of_customers):

            branch = branches.sample(1).iloc[0]

            city = random.choice(cities)

            rows.append({

                "customer_id": customer_id(),

                "branch_id": branch.branch_id,

                "first_name": fake.first_name(),

                "last_name": fake.last_name(),

                "gender": random.choices(
                    [
                        "Male",
                        "Female"
                    ],
                    weights=[
                        51,
                        49
                    ]
                )[0],

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
                    income_config["minimum"],
                    income_config["maximum"]
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