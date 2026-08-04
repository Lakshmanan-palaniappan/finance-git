from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

with open(ROOT / "config/reference/cities.yml") as f:
    CITIES = yaml.safe_load(f)