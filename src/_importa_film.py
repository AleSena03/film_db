"""Importa i film, da un file Excel, ad un database MySQL."""
import logging
import configparser
from logging import Logger, Formatter, FileHandler, StreamHandler, INFO
from configparser import ConfigParser
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

import mysql.connector
import numpy as np
import pandas as pd
from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from pandas import DataFrame


def configura_logger() -> Logger:
    """Configura il logger."""
    log: Logger = logging.getLogger(__name__)
    log.setLevel(INFO)

    formatter: Formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler: FileHandler = FileHandler("logging_info.log", mode="a")
    file_handler.setFormatter(formatter)

    stream_handler: StreamHandler = StreamHandler()
    stream_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    log.addHandler(stream_handler)

    return log


logger: Logger = configura_logger()


def configura_db(nome_file: str = "configurazione_db.ini") -> Dict[str, str]:
    """Configura il database tramite le informazioni presenti nel file."""
    configurazione: ConfigParser = configparser.ConfigParser()
    configurazione.read(nome_file)

    return {
        "host": configurazione["database"]["host"],
        "user": configurazione["database"]["user"],
        "password": configurazione["database"]["password"],
        "database": configurazione["database"]["db"],
    }


class ConnessioneDatabase:
    """Gestisce la connessione al database."""

    def __init__(self, configurazione: Dict[str, str]) -> None:
        """Inizializza la connessione al database."""
        self.configurazione = configurazione
        self.connessione: Optional[MySQLConnectionAbstract] = None
        self.cursore: Optional[MySQLCursorAbstract] = None

    def __enter__(self) -> Optional[Tuple[MySQLConnectionAbstract, MySQLCursorAbstract]]:
        """Testa la connessione al database."""
        try:
            self.connessione = mysql.connector.connect(**self.configurazione)
            self.cursore = self.connessione.cursor()
            return self.connessione, self.cursore

        except Error as errore:
            logger.error(f"Errore di connessione al database\n{errore}")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Chiude la connessione al database."""
        try:
            if self.cursore:
                self.cursore.close()

            if self.connessione:
                if exc_type:
                    self.connessione.rollback()
                else:
                    self.connessione.commit()
                self.connessione.close()

        except Error as errore:
            logger.error(f"Errore di chiusura della connessione\n{errore}")


def valida_df(df: DataFrame) -> DataFrame:
    """Valida e pulisce i dati per inserirli nel dataframe."""
    df = df.replace({np.nan: None, "": None})

    if df["titolo"].isnull().any():
        conta_titoli_vuoti: int = df["titolo"].isnull().sum()
        logger.error(f"Sono stati trovati {conta_titoli_vuoti} film senza titolo.\n"
                      f"Verranno eliminati...")
        df = df.dropna(subset=["titolo"])

    return df


def carica_df(percorso_file: Path) -> Optional[DataFrame]:
    """Carica i dati da Excel."""
    try:
        df = pd.read_excel(percorso_file, sheet_name="Film")
        df = df[["titolo",
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
                 "valutazione_imdb"]]

        return valida_df(df)

    except Exception as errore:
        logger.error(f"Errore nel caricamento del file Excel\n{errore}")


def importa_film(cursore: MySQLCursorAbstract, df: DataFrame) -> None:
    """Importa i dati dal dataframe al database."""
    try:
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
            (
                riga["titolo"],
                riga["titolo_originale"],
                riga["anno"],
                (riga["durata"]),
                riga["regia"],
                riga["lingua_originale"],
                riga["saga"],
                riga["id_prequel"],
                riga["id_sequel"],
                riga["poster"],
                riga["budget"],
                riga["incasso_primo_weekend_usa"],
                riga["incasso_usa"],
                riga["incasso_globale"],
                riga["valutazione_imdb"]
            )
            for indice, riga in df.iterrows()
        ]

        cursore.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursore.executemany(query_sql, data)
        cursore.execute("SET FOREIGN_KEY_CHECKS = 1")

        logger.info(f"Inseriti con successo {len(data)} film")

    except Error as errore:
        cursore.execute("SET FOREIGN_KEY_CHECKS = 1")
        logger.error(f"Errore durante l'inserimento di dati\n{errore}")


def main() -> None:
    """Esegue il modulo."""
    try:
        configurazione: Dict[str, str] = configura_db()
        percorso_file_excel = Path.home() / "OneDrive" / "Documenti" / "progetti" / "film_db" / "film.xlsx"

        df: DataFrame = carica_df(percorso_file_excel)

        with ConnessioneDatabase(configurazione) as (connessione, cursore):
            importa_film(cursore, df)

    except Exception as errore:
        logger.error(f"Errore non gestito\n{errore}", exc_info=True)

    finally:
        logger.info("Processo di importazione completato con successo!")


if __name__ == "__main__":
    main()
