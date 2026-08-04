"""
Customer CDC Generator
"""

from generators.common.context import GenerationContext
from generators.cdc.base_cdc_generator import BaseCDCGenerator


class CustomerCDCGenerator(BaseCDCGenerator):

    def __init__(self, context: GenerationContext):

        super().__init__(
            context=context,
            dataframe_name="customer_cdc_df"
        )

    ###############################################################

    def record_update(
        self,
        customer_id,
        attribute,
        old_value,
        new_value
    ):

        self.append({

            "entity": "CUSTOMER",

            "operation": "UPDATE",

            "customer_id": customer_id,

            "attribute": attribute,

            "old_value": old_value,

            "new_value": new_value

        })