from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/card_rules.yml") as f:
    CARD_RULES = yaml.safe_load(f)