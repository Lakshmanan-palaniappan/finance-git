from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/account_rules.yml") as f:
    ACCOUNT_RULES = yaml.safe_load(f)