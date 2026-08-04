"""
Generation Context

Shared runtime context across the banking simulator.

All generators read from and write to this object.
"""

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class GenerationContext:

    # ==========================================================
    # Master Data
    # ==========================================================

    branch_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    customer_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    account_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    card_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    loan_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    customer_kyc_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    exchange_rate_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    # ==========================================================
    # Runtime Lookups
    # ==========================================================

    branch_lookup: dict = field(default_factory=dict)

    customer_lookup: dict = field(default_factory=dict)

    account_lookup: dict = field(default_factory=dict)

    card_lookup: dict = field(default_factory=dict)

    loan_lookup: dict = field(default_factory=dict)

    # ==========================================================
    # Runtime Metadata
    # ==========================================================

    metadata: dict = field(default_factory=dict)

    # ==========================================================
    # Helper Methods
    # ==========================================================

    def reset(self):

        """
        Clears all runtime objects.
        """

        self.branch_df = pd.DataFrame()

        self.customer_df = pd.DataFrame()

        self.account_df = pd.DataFrame()

        self.card_df = pd.DataFrame()

        self.loan_df = pd.DataFrame()

        self.customer_kyc_df = pd.DataFrame()

        self.exchange_rate_df = pd.DataFrame()

        self.branch_lookup.clear()

        self.customer_lookup.clear()

        self.account_lookup.clear()

        self.card_lookup.clear()

        self.loan_lookup.clear()

        self.metadata.clear()