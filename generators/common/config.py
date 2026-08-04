"""
Central Configuration Loader

Loads:

- .env
- config/environment.yml
- config/metadata.yml

No other module should directly read YAML or environment variables.
"""

from pathlib import Path
import os

import yaml
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

CONFIG_DIR = ROOT_DIR / "config"

# ---------------------------------------------------------------------
# Environment Variables
# ---------------------------------------------------------------------

load_dotenv(ROOT_DIR / ".env")

# ---------------------------------------------------------------------
# YAML
# ---------------------------------------------------------------------

with open(CONFIG_DIR / "environment.yml", "r") as file:

    ENVIRONMENT = yaml.safe_load(file)

with open(CONFIG_DIR / "metadata.yml", "r") as file:

    METADATA = yaml.safe_load(file)

# ---------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------

PROJECT = ENVIRONMENT.get("project", {})

# ---------------------------------------------------------------------
# Azure
# ---------------------------------------------------------------------

AZURE = ENVIRONMENT.get("azure", {})

AZURE_STORAGE_ACCOUNT = AZURE.get("storage_account")

AZURE_CONTAINER = AZURE.get("container")

if not AZURE_STORAGE_ACCOUNT:
    raise ValueError("storage_account missing in environment.yml")

if not AZURE_CONTAINER:
    raise ValueError("container missing in environment.yml")

# ---------------------------------------------------------------------
# Authentication (.env)
# ---------------------------------------------------------------------

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

# ---------------------------------------------------------------------
# Unity Catalog
# ---------------------------------------------------------------------

UNITY_CATALOG = ENVIRONMENT.get(
    "unity_catalog",
    {}
)

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

PATHS = ENVIRONMENT.get(
    "paths",
    {}
)

# ---------------------------------------------------------------------
# Datasets
# ---------------------------------------------------------------------

DATASETS = ENVIRONMENT.get(
    "datasets",
    {}
)

# ---------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------

SIMULATION = ENVIRONMENT.get(
    "simulation",
    {}
)

# ---------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------

SCHEMAS = METADATA.get(
    "schemas",
    {}
)

# ---------------------------------------------------------------------
# Local Directories
# ---------------------------------------------------------------------

OUTPUT_DIRECTORY = Path(

    os.getenv(
        "OUTPUT_DIRECTORY",
        ROOT_DIR / "output"
    )

)

TEMP_DIRECTORY = Path(

    os.getenv(
        "TEMP_DIRECTORY",
        ROOT_DIR / "temp"
    )

)

ARCHIVE_DIRECTORY = Path(

    os.getenv(
        "ARCHIVE_DIRECTORY",
        ROOT_DIR / "archive"
    )

)

# ---------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

ENV = os.getenv(
    "ENV",
    "local"
)