import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.models.excel_handler import ExcelHandler
from src.utils.logger import logger
from src.utils.path import EXCEL_FILE_PATH


class Watcher:
    """Monitora eventuali modifiche del file Excel."""

    def __init__(self):
        self.observer = Observer(timeout=5)

    def start(self):
        logger.info("Monitoraggio modifiche...")

        event_handler: FileSystemEventHandler = ExcelHandler()
        self.observer.schedule(
            event_handler=event_handler,
            path=str(EXCEL_FILE_PATH.parent),
            recursive=False
        )

        self.observer.start()

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()
        logger.info("Monitoraggio terminato")
