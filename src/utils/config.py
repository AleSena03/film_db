from pathlib import Path
from typing import List, Dict


ROOT_DIR_PATH: Path = Path(__file__).resolve().parent.parent.parent

LOG_DIR_PATH: Path = ROOT_DIR_PATH / "logs"
LOG_FILE_NAME: str = "logs.log"

BACKUP_DIR_PATH: Path = ROOT_DIR_PATH / "data" / "backup"
EXCEL_FILE_PATH: Path = ROOT_DIR_PATH / "data" / "raw" / "film_db.xlsx"
CSV_FILE_PATH: Path = ROOT_DIR_PATH / "data" / "processed" / "film_ds.csv"
EXCEL_SHEET_NAME: str = "Film"
EXCEL_COLUMNS_NAME: List[str] = [
        "titolo",
        "titolo_originale",
        "anno",
        "durata",
        "regia",
        "lingua_originale",
        "saga",
        "id_prequel",
        "id_sequel",
        "poster",
        "budget",
        "incasso_primo_weekend_usa",
        "incasso_usa",
        "incasso_globale",
        "valutazione_imdb"
]
EXCEL_DTYPE: Dict[str, str] = {
    "titolo": "string",
    "titolo_originale": "string",
    "regia": "string",
    "lingua_originale": "string",
    "saga": "string",
    "poster": "string",

    "id_film": "Int64",
    "anno": "Int64",
    "durata": "Int64",
    "id_prequel": "Int64",
    "id_sequel": "Int64",
    "budget": "Int64",
    "incasso_primo_weekend_usa": "Int64",
    "incasso_usa": "Int64",
    "incasso_globale": "Int64",

    "valutazione_imdb": "float64"
}

POLL_INTERVAL: int = 2
