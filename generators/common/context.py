"""
Shared context across generators.
"""

from dataclasses import dataclass, field
import pandas as pd


@dataclass
class GenerationContext:

    branch_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    customer_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    account_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    card_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    loan_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    customer_kyc_df: pd.DataFrame = field(default_factory=pd.DataFrame)

    exchange_rate_df: pd.DataFrame = field(default_factory=pd.DataFrame)