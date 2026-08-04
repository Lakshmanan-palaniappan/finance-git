"""
Loan Service
"""

from generators.common.context import GenerationContext
from generators.cdc.loan_cdc_generator import LoanCDCGenerator


class LoanService:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.cdc = LoanCDCGenerator(context)

    ###############################################################

    def pay_emi(
        self,
        loan_index: int,
        amount: float
    ):

        dataframe = self.context.loan_df

        loan = dataframe.loc[loan_index]

        old_balance = float(
            dataframe.at[
                loan_index,
                "outstanding_balance"
            ]
        )

        new_balance = max(
            0,
            old_balance - amount
        )

        dataframe.at[
            loan_index,
            "outstanding_balance"
        ] = new_balance

        self.cdc.emi_paid(

            loan,

            old_balance,

            new_balance

        )

        if new_balance == 0:

            old_status = dataframe.at[
                loan_index,
                "status"
            ]

            dataframe.at[
                loan_index,
                "status"
            ] = "CLOSED"

            self.cdc.status_changed(

                loan,

                old_status,

                "CLOSED"

            )