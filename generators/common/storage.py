"""
Azure Data Lake Storage Utility

Authentication:
Service Principal

Works for:
- Local Development
- Azure VM
- CI/CD

Later we'll switch to Managed Identity in Databricks.
"""

from pathlib import Path
import io

from azure.identity import ClientSecretCredential

from azure.storage.filedatalake import (
    DataLakeServiceClient,
)

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

        self.account_name = AZURE_STORAGE_ACCOUNT

        self.container_name = AZURE_CONTAINER

        self.credential = ClientSecretCredential(

            tenant_id=AZURE_TENANT_ID,

            client_id=AZURE_CLIENT_ID,

            client_secret=AZURE_CLIENT_SECRET

        )

        self.service_client = DataLakeServiceClient(

            account_url=(
                f"https://{self.account_name}.dfs.core.windows.net"
            ),

            credential=self.credential

        )

        self.file_system = self.service_client.get_file_system_client(
            self.container_name
        )

        logger.info(
            f"Connected to ADLS Container: {self.container_name}"
        )

    ##################################################################

    def create_directory(self, directory):

        try:

            self.file_system.create_directory(directory)

            logger.info(
                f"Created directory: {directory}"
            )

        except Exception:

            pass

    ##################################################################

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
            f"Uploaded {local_file.name} -> {remote_path}"
        )

        return remote_path

    ##################################################################

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
            f"Uploaded dataframe -> {remote_path}"
        )

    ##################################################################

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

    ##################################################################

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

    ##################################################################

    def delete(
        self,
        remote_path
    ):

        self.file_system.delete_file(
            remote_path
        )

        logger.info(
            f"Deleted: {remote_path}"
        )

    ##################################################################

    def list_files(
        self,
        directory=""
    ):

        paths = self.file_system.get_paths(
            path=directory
        )

        return [path.name for path in paths]

    ##################################################################

    def upload_text(
        self,
        text,
        remote_path
    ):

        self.create_directory(
            str(Path(remote_path).parent)
        )

        file_client = self.file_system.get_file_client(
            remote_path
        )

        file_client.upload_data(
            text,
            overwrite=True
        )

        logger.info(
            f"Uploaded text -> {remote_path}"
        )