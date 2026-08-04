from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/loan_rules.yml") as f:
    LOAN_RULES = yaml.safe_load(f)