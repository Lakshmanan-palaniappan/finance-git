"""
Transaction Rules Loader
"""

from pathlib import Path

import yaml

REFERENCE_DIR = (
    Path(__file__).resolve().parents[2]
    / "config"
    / "reference"
)

with open(
    REFERENCE_DIR / "transaction_rules.yml",
    "r",
    encoding="utf-8"
) as file:

    TRANSACTION_RULES = yaml.safe_load(file)