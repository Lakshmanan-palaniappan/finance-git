from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/occupations.yml") as f:
    OCCUPATIONS = yaml.safe_load(f)