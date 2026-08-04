"""
Enterprise Banking Simulator
"""

import time
import schedule

from generators.common.context import GenerationContext
from generators.common.publish import Publisher
from generators.common.logger import logger
from generators.common.config import SIMULATION

from generators.master.branch_generator import BranchGenerator
from generators.master.customer_generator import CustomerGenerator
from generators.master.account_generator import AccountGenerator
from generators.master.card_generator import CardGenerator
from generators.master.loan_generator import LoanGenerator
from generators.master.kyc_generator import KYCGenerator
from generators.master.exchange_rate_generator import ExchangeRateGenerator

from generators.streaming.transaction_generator import TransactionGenerator
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

        if dataframe.empty:

            logger.warning(
                f"{dataset_name} generated no records."
            )

            return

        logger.info(
            f"Publishing {dataset_name}"
        )

        self.publisher.publish(
            dataframe,
            dataset_name
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

            try:

                dataframe = generator.generate()

                self.publish_dataset(
                    dataset_name,
                    dataframe
                )

            except Exception:

                logger.exception(
                    f"Failed generating {dataset_name}"
                )

        logger.info(
            "Master Data Generation Completed."
        )

    ###############################################################

    def transaction_job(self):

        try:

            logger.info(
                "Generating Transactions..."
            )

            dataframe = TransactionGenerator(
                self.context
            ).generate()

            self.publish_dataset(
                "transactions",
                dataframe
            )

        except Exception:

            logger.exception(
                "Transaction generation failed."
            )

    ###############################################################

    def atm_job(self):

        try:

            logger.info(
                "Generating ATM Transactions..."
            )

            dataframe = ATMGenerator(
                self.context
            ).generate()

            self.publish_dataset(
                "atm_transactions",
                dataframe
            )

        except Exception:

            logger.exception(
                "ATM transaction generation failed."
            )

    ###############################################################

    def login_job(self):

        try:

            logger.info(
                "Generating Login Activity..."
            )

            dataframe = LoginGenerator(
                self.context
            ).generate()

            self.publish_dataset(
                "login_activity",
                dataframe
            )

        except Exception:

            logger.exception(
                "Login activity generation failed."
            )

    ###############################################################

    def start(self):

        self.load_master_data()

        stream = SIMULATION["streaming"]

        schedule.every(
            stream["transaction_interval"]
        ).seconds.do(
            self.transaction_job
        )

        schedule.every(
            stream["atm_interval"]
        ).seconds.do(
            self.atm_job
        )

        schedule.every(
            stream["login_interval"]
        ).seconds.do(
            self.login_job
        )

        logger.info(
            "Enterprise Banking Simulator Started."
        )

        try:

            while True:

                schedule.run_pending()

                time.sleep(1)

        except KeyboardInterrupt:

            logger.info(
                "Simulator stopped by user."
            )