"""
Card CDC Generator
"""

from generators.common.context import GenerationContext
from generators.cdc.base_cdc_generator import BaseCDCGenerator


class CardCDCGenerator(BaseCDCGenerator):

    def __init__(self, context: GenerationContext):

        super().__init__(
            context=context,
            dataframe_name="card_cdc_df"
        )

    ###############################################################

    def status_changed(
        self,
        card,
        old_status,
        new_status
    ):

        self.append({

            "entity": "CARD",

            "operation": "UPDATE",

            "card_id": card.card_id,

            "customer_id": card.customer_id,

            "account_id": card.account_id,

            "old_status": old_status,

            "new_status": new_status,

            "card_type": card.card_type,

            "network": card.network

        })