from pandas import DataFrame

from src.utils.path import CSV_FILE_PATH
from src.utils.logger import logger
from src.services.config_df import config_df


def to_csv() -> None:
    """Converte un dataframe Excel in un file CSV."""
    try:
        df: DataFrame = config_df()
        logger.info("Conversione Excel -> CSV...")
        df.to_csv(
            str(CSV_FILE_PATH),
            index=False,
            encoding="utf8"
        )

        logger.info("Conversione avvenuta con successo")

    except Exception as err:
        logger.error(f"Errore generico durante la conversione in CSV - {err}", exc_info=True)
        return None
