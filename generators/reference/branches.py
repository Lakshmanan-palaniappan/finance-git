from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/branches.yml") as f:
    BRANCHES = yaml.safe_load(f)