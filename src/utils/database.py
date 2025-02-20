"""Modulo che gestisce la connessione con il database."""
from typing import Tuple, Dict, Optional

import mysql.connector
from mysql.connector import Error
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

from logger import logger


class GestoreDatabase:
    """Gestisce la connessione col database."""

    def __init__(self, config: Dict[str, str]) -> None:
        """Inizializza le informazioni di configurazione del database."""
        self.config = config
        self.connessione: Optional[MySQLConnectionAbstract] = None
        self.cursore: Optional[MySQLCursorAbstract] = None

    def __enter__(self) -> Optional[Tuple[MySQLConnectionAbstract, MySQLCursorAbstract]]:
        """Apre la connessione al database."""
        try:
            self.connessione = mysql.connector.connect(**self.config)
            self.cursore = self.connessione.cursor(dictionary=True)
            logger.info("Apertura della connessione al database avvenuta con successo.")
            return self.connessione, self.cursore

        except Error as errore:
            logger.error(f"Errore di connessione al database - {errore}", exc_info=True)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Chiude la connessione col database."""
        try:
            if self.cursore:
                self.cursore.close()

            if self.connessione:

                if exc_type:
                    self.connessione.rollback()

                else:
                    self.connessione.commit()

                self.connessione.close()
                logger.info("Chiusura della connessione col database avvenuta con successo.")

        except Error as errore:
            logger.error(f"Errore di chiusura della connessione con il database - {errore}")

            if not exc_type:
                raise
