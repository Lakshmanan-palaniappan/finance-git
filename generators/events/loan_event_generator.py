"""
Loan Event Generator
"""

import random

from generators.common.config import SIMULATION
from generators.common.context import GenerationContext
from generators.common.loan_service import LoanService


class LoanEventGenerator:

    def __init__(self, context: GenerationContext):

        self.context = context

        self.service = LoanService(context)

    ###############################################################

    def generate(self):

        dataframe = self.context.loan_df

        if dataframe.empty:

            return

        updates = min(

            SIMULATION["streaming"]["loan_events"],

            len(dataframe)

        )

        for _ in range(updates):

            idx = random.choice(

                dataframe.index.tolist()

            )

            loan = dataframe.loc[idx]

            if loan.status == "CLOSED":

                continue

            event = random.choices(

                [

                    "EMI",

                    "DEFAULT",

                    "CLOSE"

                ],

                weights=[

                    80,

                    10,

                    10

                ]

            )[0]

            if event == "EMI":

                payment = random.randint(

                    1000,

                    10000

                )

                self.service.pay_emi(

                    idx,

                    payment

                )

            elif event == "DEFAULT":

                self.service.mark_default(

                    idx

                )

            else:

                self.service.close_loan(

                    idx

                )