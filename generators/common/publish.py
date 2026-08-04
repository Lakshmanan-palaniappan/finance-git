"""
Publisher

Generator
    ↓
Local Output
    ↓
Azure Data Lake Storage
"""

from pathlib import Path
from time import perf_counter

import pandas as pd

from generators.common.config import (
    DATASETS,
    PATHS,
    SETTINGS
)

from generators.common.file_writer import FileWriter
from generators.common.storage import ADLSStorage
from generators.common.paths import OUTPUT_PATH
from generators.common.logger import logger


class Publisher:

    ###############################################################

    def __init__(self):

        self.storage = ADLSStorage()

    ###############################################################

    def publish(
        self,
        dataframe: pd.DataFrame,
        dataset_name: str
    ):

        if dataframe is None:

            logger.info(
                f"{dataset_name}: dataframe is None."
            )

            return None

        if dataframe.empty:

            logger.info(
                f"{dataset_name}: no records generated."
            )

            return None

        if dataset_name not in DATASETS:

            raise ValueError(
                f"{dataset_name} not found in environment.yml."
            )

        dataset = DATASETS[dataset_name]

        dataset_type = dataset["type"]

        folder = dataset["folder"]

        filename = dataset["filename_prefix"]

        file_format = dataset.get(
            "format",
            "csv"
        )

        ###########################################################
        # Local Write
        ###########################################################

        output_directory = (

            OUTPUT_PATH

            / dataset_type

            / folder

        )

        local_file = FileWriter.write(

            dataframe=dataframe,

            dataset=filename,

            output_directory=output_directory,

            file_format=file_format

        )

        ###########################################################
        # ADLS Upload
        ###########################################################

        if SETTINGS.get(
            "upload_to_adls",
            True
        ):

            remote_path = (

                f"{PATHS['landing']}/"

                f"{dataset_type}/"

                f"{folder}/"

                f"{Path(local_file).name}"

            )

            start = perf_counter()

            self.storage.upload(

                local_file,

                remote_path

            )

            elapsed = perf_counter() - start

            logger.info(

                f"Uploaded "

                f"{len(dataframe)} rows "

                f"to {remote_path} "

                f"in {elapsed:.2f} sec."

            )

        else:

            logger.info(

                "ADLS upload disabled."

            )

        return local_file