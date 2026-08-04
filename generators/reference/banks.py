from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/banks.yml") as f:
    BANKS = yaml.safe_load(f)