"""Modulo che importa nel database i dati, del file Excel, caricati e validati."""
from pathlib import Path
from typing import List, Tuple, Any

import numpy as np
import pandas as pd
from pandas import DataFrame
from mysql.connector import Error
from mysql.connector.abstracts import MySQLCursorAbstract

from logger import logger


def valida_excel(path_excel: Path) -> None:
    """Valida il file Excel."""
    if not path_excel.exists():
        logger.error(f"Il file '{path_excel}' non è stato trovato.")
        raise FileNotFoundError(f"Il file '{path_excel}' non è stato trovato.")

    if path_excel.stat().st_size == 0:
        logger.error(f"Il file '{path_excel}' è vuoto.")
        raise ValueError(f"Il file '{path_excel}' è vuoto.")


def config_df(path_excel: Path) -> DataFrame:
    """Carica e valida i dati di Excel."""
    valida_excel(path_excel)

    try:
        df: DataFrame = pd.read_excel(path_excel, sheet_name="Film")

    except Exception as errore:
        logger.error(f"Errore di lettura del file Excel - {errore}")
        raise

    colonne_necessarie: List = [
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

    colonne_mancanti: List = [col for col in colonne_necessarie if col not in df.columns]
    if colonne_mancanti:
        logger.error(f"Colonne mancanti: {", ".join(colonne_mancanti)}")
        raise ValueError(f"Colonne mancanti: {", ".join(colonne_mancanti)}")

    # CREAZIONE DEL DATAFRAME DELLE SOLE COLONNE NECESSARIE
    df = df[colonne_necessarie]

    # PULIZIA DATAFRAME
    df = df.replace({np.nan: None, "": None})
    df = df.dropna(subset=["titolo"])

    if df.empty:
        logger.error("Nessun dato valido dopo la pulizia del dataframe.")

    return df


def importa(cursore: MySQLCursorAbstract, df: DataFrame) -> None:
    """Importa nel database i dati del dataframe."""
    query_sql: str = """
                    INSERT INTO film (
                        titolo,
                        titolo_originale,
                        anno,
                        durata,
                        regia,
                        lingua_originale,
                        saga,
                        id_prequel,
                        id_sequel,
                        poster,
                        budget,
                        incasso_primo_weekend_usa,
                        incasso_usa,
                        incasso_globale,
                        valutazione_imdb
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

    data: List[Tuple[Any, ...]] = [
        tuple(riga) for riga in df.to_numpy()
    ]

    try:
        cursore.execute("START TRANSACTION")
        cursore.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursore.executemany(query_sql, data)
        cursore.execute("SET FOREIGN_KEY_CHECKS = 1")
        cursore.execute("COMMIT")

        logger.info(f"Importati con successo {len(data)} record")

    except Error as errore:
        cursore.execute("ROLLBACK")
        logger.error(f"Errore durante l'importazione dei dati - {errore}")
        raise

    except Exception as errore:
        cursore.execute("ROLLBACK")
        logger.error(f"Errore durante l'importazione dei dati - {errore}")
        raise

    cursore.execute("SET FOREIGN_KEY_CHECKS = 1")
