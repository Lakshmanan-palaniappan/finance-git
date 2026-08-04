from pathlib import Path

from generators.common.config import OUTPUT_DIRECTORY

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_PATH = PROJECT_ROOT / OUTPUT_DIRECTORY

CONFIG_PATH = PROJECT_ROOT / "config"

TEMP_PATH = PROJECT_ROOT / "temp"

ARCHIVE_PATH = PROJECT_ROOT / "archive"

LOG_PATH = PROJECT_ROOT / "logs"