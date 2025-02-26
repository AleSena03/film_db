from pathlib import Path


ROOT_DIR_PATH: Path = Path(__file__).resolve().parent.parent.parent

CONFIG_DB_FILE_PATH: Path = (ROOT_DIR_PATH / "config" / "config_db.ini").resolve()
LOG_DIR_PATH: Path = (ROOT_DIR_PATH / "logs").resolve()

EXCEL_FILE_PATH: Path = (ROOT_DIR_PATH / "data" / "raw" / "film_db.xlsx").resolve()
CSV_FILE_PATH: Path = (ROOT_DIR_PATH / "data" / "processed" / "film_ds.csv").resolve()
