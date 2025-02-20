"""Modulo che configura un sistema avanzato di logging."""
import logging
from logging import Logger, Formatter, StreamHandler, INFO
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def config_logger(
        file_log: Optional[str] = None,
        bytes_max: int = 1048576,
        files_backup: int = 5
) -> Logger:
    """
    Configura un logger avanzato con RotatingFileHandler e StreamHandler.

    Parameters
    ----------
    file_log : Optional[str] = None
        Nome del file di log.
    bytes_max : int = 1048576 (1 MB)
        Dimensione massima del file di log prima della rotazione.
    files_backup : int = 5
        Numero di file backup da mantenere.

    Returns
    -------
    Logger
        Logger configurato per output su file e stream.
    """
    log: Logger = logging.getLogger(__name__)
    log.setLevel(INFO)

    # EVITA AGGIUNTA DI HANDLER GIA PRESENTI
    if not log.handlers:
        formatter: Formatter = Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        if file_log:
            # CREA DIRECTORY PER IL FILE DI LOG
            path_root: Path = Path(__file__).resolve().parent.parent.parent
            path_log: Path = path_root / "logs"/ file_log
            path_log.parent.mkdir(parents=True, exist_ok=True)

            # CREA ROTATING FILE HANDLER
            file_handler: RotatingFileHandler = RotatingFileHandler(
                filename=path_log,
                mode="a",
                maxBytes=bytes_max,
                backupCount=files_backup,
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
logger: Logger = config_logger(
    file_log="importa_log.log"
)
