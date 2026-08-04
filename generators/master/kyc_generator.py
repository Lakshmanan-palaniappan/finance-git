"""
KYC Generator
"""

import random
from datetime import date, timedelta

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import kyc_id


DOCUMENT_TYPES = [
    "AADHAAR",
    "PAN",
    "PASSPORT",
    "DRIVING_LICENSE"
]


class KYCGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    @staticmethod
    def generate_employee_id():

        return f"EMP{random.randint(1000, 9999)}"

    ###############################################################

    def generate(self):

        rows = []

        customers = self.context.customer_df

        if customers.empty:

            raise ValueError(
                "Customer data is empty. Run CustomerGenerator before KYCGenerator."
            )

        for _, customer in customers.iterrows():

            status = random.choices(

                [
                    "VERIFIED",
                    "PENDING",
                    "REJECTED"
                ],

                weights=[
                    92,
                    6,
                    2
                ]

            )[0]

            verification_date = (

                date.today()

                - timedelta(

                    days=random.randint(
                        1,
                        365
                    )

                )

            )

            rows.append({

                "kyc_id": kyc_id(),

                "customer_id": customer.customer_id,

                "document_type": random.choice(
                    DOCUMENT_TYPES
                ),

                "pan_number": customer.pan_number,

                "aadhaar_number": customer.aadhaar_number,

                "verification_date": verification_date,

                "verified_by": self.generate_employee_id(),

                "status": status

            })

        dataframe = pd.DataFrame(rows)

        self.context.customer_kyc_df = dataframe

        return dataframe