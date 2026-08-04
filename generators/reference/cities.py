"""
City Reference Loader
"""

from pathlib import Path

import yaml

REFERENCE_DIR = (
    Path(__file__).resolve().parents[2]
    / "config"
    / "reference"
)

with open(
    REFERENCE_DIR / "cities.yml",
    "r",
    encoding="utf-8"
) as file:

    CITIES = yaml.safe_load(file)