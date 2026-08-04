"""
Card Event Generator
"""

import random

from generators.common.config import SIMULATION
from generators.common.context import GenerationContext
from generators.common.card_service import CardService


VALID_TRANSITIONS = {

    "ACTIVE": [

        "BLOCKED",

        "EXPIRED"

    ],

    "BLOCKED": [

        "ACTIVE"

    ],

    "EXPIRED": []

}


class CardEventGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.service = CardService(context)

    ###############################################################

    def generate(self):

        dataframe = self.context.card_df

        if dataframe.empty:

            return

        updates = min(

            SIMULATION["streaming"]["card_events"],

            len(dataframe)

        )

        for _ in range(updates):

            idx = random.choice(dataframe.index.tolist())

            status = dataframe.at[idx, "status"]

            allowed = VALID_TRANSITIONS.get(

                status,

                []

            )

            if not allowed:

                continue

            new_status = random.choice(allowed)

            self.service.update_status(

                idx,

                new_status

            )