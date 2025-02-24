from typing import Dict, Optional

import pandas as pd
from pandas import DataFrame

from src.utils.path import EXCEL_FILE_PATH
from src.utils.logger import logger


EXCEL_SHEET_NAME: str = "Film"
EXCEL_DTYPES: Dict[str, str] = {
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


def read_excel() -> Optional[DataFrame]:
    """Legge un file Excel tramite Pandas."""
    try:
        if not EXCEL_FILE_PATH.exists():
            raise FileNotFoundError(f"File Excel non trovato: {EXCEL_FILE_PATH}")

        if EXCEL_FILE_PATH.stat().st_size == 0:
            raise ValueError("Il file Excel è vuoto")

        df: DataFrame = pd.read_excel(
            EXCEL_FILE_PATH,
            sheet_name=EXCEL_SHEET_NAME,
            dtype=EXCEL_DTYPES,
            engine="openpyxl"
        )

        return df

    except FileNotFoundError as err:
        logger.error(err, exc_info=True)
    except ValueError as err:
        logger.error(err, exc_info=True)
    except Exception as err:
        logger.error(f"Errore generico durante la lettura del file Excel - {err}", exc_info=True)
