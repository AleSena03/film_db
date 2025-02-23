import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.errors import EmptyDataError

from src.utils.config import EXCEL_FILE_PATH, EXCEL_SHEET_NAME, EXCEL_COLUMNS_NAME, EXCEL_DTYPE
from src.utils.config import CSV_FILE_PATH, BACKUP_DIR_PATH
from src.utils.logger import logger


def excel_to_csv() -> None:

    try:
        if not EXCEL_FILE_PATH.exists():
            raise FileNotFoundError(f"File Excel non trovato: {EXCEL_FILE_PATH}")

        if EXCEL_FILE_PATH.stat().st_size == 0:
            raise EmptyDataError(f"Il file Excel è vuoto")

        if not os.access(EXCEL_FILE_PATH, os.R_OK):
            raise PermissionError(f"Errore permessi file")

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
            BACKUP_DIR_PATH.mkdir(parents=True, exist_ok=True)
            backup_name_csv: str = f"backup_{CSV_FILE_PATH.stem}{CSV_FILE_PATH.suffix}"
            backup_csv_path: Path = BACKUP_DIR_PATH / backup_name_csv
            if not backup_csv_path.exists():
                shutil.copy(CSV_FILE_PATH, backup_csv_path)
                logger.info(f"File CSV di backup creato: {backup_csv_path}")

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
    except PermissionError as err:
        logger.error(err, exc_info=True)
    except Exception as err:
        logger.error(f"Errore conversione - {err}", exc_info=True)
