"""
Write generated datasets locally.
"""

from pathlib import Path
from datetime import datetime

from generators.common.config import DATASETS


class FileWriter:

    @staticmethod
    def write(df, dataset, output_directory):

        Path(output_directory).mkdir(

            parents=True,

            exist_ok=True

        )

        prefix = DATASETS[dataset]["filename_prefix"]

        filename = (

            f"{prefix}_"

            f"{datetime.now():%Y%m%d_%H%M%S}.csv"

        )

        path = Path(output_directory) / filename

        df.to_csv(

            path,

            index=False

        )

        return str(path)