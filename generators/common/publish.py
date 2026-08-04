"""
Publishes datasets.

Local
↓

ADLS Landing
"""

from pathlib import Path

from generators.common.file_writer import FileWriter
from generators.common.storage import ADLSStorage
from generators.common.paths import OUTPUT_PATH
from generators.common.config import PATHS
from generators.common.logger import logger


class Publisher:

    storage = ADLSStorage()

    @classmethod
    def publish(cls, dataframe, dataset):

        folder = OUTPUT_PATH / dataset

        file_path = FileWriter.write(

            dataframe,

            dataset,

            folder

        )

        landing = PATHS["landing"]

        remote_path = (

            f"{landing}/"

            f"{dataset}/"

            f"{Path(file_path).name}"

        )

        cls.storage.upload(

            file_path,

            remote_path

        )

        logger.info(

            f"Uploaded {remote_path}"

        )

        return file_path