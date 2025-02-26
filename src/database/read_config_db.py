from configparser import ConfigParser
from typing import List, Dict, Optional

from src.utils.path import CONFIG_DB_FILE_PATH
from src.utils.logger import logger


CONFIG_SECTION: str = "database"
CONFIG_OPTIONS: List[str] = [
    "host",
    "port",
    "user",
    "password",
    "db",
    "charset",
    "timeout"
]


def read_config_db() -> Optional[Dict[str, str]]:

    try:
        if not CONFIG_DB_FILE_PATH.exists():
            raise FileNotFoundError(f"File di configurazione del database non trovato: {CONFIG_DB_FILE_PATH}")

        if not CONFIG_DB_FILE_PATH.is_file():
            raise ValueError(f"Il percorso {CONFIG_DB_FILE_PATH} non è un file")

        if CONFIG_DB_FILE_PATH.stat().st_size == 0:
            raise ValueError("Il file di configurazione del database è vuoto")

        config_parser: ConfigParser = ConfigParser()
        config_parser.read(CONFIG_DB_FILE_PATH)

        if not config_parser.has_section(CONFIG_SECTION):
            raise ValueError(f"Il file di configurazione del database non ha la sezione [{CONFIG_SECTION}]")

        config: Dict[str, str] = {}

        for option in CONFIG_OPTIONS:
            if not config_parser.has_option(CONFIG_SECTION, option):
                raise ValueError(f"Opzione '{option}' mancante nel file di configurazione.")

            config[option] = config_parser.get(CONFIG_SECTION, option)

        config["database"] = config.pop("db")
        return config

    except FileNotFoundError as err:
        logger.error(err, exc_info=True)
    except ValueError as err:
        logger.error(err, exc_info=True)
    except Exception as err:
        logger.error(f"Errore generico durante la lettura del file di configurazione del database - {err}", exc_info=True)
