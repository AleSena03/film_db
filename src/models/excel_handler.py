from pathlib import Path
from time import time


from watchdog.events import FileSystemEventHandler, DirModifiedEvent, FileModifiedEvent

from src.services.excel_to_csv import excel_to_csv
from src.utils.logger import logger
from src.utils.path import EXCEL_FILE_PATH, POLL_INTERVAL


class ExcelHandler(FileSystemEventHandler):

    def __init__(self):
        self.last_trigger = 0
        super().__init__()

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        logger.debug(f"Evento ricevuto: {type(event)} - {event.src_path}")

        if not isinstance(event, FileModifiedEvent):
            return

        current_time = time()
        elapsed = current_time - self.last_trigger
        if elapsed < POLL_INTERVAL:
            logger.debug(f"Debounce attivo: {elapsed:.2f}s")
            return



        event_path = str(Path(event.src_path).resolve()).lower()
        if event_path == str(EXCEL_FILE_PATH.resolve()).lower():
            logger.info("File Excel modificato")
            logger.debug(f"Evento ricevuto: {event}")
            self.last_trigger = current_time
            excel_to_csv()

        else:
            logger.debug(f"Ignorato evento per: {event_path}")
