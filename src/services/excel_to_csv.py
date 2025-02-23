import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.errors import EmptyDataError

from src.utils.config import EXCEL_FILE_PATH, EXCEL_SHEET_NAME, EXCEL_COLUMNS_NAME, EXCEL_DTYPE
from src.utils.config import CSV_FILE_PATH
from src.utils.logger import logger


def excel_to_csv() -> None:

    try:
        if not EXCEL_FILE_PATH.exists():
            raise FileNotFoundError(f"File Excel non trovato: {EXCEL_FILE_PATH}")

        if EXCEL_FILE_PATH.stat().st_size == 0:
            raise EmptyDataError(f"Il file Excel è vuoto")

        logger.info("Avvio conversione Excel -> CSV")

        df: DataFrame = pd.read_excel(
            EXCEL_FILE_PATH,
            sheet_name=EXCEL_SHEET_NAME,
            engine="openpyxl",
            dtype=EXCEL_DTYPE
        )

        df: DataFrame = df[EXCEL_COLUMNS_NAME]
        df: DataFrame = df.replace({np.nan: None, "": None})

        CSV_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

        if CSV_FILE_PATH.exists():
            backup_csv: Path = CSV_FILE_PATH.with_stem(f"backup_{CSV_FILE_PATH.stem}")
            if not backup_csv.exists():
                shutil.copy(CSV_FILE_PATH, backup_csv)
                logger.info(f"File CSV di backup creato: {backup_csv}")

        df.to_csv(
            str(CSV_FILE_PATH),
            index=False,
            encoding="utf8"
        )

        logger.info("Conversione avvenuta con successo")

    except FileNotFoundError as err:
        logger.error(err, exc_info=True)
    except EmptyDataError as err:
        logger.error(err, exc_info=True)
    except PermissionError:
        logger.error(f"Errore permessi file", exc_info=True)
    except Exception as err:
        logger.error(f"Errore conversione - {err}", exc_info=True)
