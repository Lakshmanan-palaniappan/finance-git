"""
Enterprise Banking Simulator
"""

import schedule
import time

from generators.common.context import GenerationContext
from generators.common.logger import logger

from generators.master.branch_generator import generate as generate_branches
from generators.master.customer_generator import generate as generate_customers
from generators.master.account_generator import generate as generate_accounts
from generators.master.card_generator import generate as generate_cards
from generators.master.loan_generator import generate as generate_loans
from generators.master.kyc_generator import generate as generate_kyc
from generators.master.exchange_rate_generator import generate as generate_exchange_rates

from generators.streaming.transaction_generator import TransactionGenerator
from generators.streaming.atm_generator import ATMGenerator
from generators.streaming.login_generator import LoginGenerator

from generators.common.publish import Publisher


class BankingSimulator:

    def __init__(self):

        self.context = GenerationContext()

    ####################################################

    def load_master_data(self):

        logger.info("Generating Branches")

        Publisher.publish(
            generate_branches(self.context),
            "branches"
        )

        logger.info("Generating Customers")

        Publisher.publish(
            generate_customers(self.context),
            "customers"
        )

        logger.info("Generating Accounts")

        Publisher.publish(
            generate_accounts(self.context),
            "accounts"
        )

        logger.info("Generating Cards")

        Publisher.publish(
            generate_cards(self.context),
            "cards"
        )

        logger.info("Generating Loans")

        Publisher.publish(
            generate_loans(self.context),
            "loans"
        )

        logger.info("Generating KYC")

        Publisher.publish(
            generate_kyc(self.context),
            "kyc"
        )

        logger.info("Generating Exchange Rates")

        Publisher.publish(
            generate_exchange_rates(),
            "exchange_rates"
        )

    ####################################################

    def transaction_job(self):

        TransactionGenerator(self.context).run()

    ####################################################

    def atm_job(self):

        ATMGenerator(self.context).run()

    ####################################################

    def login_job(self):

        LoginGenerator(self.context).run()

    ####################################################

    def start(self):

        logger.info("Loading Master Data")

        self.load_master_data()

        schedule.every(5).minutes.do(
            self.transaction_job
        )

        schedule.every(5).minutes.do(
            self.atm_job
        )

        schedule.every(1).minutes.do(
            self.login_job
        )

        logger.info("Simulator Started")

        while True:

            schedule.run_pending()

            time.sleep(1)