"""Modulo che carica e valida la configurazione del database."""
import configparser
from configparser import ConfigParser
from pathlib import Path
from typing import List, Dict

from logger import logger


def config_db(file_config: str = "config_db.ini") -> Dict[str, str]:
    """
    Carica e valida la configurazione del database.

    Parameters
    ----------
    file_config : str
        Nome del file .ini

    Returns
    -------
    Dict[str, str]
        Dizionario con le informazioni necessarie per configurare il database.
    """
    path_root: Path = Path(__file__).resolve().parent.parent.parent
    path_config: Path = path_root / "config" / file_config

    # VERIFICA ESISTENZA DEL FILE .INI
    if not path_config.exists():
        logger.error(f"Il file '{path_config}' non è stato trovato.")
        raise FileNotFoundError(f"Il file '{path_config}' non è stato trovato.")

    config: ConfigParser = configparser.ConfigParser()
    config.read(path_config)

    # VERIFICA L'ESISTENZA DELLA SEZIONE NECESSARIA
    if not config.has_section("database"):
        logger.error("Sezione [database] mancante nel file di configurazione.")
        raise ValueError("Sezione [database] mancante nel file di configurazione.")

    keys: List[str] = [
        "host",
        "user",
        "password",
        "db"
    ]

    configurazione_db: Dict = {}

    for key in keys:
        # VERIFICA L'ESISTENZA DELLE OPZIONI NECESSARIE
        if not config.has_option("database", key):
            logger.error(f"Chiave '{key}' mancante nel file di configurazione.")
            raise ValueError(f"Chiave '{key}' mancante nel file di configurazione.")
        configurazione_db[key] = config.get("database", key)

    configurazione_db["database"] = configurazione_db.pop("db")
    logger.info("Configurazione del database caricata con successo.")
    return configurazione_db
