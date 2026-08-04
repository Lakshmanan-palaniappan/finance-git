"""
Exchange Rate Reference Loader
"""

from pathlib import Path

import yaml

REFERENCE_DIR = (
    Path(__file__).resolve().parents[2]
    / "config"
    / "reference"
)

with open(
    REFERENCE_DIR / "exchange_rates.yml",
    "r",
    encoding="utf-8"
) as file:

    EXCHANGE_RATES = yaml.safe_load(file)