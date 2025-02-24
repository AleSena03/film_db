from src.models.watcher import Watcher


def update_csv():
    watcher = Watcher()
    watcher.start()


if __name__ == "__main__":
    update_csv()
