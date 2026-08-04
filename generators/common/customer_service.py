"""
Customer Service

Responsible for updating customer master data and emitting CDC.
"""

from generators.common.context import GenerationContext
from generators.cdc.customer_cdc_generator import CustomerCDCGenerator


class CustomerService:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.cdc = CustomerCDCGenerator(context)

    ###############################################################

    def update_attribute(
        self,
        customer_index: int,
        attribute: str,
        new_value
    ):

        dataframe = self.context.customer_df

        customer = dataframe.loc[customer_index]

        old_value = dataframe.at[
            customer_index,
            attribute
        ]

        if old_value == new_value:

            return

        dataframe.at[
            customer_index,
            attribute
        ] = new_value

        self.cdc.record_update(

            customer_id=customer.customer_id,

            attribute=attribute,

            old_value=old_value,

            new_value=new_value

        )