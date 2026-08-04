import random
import pandas as pd

from generators.common.context import GenerationContext
from generators.common.id_generator import branch_id

from generators.reference.cities import CITIES
from generators.reference.banks import BANKS
from generators.reference.branches import BRANCHES


def generate(
    context: GenerationContext,
    records=50
):

    rows = []

    bank = BANKS["bank"]

    ifsc_prefix = bank["ifsc_prefix"]

    cities = CITIES["cities"]

    used_ifsc = set()

    for _ in range(records):

        city = random.choice(cities)

        city_name = city["city"]

        state = city["state"]

        zone = city["zone"]

        branch_name = random.choice(
            BRANCHES["branches"][city_name]
        )

        while True:

            code = random.randint(1000,9999)

            ifsc = f"{ifsc_prefix}{code}"

            if ifsc not in used_ifsc:

                used_ifsc.add(ifsc)

                break

        bid = branch_id()

        context.branch_ids.append(bid)

        rows.append({

            "branch_id": bid,

            "branch_name": f"{branch_name} Branch",

            "branch_code": code,

            "ifsc_code": ifsc,

            "bank_name": bank["name"],

            "city": city_name,

            "state": state,

            "zone": zone,

            "country":"India",

            "status":"ACTIVE"

        })

    df = pd.DataFrame(rows)

    context.branch_df = df

    return df