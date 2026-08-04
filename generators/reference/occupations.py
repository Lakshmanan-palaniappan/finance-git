"""
Occupation Reference Loader
"""

from pathlib import Path

import yaml

REFERENCE_DIR = (
    Path(__file__).resolve().parents[2]
    / "config"
    / "reference"
)

with open(
    REFERENCE_DIR / "occupations.yml",
    "r",
    encoding="utf-8"
) as file:

    OCCUPATIONS = yaml.safe_load(file)