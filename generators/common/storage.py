"""
Azure Data Lake Storage Utility

Authentication Priority
-----------------------
1. Azure CLI (az login)
2. Managed Identity (Databricks)
3. Service Principal (future)

No code changes are required between local and Databricks.
"""

from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

from generators.common.config import (
    AZURE_STORAGE_ACCOUNT,
    AZURE_CONTAINER
)

from generators.common.logger import logger


class ADLSStorage:

    def __init__(self):

        self.account_name = AZURE_STORAGE_ACCOUNT
        self.container_name = AZURE_CONTAINER

        self.credential = DefaultAzureCredential()

        self.service_client = DataLakeServiceClient(
            account_url=f"https://{self.account_name}.dfs.core.windows.net",
            credential=self.credential
        )

        self.file_system = self.service_client.get_file_system_client(
            self.container_name
        )

        logger.info(
            f"Connected to ADLS Container: {self.container_name}"
        )

    #####################################################################

    def create_directory(self, directory: str):

        try:

            self.file_system.create_directory(directory)

            logger.info(
                f"Directory created: {directory}"
            )

        except Exception:

            logger.debug(
                f"Directory already exists: {directory}"
            )

    #####################################################################

    def upload(
        self,
        local_file: str,
        remote_path: str
    ):

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
            f"Uploaded: {local_file.name} -> {remote_path}"
        )

        return remote_path

    #####################################################################

    def download(
        self,
        remote_path: str,
        local_file: str
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

            file.write(download.readall())

        logger.info(
            f"Downloaded: {remote_path}"
        )

    #####################################################################

    def exists(
        self,
        remote_path: str
    ) -> bool:

        try:

            self.file_system.get_file_client(
                remote_path
            ).get_file_properties()

            return True

        except Exception:

            return False

    #####################################################################

    def delete(
        self,
        remote_path: str
    ):

        self.file_system.delete_file(
            remote_path
        )

        logger.info(
            f"Deleted: {remote_path}"
        )

    #####################################################################

    def list_files(
        self,
        directory: str = ""
    ):

        paths = self.file_system.get_paths(
            path=directory
        )

        return [path.name for path in paths]

    #####################################################################

    def upload_dataframe(
        self,
        dataframe,
        remote_path: str
    ):
        """
        Upload dataframe directly without writing locally.
        Mainly useful for future Databricks jobs.
        """

        import io

        csv_buffer = io.StringIO()

        dataframe.to_csv(
            csv_buffer,
            index=False
        )

        file_client = self.file_system.get_file_client(
            remote_path
        )

        file_client.upload_data(
            csv_buffer.getvalue(),
            overwrite=True
        )

        logger.info(
            f"Uploaded dataframe -> {remote_path}"
        )