"""
Azure Data Lake Storage Utility

Supports

1. Interactive Browser
2. Azure CLI
3. Managed Identity

No code changes required between environments.
"""

from pathlib import Path
import io

from azure.identity import (
    InteractiveBrowserCredential,
    AzureCliCredential,
    DefaultAzureCredential,
)

from azure.storage.filedatalake import (
    DataLakeServiceClient,
)

from generators.common.config import (
    AZURE_STORAGE_ACCOUNT,
    AZURE_CONTAINER,
    AUTH_MODE,
)

from generators.common.logger import logger


def get_credential():

    if AUTH_MODE.lower() == "browser":

        logger.info(
            "Using InteractiveBrowserCredential"
        )

        return InteractiveBrowserCredential()

    elif AUTH_MODE.lower() == "azure_cli":

        logger.info(
            "Using AzureCliCredential"
        )

        return AzureCliCredential()

    elif AUTH_MODE.lower() == "managed_identity":

        logger.info(
            "Using DefaultAzureCredential"
        )

        return DefaultAzureCredential()

    else:

        raise ValueError(
            f"Unsupported auth mode : {AUTH_MODE}"
        )


class ADLSStorage:

    def __init__(self):

        self.account_name = AZURE_STORAGE_ACCOUNT

        self.container_name = AZURE_CONTAINER

        self.credential = get_credential()

        self.service_client = DataLakeServiceClient(

            account_url=(
                f"https://"
                f"{self.account_name}"
                f".dfs.core.windows.net"
            ),

            credential=self.credential

        )

        self.file_system = (
            self.service_client.get_file_system_client(
                self.container_name
            )
        )

        logger.info(
            f"Connected to ADLS container : "
            f"{self.container_name}"
        )

    ##########################################################

    def create_directory(self, directory):

        try:

            self.file_system.create_directory(directory)

        except Exception:

            pass

    ##########################################################

    def upload(self, local_file, remote_path):

        local_file = Path(local_file)

        self.create_directory(
            str(Path(remote_path).parent)
        )

        file_client = self.file_system.get_file_client(
            remote_path
        )

        with open(local_file, "rb") as file:

            file_client.upload_data(
                file,
                overwrite=True
            )

        logger.info(
            f"Uploaded {local_file.name}"
        )

        return remote_path

    ##########################################################

    def upload_dataframe(
        self,
        dataframe,
        remote_path
    ):

        csv_buffer = io.StringIO()

        dataframe.to_csv(
            csv_buffer,
            index=False
        )

        self.create_directory(
            str(Path(remote_path).parent)
        )

        file_client = self.file_system.get_file_client(
            remote_path
        )

        file_client.upload_data(
            csv_buffer.getvalue(),
            overwrite=True
        )

        logger.info(
            f"Uploaded dataframe -> "
            f"{remote_path}"
        )

    ##########################################################

    def download(
        self,
        remote_path,
        local_file
    ):

        file_client = self.file_system.get_file_client(
            remote_path
        )

        download = file_client.download_file()

        Path(local_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(local_file, "wb") as file:

            file.write(
                download.readall()
            )

    ##########################################################

    def delete(self, remote_path):

        self.file_system.delete_file(
            remote_path
        )

    ##########################################################

    def exists(self, remote_path):

        try:

            self.file_system.get_file_client(
                remote_path
            ).get_file_properties()

            return True

        except Exception:

            return False

    ##########################################################

    def list_files(self, directory=""):

        paths = self.file_system.get_paths(
            path=directory
        )

        return [
            path.name
            for path in paths
        ]