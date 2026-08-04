"""
Card Service
"""

from generators.common.context import GenerationContext
from generators.cdc.card_cdc_generator import CardCDCGenerator


class CardService:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.cdc = CardCDCGenerator(context)

    ###############################################################

    def update_status(
        self,
        card_index: int,
        new_status: str
    ):

        dataframe = self.context.card_df

        card = dataframe.loc[card_index]

        old_status = dataframe.at[
            card_index,
            "status"
        ]

        if old_status == new_status:

            return

        dataframe.at[
            card_index,
            "status"
        ] = new_status

        self.cdc.status_changed(

            card,

            old_status,

            new_status

        )