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

KYC_STATUS = [
    "VERIFIED",
    "PENDING",
    "REJECTED"
]


def generate(context: GenerationContext):

    rows = []

    customer_df = context.customer_df

    for _, customer in customer_df.iterrows():

        kid = kyc_id()

        status = random.choices(
            KYC_STATUS,
            weights=[85, 10, 5],
            k=1
        )[0]

        rows.append({

            "kyc_id": kid,

            "customer_id": customer.customer_id,

            "document_type": random.choice(
                DOCUMENT_TYPES
            ),

            "pan_number": customer.pan_number,

            "aadhaar_number": customer.aadhaar_number,

            "verification_date":
                date.today() -
                timedelta(
                    days=random.randint(1, 1000)
                ),

            "verified_by":
                f"EMP{random.randint(1000,9999)}",

            "status": status

        })

    df = pd.DataFrame(rows)

    context.kyc_df = df

    return df