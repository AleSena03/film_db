import logging
from logging import Formatter, StreamHandler, INFO
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from src.utils.config import LOG_DIR_PATH, LOG_FILE_NAME


class Logger:
    """
    Rappresenta un logger avanzato che utilizza RotatingFileHandler e StreamHandler

    Attributes
    ----------
    self.__file_name : Optional[str] = None
        Il nome del file di log.
    self.__max_bytes : int = 1048576 (1 MB)
        La dimensione massima (in byte) che i file di log possono raggiungere prima della rotazione.
    self.__backup_files : int = 5
        Il numero massimo dei file di log di backup che possono essere mantenuti.

    """

    def __init__(
            self,
            file_name: Optional[str] = None,
            max_bytes: int = 1048576,
            backup_files: int = 5
    ) -> None:
        self.__file_name = file_name
        self.__max_bytes = max_bytes
        self.__backup_files = backup_files
        self.__logger = self.__set_logger()

    @property
    def logger(self):
        return self.__logger

    def __set_logger(self):
        log = logging.getLogger(__name__)
        log.setLevel(INFO)

        if not log.handlers:
            formatter: Formatter = Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "%Y-%m-%d %H:%M:%S"
            )

            if self.__file_name:
                file_path: Path = LOG_DIR_PATH / self.__file_name
                file_path.parent.mkdir(parents=True, exist_ok=True)

                file_handler: RotatingFileHandler = RotatingFileHandler(
                    filename=file_path,
                    mode="a",
                    maxBytes=self.__max_bytes,
                    backupCount=self.__backup_files,
                    encoding="utf-8"
                )
                file_handler.setFormatter(formatter)
                log.addHandler(file_handler)

            stream_handler: StreamHandler = StreamHandler()
            stream_handler.setFormatter(formatter)
            log.addHandler(stream_handler)

        return log


logger = Logger(LOG_FILE_NAME).logger
