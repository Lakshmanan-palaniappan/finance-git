"""
Azure Data Lake Storage
"""

from pathlib import Path

from azure.identity import DefaultAzureCredential

from azure.storage.filedatalake import (
    DataLakeServiceClient
)

from generators.common.config import AZURE
from generators.common.logger import logger


class ADLSStorage:

    ###############################################################

    def __init__(self):

        credential = DefaultAzureCredential()

        account_url = (

            f"https://"

            f"{AZURE['storage_account']}"

            ".dfs.core.windows.net"

        )

        self.service = DataLakeServiceClient(

            account_url=account_url,

            credential=credential

        )

        self.filesystem = self.service.get_file_system_client(

            AZURE["container"]

        )

        logger.info(

            "Connected to Azure Data Lake Storage."

        )

    ###############################################################

    def upload(

        self,

        local_file,

        remote_path

    ):

        local_file = Path(local_file)

        directory = str(

            Path(remote_path).parent

        )

        filename = Path(remote_path).name

        try:

            self.filesystem.create_directory(

                directory

            )

        except Exception:

            pass

        file_client = self.filesystem.get_file_client(

            remote_path

        )

        with open(

            local_file,

            "rb"

        ) as file:

            file_client.upload_data(

                file,

                overwrite=True

            )

        logger.info(

            f"Uploaded {filename}"

        )