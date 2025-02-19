"""Modulo che configura un sistema avanzato di logging."""
import logging
from logging import Logger, Formatter, StreamHandler, INFO
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


# PERCORSO DEL PROGETTO (es. film_db/...)
PERCORSO_PROGETTO: Path = Path(__file__).resolve().parent.parent
PERCORSO_CARTELLA_LOG: Path = PERCORSO_PROGETTO / "logs"
PERCORSO_FILE_LOG: Path = PERCORSO_CARTELLA_LOG / "importa_log.log"


def configura_logger(
        nome_file: Optional[Path] = None,
        bytes_max: int = 1048576,
        file_backup: int = 5
) -> Logger:
    """
    Configura un logger.

    Parameters
    ----------
    nome_file : Optional[str] = None
        Percorso del file di log.
    bytes_max : int = 1048576 (1 MB)
        Dimensione massima del file.
    file_backup : int = 5
        Numero massimo di file di log da mantenere.

    Returns
    -------
    Logger
        Logger configurato.
    """
    log: Logger = logging.getLogger(__name__)
    log.setLevel(INFO)

    # EVITA ACCUMULO DI HANDLER
    if not log.handlers:
        formatter: Formatter = Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        if nome_file:
            # CREA DIRECTORY E NORMALIZZA PERCORSO DEL FILE
            percorso_completo: Path = PERCORSO_PROGETTO / nome_file
            percorso_completo.parent.mkdir(parents=True, exist_ok=True)

            # CREA ROTATING FILE HANDLER
            file_handler: RotatingFileHandler = RotatingFileHandler(
                filename=percorso_completo,
                mode="a",
                maxBytes=bytes_max,
                backupCount=file_backup,
                encoding="utf-8"
            )
            file_handler.setFormatter(formatter)
            log.addHandler(file_handler)

        # CREA STREAM HANDLER
        stream_handler: StreamHandler = StreamHandler()
        stream_handler.setFormatter(formatter)
        log.addHandler(stream_handler)

    return log


# CONFIGURAZIONE DEL LOGGER PRINCIPALE
logger: Logger = configura_logger(
    nome_file=PERCORSO_FILE_LOG.relative_to(PERCORSO_PROGETTO),
    bytes_max=1048576,
    file_backup=5
)
