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
    df: DataFrame = read_excel()

    try:
        logger.info("Configurazione del dataframe...")
        df: DataFrame = df[COLUMNS_REQUIRED]
        df: DataFrame = df.replace({np.nan: None, "": None})

        logger.info("Dataframe configurato")
        return df

    except Exception as err:
        logger.error(f"Errore generico durante la configurazione del dataframe - {err}", exc_info=True)
