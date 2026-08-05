"""
File Writer

Responsible only for writing datasets to the local filesystem.

It does NOT know anything about ADLS or SDP.
"""

from pathlib import Path
from datetime import datetime
import uuid

import pandas as pd

from generators.common.logger import logger


class FileWriter:

    ###########################################################################

    @staticmethod
    def generate_filename(
        dataset: str,
        extension: str,
    ) -> str:
        """
        Example

        customers_20260805_121530_4F8A.csv
        """

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        random_id = uuid.uuid4().hex[:4].upper()

        return (
            f"{dataset}_"
            f"{timestamp}_"
            f"{random_id}."
            f"{extension}"
        )

    ###########################################################################

    @staticmethod
    def ensure_directory(
        directory: Path,
    ):

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    ###########################################################################

    @staticmethod
    def write_csv(
        dataframe: pd.DataFrame,
        file_path: Path,
    ):

        dataframe.to_csv(
            file_path,
            index=False,
        )

    ###########################################################################

    @staticmethod
    def write_parquet(
        dataframe: pd.DataFrame,
        file_path: Path,
    ):

        dataframe.to_parquet(
            file_path,
            index=False,
        )

    ###########################################################################

    @classmethod
    def write(
        cls,
        dataframe: pd.DataFrame,
        dataset: str,
        output_directory: Path,
        file_format: str = "csv",
    ) -> Path:

        """
        Writes dataframe locally.

        Returns

            Path
        """

        cls.ensure_directory(output_directory)

        extension = file_format.lower()

        filename = cls.generate_filename(
            dataset,
            extension,
        )

        file_path = output_directory / filename

        if extension == "csv":

            cls.write_csv(
                dataframe,
                file_path,
            )

        elif extension == "parquet":

            cls.write_parquet(
                dataframe,
                file_path,
            )

        else:

            raise ValueError(
                f"Unsupported format : {extension}"
            )

        logger.info(
            f"Created {file_path}"
        )

        return file_path