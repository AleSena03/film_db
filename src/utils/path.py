from pathlib import Path


ROOT_DIR_PATH: Path = Path(__file__).resolve().parent.parent.parent

LOG_DIR_PATH: Path = ROOT_DIR_PATH / "logs"

EXCEL_FILE_PATH: Path = ROOT_DIR_PATH / "data" / "raw" / "film_db.xlsx"
CSV_FILE_PATH: Path = ROOT_DIR_PATH / "data" / "processed" / "film_ds.csv"

POLL_INTERVAL: int = 2
