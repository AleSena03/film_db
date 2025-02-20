"""Modulo che valida il file Excel e carica i dati contenuti al suo interno."""
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from pandas import DataFrame

from utils.logger import logger


def valida_excel(path_excel: Path) -> None:
    """Valida il file Excel."""
    if not path_excel.exists():
        logger.error(f"Il file '{path_excel}' non è stato trovato.")
        raise FileNotFoundError(f"Il file '{path_excel}' non è stato trovato.")

    if path_excel.stat().st_size == 0:
        logger.error(f"Il file '{path_excel}' è vuoto.")
        raise ValueError(f"Il file '{path_excel}' è vuoto.")

def valida_dati(path_excel: Path) -> DataFrame:
    """Carica e valida i dati del file Excel."""
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
