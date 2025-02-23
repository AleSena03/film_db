import logging
from logging import Formatter, StreamHandler, INFO
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


FILE_NAME: str = "logs.log"


class Logger:
    ROOT_PATH: Path = Path(__file__).resolve().parent.parent.parent
    LOG_PATH: Path = ROOT_PATH / "logs"

    def __init__(
            self,
            file_name: Optional[str],
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
                file_path: Path = self.LOG_PATH / self.__file_name
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


logger = Logger(FILE_NAME).logger
logger.info("Logger configurato con successo.")
