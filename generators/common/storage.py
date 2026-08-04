"""
Azure Data Lake Storage Utility

Authentication:
    Service Principal

Responsibilities:
    - Connect to ADLS Gen2
    - Create directories
    - Upload files
    - Upload DataFrames
    - Download files
    - Delete files
    - Check existence
    - List files
"""

from pathlib import Path
import io

from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient

from generators.common.config import (
    AZURE_STORAGE_ACCOUNT,
    AZURE_CONTAINER,
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
)

from generators.common.logger import logger


class ADLSStorage:

    def __init__(self):

        self.credential = ClientSecretCredential(
            tenant_id=AZURE_TENANT_ID,
            client_id=AZURE_CLIENT_ID,
            client_secret=AZURE_CLIENT_SECRET
        )

        self.service_client = DataLakeServiceClient(
            account_url=f"https://{AZURE_STORAGE_ACCOUNT}.dfs.core.windows.net",
            credential=self.credential
        )

        self.file_system = self.service_client.get_file_system_client(
            AZURE_CONTAINER
        )

        logger.info(
            "Connected to Azure Data Lake Storage."
        )

    ###########################################################

    def create_directory(self, directory: str):

        try:

            self.file_system.create_directory(directory)

        except Exception:

            # Directory already exists
            pass

    ###########################################################

    def upload(
        self,
        local_file,
        remote_path
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
            f"Uploaded {local_file.name}"
        )

        return remote_path

    ###########################################################

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

    ###########################################################

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

            file.write(download.readall())

    ###########################################################

    def delete(
        self,
        remote_path
    ):

        self.file_system.delete_file(
            remote_path
        )

    ###########################################################

    def exists(
        self,
        remote_path
    ):

        try:

            self.file_system.get_file_client(
                remote_path
            ).get_file_properties()

            return True

        except Exception:

            return False

    ###########################################################

    def list_files(
        self,
        directory=""
    ):

        return [
            path.name
            for path in self.file_system.get_paths(
                path=directory
            )
        ]