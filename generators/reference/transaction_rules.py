from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/transaction_rules.yml") as f:
    TRANSACTION_RULES = yaml.safe_load(f)