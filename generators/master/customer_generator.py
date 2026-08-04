import random
import string

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import customer_id
from generators.common.faker_provider import fake

from generators.reference.occupations import OCCUPATIONS
from generators.reference.cities import CITIES


def generate(
        context: GenerationContext,
        records=5000
):

    rows=[]

    occupations=OCCUPATIONS["occupations"]

    cities=CITIES["cities"]

    for _ in range(records):

        cid=customer_id()

        context.customer_ids.append(cid)

        city=random.choice(cities)

        pan=''.join(random.choices(string.ascii_uppercase,k=5)) + \
            ''.join(random.choices(string.digits,k=4)) + \
            random.choice(string.ascii_uppercase)

        aadhaar="".join(
            random.choices(
                string.digits,
                k=12
            )
        )

        rows.append({

            "customer_id":cid,

            "branch_id":random.choice(
                context.branch_ids
            ),

            "first_name":fake.first_name(),

            "last_name":fake.last_name(),

            "gender":random.choice([
                "Male",
                "Female"
            ]),

            "dob":fake.date_of_birth(
                minimum_age=18,
                maximum_age=80
            ),

            "mobile_number":"9"+''.join(
                random.choices(
                    string.digits,
                    k=9
                )
            ),

            "email":fake.email(),

            "pan_number":pan,

            "aadhaar_number":aadhaar,

            "occupation":random.choice(
                occupations
            ),

            "annual_income":random.randint(
                300000,
                3000000
            ),

            "city":city["city"],

            "state":city["state"],

            "status":"ACTIVE"

        })

    df=pd.DataFrame(rows)

    context.customer_df=df

    return df