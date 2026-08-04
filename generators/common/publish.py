"""
Publisher

Generator
    ↓
Local File
    ↓
Azure Data Lake Storage
"""

from pathlib import Path

from generators.common.config import (
    DATASETS,
    PATHS,
)

from generators.common.file_writer import FileWriter
from generators.common.storage import ADLSStorage
from generators.common.paths import OUTPUT_PATH
from generators.common.logger import logger


class Publisher:

    def __init__(self):

        self.storage = ADLSStorage()

    ##############################################################

    def publish(
        self,
        dataframe,
        dataset_name: str
    ):

        if dataset_name not in DATASETS:

            raise ValueError(
                f"{dataset_name} not found in environment.yml datasets."
            )

        dataset = DATASETS[dataset_name]

        folder = dataset["folder"]

        filename_prefix = dataset["filename_prefix"]

        file_format = dataset.get(
            "format",
            "csv"
        )

        local_directory = OUTPUT_PATH / folder

        local_file = FileWriter.write(

            dataframe=dataframe,

            dataset=filename_prefix,

            output_directory=local_directory,

            file_format=file_format

        )

        remote_path = (

            f"{PATHS['landing']}/"

            f"{folder}/"

            f"{Path(local_file).name}"

        )

        self.storage.upload(

            local_file,

            remote_path

        )

        logger.info(

            f"{dataset_name} published successfully."

        )

        return local_file