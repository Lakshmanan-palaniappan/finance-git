"""
Generation Context

Shared state across all generators.
"""

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class GenerationContext:

    ###############################################################
    # Master Data
    ###############################################################

    branch_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    customer_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    account_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    card_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    loan_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    customer_kyc_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    exchange_rate_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    ###############################################################
    # Streaming
    ###############################################################

    transaction_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    atm_transaction_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    login_activity_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    ###############################################################
    # CDC
    ###############################################################

    account_cdc_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    customer_cdc_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    card_cdc_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    loan_cdc_df: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )

    ###############################################################
    # Batch Metadata
    ###############################################################

    current_batch_id: str = ""

    ###############################################################
    # Streaming Cleanup
    ###############################################################

    def clear_streaming(self):

        self.transaction_df = pd.DataFrame()

        self.atm_transaction_df = pd.DataFrame()

        self.login_activity_df = pd.DataFrame()

    ###############################################################
    # CDC Cleanup
    ###############################################################

    def clear_cdc(self):

        self.account_cdc_df = pd.DataFrame()

        self.customer_cdc_df = pd.DataFrame()

        self.card_cdc_df = pd.DataFrame()

        self.loan_cdc_df = pd.DataFrame()