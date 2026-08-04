"""
Enterprise Configuration Loader
"""

from pathlib import Path
import os

import yaml
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]

CONFIG_DIR = ROOT_DIR / "config"

load_dotenv(ROOT_DIR / ".env")


def load_yaml(file_name: str):

    with open(CONFIG_DIR / file_name, "r") as file:

        return yaml.safe_load(file)


ENVIRONMENT = load_yaml("environment.yml")
METADATA = load_yaml("metadata.yml")


PROJECT = ENVIRONMENT["project"]

AZURE = ENVIRONMENT["azure"]

UNITY_CATALOG = ENVIRONMENT["unity_catalog"]

PATHS = ENVIRONMENT["paths"]

DATASETS = ENVIRONMENT["datasets"]

SIMULATION = ENVIRONMENT["simulation"]

MONITORING = ENVIRONMENT["monitoring"]


# ---------------------------------------------------------------------
# Azure
# ---------------------------------------------------------------------

AZURE_STORAGE_ACCOUNT = AZURE["storage_account"]

AZURE_CONTAINER = AZURE["container"]

AUTH_MODE = AZURE.get(
    "auth_mode",
    "browser"
)
ENV = os.getenv("ENV", "local")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

TEMP_DIRECTORY = os.getenv("TEMP_DIRECTORY", "temp")

ARCHIVE_DIRECTORY = os.getenv("ARCHIVE_DIRECTORY", "archive")

OUTPUT_DIRECTORY = os.getenv("OUTPUT_DIRECTORY", "output")