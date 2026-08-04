"""
Branch Generator
"""

import random

import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import branch_id
from generators.common.config import SIMULATION

from generators.reference.banks import BANKS
from generators.reference.branches import BRANCHES
from generators.reference.cities import CITIES


class BranchGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

    ###############################################################

    def generate(self):

        rows = []

        bank = BANKS["bank"]

        ifsc_prefix = bank["ifsc_prefix"]

        number_of_branches = SIMULATION["master"]["branches"]

        used_ifsc = set()

        cities = CITIES["cities"]

        for _ in range(number_of_branches):

            city = random.choice(cities)

            city_name = city["city"]

            state = city["state"]

            zone = city["zone"]

            branch_name = random.choice(
                BRANCHES["branches"][city_name]
            )

            while True:

                branch_code = random.randint(
                    1000,
                    9999
                )

                ifsc = (
                    f"{ifsc_prefix}"
                    f"{branch_code}"
                )

                if ifsc not in used_ifsc:

                    used_ifsc.add(ifsc)

                    break

            rows.append({

                "branch_id": branch_id(),

                "branch_name": branch_name,

                "branch_code": branch_code,

                "ifsc_code": ifsc,

                "bank_name": bank["name"],

                "city": city_name,

                "state": state,

                "zone": zone,

                "country": bank.get("country", "India"),

                "status": "ACTIVE"

            })

        dataframe = pd.DataFrame(rows)

        self.context.branch_df = dataframe

        self.context.branch_lookup = {

            row.branch_id: row

            for _, row in dataframe.iterrows()

        }

        return dataframe