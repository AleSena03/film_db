from pathlib import Path
from threading import Lock
from time import time

from watchdog.events import FileSystemEventHandler, FileModifiedEvent

from src.services.to_csv import to_csv
from src.utils.logger import logger
from src.utils.path import EXCEL_FILE_PATH, POLL_INTERVAL


class ExcelHandler(FileSystemEventHandler):
    """Gestisce le modifiche avvenute sul file Excel."""

    def __init__(self):
        self.last_trigger: int = 0
        self.lock: Lock = Lock()
        super().__init__()

    def on_modified(self, event: FileModifiedEvent) -> None:
        try:
            with (self.lock):
                if (time() - self.last_trigger) < POLL_INTERVAL:
                    return

                event_path: Path = Path(event.src_path).resolve()
                if not event_path.exists() or event_path.is_dir():
                    return

                if event_path != EXCEL_FILE_PATH:
                    return

                if event_path.stat().st_mtime <= self.last_trigger:
                    return

                logger.info("File Excel modificato")
                to_csv()
                self.last_trigger = time()

        except OSError as err:
            logger.error(f"Errore di accesso al file {event} - {err}", exc_info=True)
        except Exception as err:
            logger.error(f"Errore generico durante l'elaborazione - {err}", exc_info=True)
