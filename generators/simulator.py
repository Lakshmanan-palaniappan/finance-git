"""
Enterprise Banking Simulator
"""

import time
from uuid import uuid4

import schedule

from generators.common.context import GenerationContext
from generators.common.publish import Publisher
from generators.common.logger import logger
from generators.common.config import SIMULATION

# Master
from generators.master.branch_generator import BranchGenerator
from generators.master.customer_generator import CustomerGenerator
from generators.master.account_generator import AccountGenerator
from generators.master.card_generator import CardGenerator
from generators.master.loan_generator import LoanGenerator
from generators.master.kyc_generator import KYCGenerator
from generators.master.exchange_rate_generator import (
    ExchangeRateGenerator
)

# Events
from generators.events.customer_event_generator import (
    CustomerEventGenerator
)
from generators.events.card_event_generator import (
    CardEventGenerator
)
from generators.events.loan_event_generator import (
    LoanEventGenerator
)

# Streaming
from generators.streaming.transaction_generator import (
    TransactionGenerator
)
from generators.streaming.atm_generator import ATMGenerator
from generators.streaming.login_generator import LoginGenerator


class BankingSimulator:

    def __init__(self):

        self.context = GenerationContext()

        self.publisher = Publisher()

    ###############################################################

    def publish_dataset(
        self,
        dataset_name,
        dataframe
    ):

        self.publisher.publish(
            dataframe=dataframe,
            dataset_name=dataset_name
        )

    ###############################################################

    def load_master_data(self):

        logger.info(
            "Generating Master Data..."
        )

        datasets = [

            (
                "branches",
                BranchGenerator(self.context)
            ),

            (
                "customers",
                CustomerGenerator(self.context)
            ),

            (
                "accounts",
                AccountGenerator(self.context)
            ),

            (
                "cards",
                CardGenerator(self.context)
            ),

            (
                "loans",
                LoanGenerator(self.context)
            ),

            (
                "customer_kyc",
                KYCGenerator(self.context)
            ),

            (
                "exchange_rates",
                ExchangeRateGenerator(self.context)
            )

        ]

        for dataset_name, generator in datasets:

            dataframe = generator.generate()

            self.publish_dataset(

                dataset_name,

                dataframe

            )

        logger.info(
            "Master Data Generation Completed."
        )

    ###############################################################

    def generate_events(self):

        CustomerEventGenerator(
            self.context
        ).generate()

        CardEventGenerator(
            self.context
        ).generate()

        LoanEventGenerator(
            self.context
        ).generate()

    ###############################################################

    def generate_streaming(self):

        transaction_df = TransactionGenerator(

            self.context

        ).generate()

        atm_df = ATMGenerator(

            self.context

        ).generate()

        login_df = LoginGenerator(

            self.context

        ).generate()

        return (

            transaction_df,

            atm_df,

            login_df

        )

    ###############################################################

    def publish_streaming(self):

        self.publish_dataset(

            "transactions",

            self.context.transaction_df

        )

        self.publish_dataset(

            "atm_transactions",

            self.context.atm_transaction_df

        )

        self.publish_dataset(

            "login_activity",

            self.context.login_activity_df

        )

    ###############################################################

    def publish_cdc(self):

        self.publish_dataset(

            "account_cdc",

            self.context.account_cdc_df

        )

        self.publish_dataset(

            "customer_cdc",

            self.context.customer_cdc_df

        )

        self.publish_dataset(

            "card_cdc",

            self.context.card_cdc_df

        )

        self.publish_dataset(

            "loan_cdc",

            self.context.loan_cdc_df

        )

    ###############################################################

    def business_cycle(self):

        logger.info(

            "=" * 70

        )

        logger.info(

            "Starting Business Cycle"

        )

        ###########################################################
        # New Batch
        ###########################################################

        self.context.current_batch_id = str(

            uuid4()

        )

        ###########################################################
        # Business Events
        ###########################################################

        self.generate_events()

        ###########################################################
        # Streaming
        ###########################################################

        transaction_df, atm_df, login_df = (

            self.generate_streaming()

        )

        ###########################################################
        # Publish
        ###########################################################

        self.publish_streaming()

        self.publish_cdc()

        ###########################################################
        # Summary
        ###########################################################

        logger.info(

            f"""

Business Cycle Completed

Batch ID : {self.context.current_batch_id}

Transactions : {len(transaction_df)}

ATM Transactions : {len(atm_df)}

Login Activity : {len(login_df)}

Account CDC : {len(self.context.account_cdc_df)}

Customer CDC : {len(self.context.customer_cdc_df)}

Card CDC : {len(self.context.card_cdc_df)}

Loan CDC : {len(self.context.loan_cdc_df)}

"""

        )

        ###########################################################
        # Cleanup
        ###########################################################

        self.context.clear_streaming()

        self.context.clear_cdc()

    ###############################################################

    def start(self):

        self.load_master_data()

        interval = SIMULATION["streaming"][

            "cycle_interval"

        ]

        schedule.every(

            interval

        ).seconds.do(

            self.business_cycle

        )

        logger.info(

            f"Business Cycle every {interval} seconds."

        )

        self.business_cycle()

        while True:

            schedule.run_pending()

            time.sleep(1)