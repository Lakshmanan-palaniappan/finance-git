"""
Publisher

Generator
    ↓
Publisher
    ↓
Storage Backend
        ├── Local
        ├── ADLS
        └── (Future) Unity Catalog Volume
"""

from pathlib import Path
from time import perf_counter

import pandas as pd

from generators.common.config import (
    DATASETS,
    SETTINGS,
    dataset_format,
    dataset_folder,
    dataset_prefix,
    dataset_type,
)

from generators.common.file_writer import FileWriter
from generators.common.storage import get_storage
from generators.common.paths import OUTPUT_PATH
from generators.common.logger import logger


class Publisher:

    ###########################################################################

    def __init__(self):

        self.storage = get_storage()

    ###########################################################################

    def publish(
        self,
        dataframe: pd.DataFrame,
        dataset_name: str,
    ):

        """
        Publish a generated dataframe.

        Steps

        1. Validate dataframe
        2. Write locally
        3. Upload to configured storage backend
        """

        #######################################################################
        # Validation
        #######################################################################

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
                f"{dataset_name} is not configured in environment.yml"
            )

        #######################################################################
        # Dataset Configuration
        #######################################################################

        layer = dataset_type(dataset_name)

        folder = dataset_folder(dataset_name)

        filename_prefix = dataset_prefix(dataset_name)

        file_format = dataset_format(dataset_name)

        #######################################################################
        # Local Write
        #######################################################################

        output_directory = (
            OUTPUT_PATH
            / layer
            / folder
        )

        local_file = FileWriter.write(
            dataframe=dataframe,
            dataset=filename_prefix,
            output_directory=output_directory,
            file_format=file_format,
        )

        logger.info(
            f"{dataset_name}: wrote "
            f"{len(dataframe):,} rows "
            f"to {local_file}"
        )

        #######################################################################
        # Storage Upload
        #######################################################################

        if SETTINGS.get("upload_to_adls", True):

            start = perf_counter()

            remote_path = self.storage.upload_dataset(
                local_file,
                layer=layer,
                dataset=folder,
            )

            elapsed = perf_counter() - start

            logger.info(
                f"{dataset_name}: uploaded "
                f"{Path(local_file).name} "
                f"-> {remote_path} "
                f"in {elapsed:.2f} sec."
            )

        else:

            logger.info(
                "Upload disabled. Local copy retained."
            )

        return local_file

    ###########################################################################

    def publish_multiple(
        self,
        datasets: dict[str, pd.DataFrame],
    ):

        """
        Publish multiple datasets.

        Example

            {
                "customers": customer_df,
                "accounts": account_df
            }
        """

        outputs = {}

        for dataset_name, dataframe in datasets.items():

            outputs[dataset_name] = self.publish(
                dataframe=dataframe,
                dataset_name=dataset_name,
            )

        return outputs