"""
Central Configuration Loader

This module is the ONLY place that reads:

- .env
- config/environment.yml
- config/metadata.yml

Every other module imports values from here.
"""

from pathlib import Path
import os

import yaml
from dotenv import load_dotenv

# ==============================================================================
# Root Directories
# ==============================================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

CONFIG_DIR = ROOT_DIR / "config"

load_dotenv(ROOT_DIR / ".env")

# ==============================================================================
# YAML Configuration
# ==============================================================================

with open(CONFIG_DIR / "environment.yml", encoding="utf-8") as f:
    ENVIRONMENT = yaml.safe_load(f)

with open(CONFIG_DIR / "metadata.yml", encoding="utf-8") as f:
    METADATA = yaml.safe_load(f)

# ==============================================================================
# Project
# ==============================================================================

PROJECT = ENVIRONMENT.get("project", {})
PROJECT_NAME = PROJECT.get("name", "finance-project")

ENVIRONMENT_INFO = ENVIRONMENT.get("environment", {})
ENVIRONMENT_NAME = ENVIRONMENT_INFO.get("name", "dev")

# ==============================================================================
# Storage
# ==============================================================================

STORAGE = ENVIRONMENT.get("storage", {})

STORAGE_BACKEND = STORAGE.get("backend", "local").lower()

SAVE_LOCAL_COPY = STORAGE.get("save_local_copy", True)

LOCAL_OUTPUT_ROOT = ROOT_DIR / STORAGE.get("local_output_root", "output")

LOCAL_ARCHIVE_ROOT = ROOT_DIR / STORAGE.get("archive_root", "archive")

LOCAL_TEMP_ROOT = ROOT_DIR / STORAGE.get("temp_root", "temp")

FILE_FORMAT = STORAGE.get("file_format", "csv")

# ==============================================================================
# Azure
# ==============================================================================

AZURE = ENVIRONMENT.get("azure", {})

AZURE_STORAGE_ACCOUNT = AZURE.get("storage_account")

AZURE_CONTAINER = AZURE.get("container")

AZURE_FILESYSTEM = AZURE.get("filesystem")

AZURE_ROOT_FOLDER = AZURE.get("root_folder", "landing")

AZURE_AUTHENTICATION = AZURE.get("authentication", "default")

# ==============================================================================
# Azure Credentials (.env)
# ==============================================================================

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")

# ==============================================================================
# Unity Catalog
# ==============================================================================

UNITY_CATALOG = ENVIRONMENT.get("unity_catalog", {})

UC_ENABLED = UNITY_CATALOG.get("enabled", False)

UC_CATALOG = UNITY_CATALOG.get("catalog")

UC_BRONZE_SCHEMA = UNITY_CATALOG.get("bronze_schema")

UC_SILVER_SCHEMA = UNITY_CATALOG.get("silver_schema")

UC_GOLD_SCHEMA = UNITY_CATALOG.get("gold_schema")

UC_MONITORING_SCHEMA = UNITY_CATALOG.get("monitoring_schema")

UC_VOLUME = UNITY_CATALOG.get("volume")

# ==============================================================================
# Landing Paths
# ==============================================================================

PATHS = ENVIRONMENT.get("paths", {})

LANDING_PATH = PATHS.get("landing", "landing")

MASTER_PATH = PATHS.get("master", "master")

CDC_PATH = PATHS.get("cdc", "cdc")

STREAMING_PATH = PATHS.get("streaming", "streaming")

BRONZE_PATH = PATHS.get("bronze", "bronze")

SILVER_PATH = PATHS.get("silver", "silver")

GOLD_PATH = PATHS.get("gold", "gold")

CHECKPOINT_PATH = PATHS.get("checkpoints", "checkpoints")

SCHEMA_PATH = PATHS.get("schema", "schema")

QUARANTINE_PATH = PATHS.get("quarantine", "quarantine")

LOG_PATH = PATHS.get("logs", "logs")

ARCHIVE_PATH = PATHS.get("archive", "archive")

# ==============================================================================
# Dataset Definitions
# ==============================================================================

DATASETS = ENVIRONMENT.get("datasets", {})

# ==============================================================================
# Simulation
# ==============================================================================

SIMULATION = ENVIRONMENT.get("simulation", {})

# ==============================================================================
# Jobs
# ==============================================================================

JOB = ENVIRONMENT.get("job", {})

JOB_ENABLED = JOB.get("enabled", True)

JOB_DEFAULT_MODE = JOB.get("default_mode", "full")

JOB_DEFAULT_RECORDS = JOB.get("default_records", 1000)

JOB_DEFAULT_OUTPUT = JOB.get("default_output", STORAGE_BACKEND)

# ==============================================================================
# Monitoring
# ==============================================================================

MONITORING = ENVIRONMENT.get("monitoring", {})

# ==============================================================================
# Settings
# ==============================================================================

SETTINGS = ENVIRONMENT.get("settings", {})

OVERWRITE_EXISTING = SETTINGS.get("overwrite_existing_files", False)

UPLOAD_TO_ADLS = SETTINGS.get("upload_to_adls", True)

TIMEZONE = SETTINGS.get("timezone", "Asia/Kolkata")

LOG_LEVEL = SETTINGS.get(
    "log_level",
    os.getenv("LOG_LEVEL", "INFO")
)

# ==============================================================================
# Metadata
# ==============================================================================

SCHEMAS = METADATA.get("schemas", {})

# ==============================================================================
# Local Directories
# ==============================================================================

OUTPUT_DIRECTORY = LOCAL_OUTPUT_ROOT

TEMP_DIRECTORY = LOCAL_TEMP_ROOT

ARCHIVE_DIRECTORY = LOCAL_ARCHIVE_ROOT

OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

TEMP_DIRECTORY.mkdir(parents=True, exist_ok=True)

ARCHIVE_DIRECTORY.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# Runtime Environment
# ==============================================================================

ENV = os.getenv("ENV", "local")

# ==============================================================================
# Helper Functions
# ==============================================================================

def dataset_config(dataset_name: str) -> dict:
    """Return dataset configuration from environment.yml."""
    return DATASETS.get(dataset_name, {})


def dataset_folder(dataset_name: str) -> str:
    """Return configured landing folder."""
    return dataset_config(dataset_name).get("folder", dataset_name)


def dataset_type(dataset_name: str) -> str:
    """master / cdc / streaming"""
    return dataset_config(dataset_name).get("type", "master")


def dataset_format(dataset_name: str) -> str:
    return dataset_config(dataset_name).get("format", FILE_FORMAT)


def dataset_prefix(dataset_name: str) -> str:
    return dataset_config(dataset_name).get(
        "filename_prefix",
        dataset_name,
    )