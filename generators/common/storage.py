"""
Storage Layer

Supports:
    - Azure Data Lake Storage (ADLS)
    - Local file system
    - Future Unity Catalog Volumes

The rest of the project should interact with this class only.
"""

from pathlib import Path
from typing import Union

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

from generators.common.config import (
    AZURE_STORAGE_ACCOUNT,
    AZURE_CONTAINER,
    AZURE_ROOT_FOLDER,
    STORAGE_BACKEND,
)
from generators.common.logger import logger


class ADLSStorage:

    ###########################################################################

    def __init__(self):

        credential = DefaultAzureCredential()

        account_url = (
            f"https://{AZURE_STORAGE_ACCOUNT}.dfs.core.windows.net"
        )

        self.service = DataLakeServiceClient(
            account_url=account_url,
            credential=credential,
        )

        self.filesystem = self.service.get_file_system_client(
            AZURE_CONTAINER
        )

        logger.info(
            "Connected to Azure Data Lake Storage."
        )

    ###########################################################################

    def ensure_directory(
        self,
        directory: str,
    ) -> None:
        """
        Creates a directory if it doesn't already exist.
        """

        try:
            self.filesystem.create_directory(directory)
        except Exception:
            pass

    ###########################################################################

    def upload(
        self,
        local_file: Union[str, Path],
        remote_path: str,
        overwrite: bool = True,
    ) -> str:
        """
        Upload a local file to ADLS.
        """

        local_file = Path(local_file)

        if not local_file.exists():
            raise FileNotFoundError(local_file)

        directory = str(Path(remote_path).parent)

        self.ensure_directory(directory)

        file_client = self.filesystem.get_file_client(remote_path)

        with open(local_file, "rb") as file:

            file_client.upload_data(
                file,
                overwrite=overwrite,
            )

        logger.info(
            f"Uploaded {local_file.name} -> {remote_path}"
        )

        return remote_path

    ###########################################################################

    def exists(
        self,
        remote_path: str,
    ) -> bool:
        """
        Check if a file already exists.
        """

        try:

            self.filesystem.get_file_client(
                remote_path
            ).get_file_properties()

            return True

        except Exception:

            return False

    ###########################################################################

    def delete(
        self,
        remote_path: str,
    ) -> None:
        """
        Delete a remote file.
        """

        self.filesystem.delete_file(remote_path)

        logger.info(
            f"Deleted {remote_path}"
        )

    ###########################################################################

    def build_path(
        self,
        layer: str,
        dataset: str,
        filename: str,
    ) -> str:
        """
        Creates a standard landing path.

        Example:

        finance/
            landing/
                master/
                    customers/
                        customers_001.csv
        """

        return (
            f"{AZURE_ROOT_FOLDER}/"
            f"{layer}/"
            f"{dataset}/"
            f"{filename}"
        )

    ###########################################################################

    def upload_dataset(
        self,
        local_file: Union[str, Path],
        *,
        layer: str,
        dataset: str,
    ) -> str:
        """
        Upload a generated dataset into the correct landing folder.
        """

        local_file = Path(local_file)

        remote_path = self.build_path(
            layer=layer,
            dataset=dataset,
            filename=local_file.name,
        )

        return self.upload(
            local_file,
            remote_path,
        )


###############################################################################


class LocalStorage:

    """
    Local storage backend.

    Keeps the same interface as ADLSStorage.
    """

    ###########################################################################

    def upload(
        self,
        local_file,
        remote_path,
        overwrite=True,
    ):
        return remote_path

    ###########################################################################

    def upload_dataset(
        self,
        local_file,
        *,
        layer,
        dataset,
    ):
        return local_file


###############################################################################


def get_storage():

    """
    Factory.

    Returns the configured storage backend.
    """

    backend = STORAGE_BACKEND.lower()

    if backend == "adls":
        return ADLSStorage()

    if backend == "local":
        return LocalStorage()

    raise ValueError(
        f"Unsupported storage backend: {backend}"
    )