from pathlib import Path
from datetime import datetime


def write_csv(df, folder: Path, prefix: str):

    folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = folder / f"{prefix}_{timestamp}.csv"

    df.to_csv(file_path, index=False)

    return file_path