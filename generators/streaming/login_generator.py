import random
from datetime import datetime

import pandas as pd

from generators.common.base_generator import BaseGenerator
from generators.common.id_generator import login_id


class LoginGenerator(BaseGenerator):

    dataset_name = "login_activity"

    def generate(self):

        rows = []

        customers = self.context.customer_df.sample(
            300
        )

        cities = [
            "Chennai",
            "Bengaluru",
            "Mumbai",
            "Delhi",
            "Hyderabad"
        ]

        for _, customer in customers.iterrows():

            rows.append({

                "login_id":
                    login_id(),

                "customer_id":
                    customer.customer_id,

                "city":
                    random.choice(cities),

                "device":
                    random.choice(
                        [
                            "Android",
                            "iPhone",
                            "Windows",
                            "Mac"
                        ]
                    ),

                "status":
                    random.choices(
                        [
                            "SUCCESS",
                            "FAILED"
                        ],
                        weights=[92,8]
                    )[0],

                "login_timestamp":
                    datetime.now()

            })

        return pd.DataFrame(rows)