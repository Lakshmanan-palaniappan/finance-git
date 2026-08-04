"""
Loan CDC Generator
"""

from generators.common.context import GenerationContext
from generators.cdc.base_cdc_generator import BaseCDCGenerator


class LoanCDCGenerator(BaseCDCGenerator):

    def __init__(self, context: GenerationContext):

        super().__init__(
            context=context,
            dataframe_name="loan_cdc_df"
        )

    ###############################################################

    def emi_paid(
        self,
        loan,
        old_balance,
        new_balance
    ):

        self.append({

            "entity": "LOAN",

            "operation": "UPDATE",

            "loan_id": loan.loan_id,

            "customer_id": loan.customer_id,

            "old_balance": old_balance,

            "new_balance": new_balance,

            "old_status": loan.status,

            "new_status": loan.status

        })

    ###############################################################

    def status_changed(
        self,
        loan,
        old_status,
        new_status
    ):

        self.append({

            "entity": "LOAN",

            "operation": "UPDATE",

            "loan_id": loan.loan_id,

            "customer_id": loan.customer_id,

            "old_balance": loan.outstanding_balance,

            "new_balance": loan.outstanding_balance,

            "old_status": old_status,

            "new_status": new_status

        })