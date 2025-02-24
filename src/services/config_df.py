from typing import List, Optional

import numpy as np
from pandas import DataFrame

from src.utils.logger import logger
from src.services.read_excel import read_excel


COLUMNS_REQUIRED: List[str] = [
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


def config_df() -> Optional[DataFrame]:
    """Configura un dataframe."""
    try:
        df: DataFrame = read_excel()
        miss_columns: List[str] = [col for col in COLUMNS_REQUIRED if col not in df.columns]
        if miss_columns:
            logger.error(f"Colonne mancanti nel dataframe: {", ".join(miss_columns)}")
            return None

        df: DataFrame = df[COLUMNS_REQUIRED]
        df: DataFrame = df.replace({np.nan: None, "": None})

        initial_record: int = len(df)
        df: DataFrame = df.dropna(subset=["titolo"])

        removed_record: int = initial_record - len(df)
        if removed_record > 0:
            logger.warning(f"Rimossi: {removed_record} record con titolo mancante o non valido")

        if df.empty:
            logger.error("Nessuna record rimasto")
            return None

        return df

    except Exception as err:
        logger.error(f"Errore generico durante la configurazione del dataframe - {err}", exc_info=True)
        return None
