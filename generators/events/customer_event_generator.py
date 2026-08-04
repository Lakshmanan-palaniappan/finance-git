"""
Customer Event Generator
"""

import random

from generators.common.config import SIMULATION
from generators.common.context import GenerationContext
from generators.common.customer_service import CustomerService

from generators.reference.cities import CITIES
from generators.reference.occupations import OCCUPATIONS


class CustomerEventGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.service = CustomerService(context)

    ###############################################################

    @staticmethod
    def random_mobile():

        return "9" + "".join(
            random.choices("0123456789", k=9)
        )

    ###############################################################

    @staticmethod
    def random_email():

        return (
            f"user{random.randint(100000,999999)}"
            "@mail.com"
        )

    ###############################################################

    def generate(self):

        dataframe = self.context.customer_df

        if dataframe.empty:

            return

        updates = min(

            SIMULATION["streaming"]["customer_events"],

            len(dataframe)

        )

        for _ in range(updates):

            idx = random.choice(dataframe.index.tolist())

            attribute = random.choice([

                "mobile_number",

                "email",

                "city",

                "occupation"

            ])

            current = dataframe.at[idx, attribute]

            if attribute == "mobile_number":

                value = self.random_mobile()

            elif attribute == "email":

                value = self.random_email()

            elif attribute == "city":

                value = random.choice(
                    CITIES["cities"]
                )["city"]

            else:

                value = random.choice(
                    OCCUPATIONS["occupations"]
                )

            if value == current:

                continue

            self.service.update_attribute(

                customer_index=idx,

                attribute=attribute,

                new_value=value

            )