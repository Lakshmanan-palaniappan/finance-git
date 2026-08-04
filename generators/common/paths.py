"""
Project Paths

All filesystem paths used by the simulator.
"""

from pathlib import Path

from generators.common.config import (
    ROOT_DIR,
    OUTPUT_DIRECTORY,
    TEMP_DIRECTORY,
    ARCHIVE_DIRECTORY,
)

# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

PROJECT_ROOT = ROOT_DIR

# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

CONFIG_PATH = PROJECT_ROOT / "config"

REFERENCE_PATH = CONFIG_PATH / "reference"

# ---------------------------------------------------------
# Local Output
# ---------------------------------------------------------

OUTPUT_PATH = Path(OUTPUT_DIRECTORY)

TEMP_PATH = Path(TEMP_DIRECTORY)

ARCHIVE_PATH = Path(ARCHIVE_DIRECTORY)

LOG_PATH = PROJECT_ROOT / "logs"

# ---------------------------------------------------------
# Create Directories
# ---------------------------------------------------------

for directory in [

    OUTPUT_PATH,

    TEMP_PATH,

    ARCHIVE_PATH,

    LOG_PATH,

]:

    directory.mkdir(

        parents=True,

        exist_ok=True

    )