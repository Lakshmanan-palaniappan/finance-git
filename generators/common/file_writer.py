"""
File Writer

Writes generated datasets to local storage before they are
published to ADLS.
"""

from pathlib import Path
from datetime import datetime

import pandas as pd

from generators.common.logger import logger


class FileWriter:

    @staticmethod
    def write(
        dataframe: pd.DataFrame,
        dataset: str,
        output_directory: Path,
        file_format: str = "csv"
    ) -> Path:

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = f"{dataset}_{timestamp}.{file_format}"

        output_file = output_directory / filename

        if file_format.lower() == "csv":

            dataframe.to_csv(
                output_file,
                index=False
            )

        elif file_format.lower() == "parquet":

            dataframe.to_parquet(
                output_file,
                index=False
            )

        else:

            raise ValueError(
                f"Unsupported file format: {file_format}"
            )

        logger.info(
            f"Written dataset '{dataset}' to {output_file}"
        )

        return output_file