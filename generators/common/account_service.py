"""
Account Service

Maintains account balances and emits Account CDC.
"""

from generators.common.context import GenerationContext
from generators.cdc.account_cdc_generator import AccountCDCGenerator


class AccountService:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.cdc = AccountCDCGenerator(context)

    ###############################################################

    def update_balance(
        self,
        account_index: int,
        amount: float,
        transaction_id: str,
        operation: str
    ):

        dataframe = self.context.account_df

        account = dataframe.loc[account_index]

        old_balance = float(
            dataframe.at[
                account_index,
                "balance"
            ]
        )

        if operation in [

            "Withdrawal",

            "ATM",

            "Transfer",

            "UPI"

        ]:

            if old_balance < amount:

                return False

            new_balance = old_balance - amount

        else:

            new_balance = old_balance + amount

        dataframe.at[
            account_index,
            "balance"
        ] = round(
            new_balance,
            2
        )

        self.cdc.record_update(

            account_id=account.account_id,

            customer_id=account.customer_id,

            branch_id=account.branch_id,

            old_balance=old_balance,

            new_balance=new_balance,

            transaction_id=transaction_id

        )

        return True