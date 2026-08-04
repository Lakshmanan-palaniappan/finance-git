"""
Account CDC Generator
"""

from generators.common.context import GenerationContext
from generators.cdc.base_cdc_generator import BaseCDCGenerator


class AccountCDCGenerator(BaseCDCGenerator):

    def __init__(self, context: GenerationContext):

        super().__init__(
            context=context,
            dataframe_name="account_cdc_df"
        )

    ###############################################################

    def record_update(
        self,
        account_id,
        customer_id,
        branch_id,
        old_balance,
        new_balance,
        transaction_id
    ):

        self.append({

            "entity": "ACCOUNT",

            "operation": "UPDATE",

            "account_id": account_id,

            "customer_id": customer_id,

            "branch_id": branch_id,

            "old_balance": round(
                float(old_balance),
                2
            ),

            "new_balance": round(
                float(new_balance),
                2
            ),

            "balance_difference": round(
                float(new_balance)
                - float(old_balance),
                2
            ),

            "transaction_id": transaction_id

        })