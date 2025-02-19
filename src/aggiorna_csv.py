import os
import time
import pandas as pd
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

file_excel = r"D:\Documents\Progetti\FilmDB\FilmDB.xlsm"
file_csv = r"D:\Documents\Progetti\FilmDB\film.csv"

class AggiornaCSV(FileSystemEventHandler):
    
    def on_modified(self, event):
        
        print("File Excel modificato")
        if event.src_path.endswith(file_excel):
            self.aggiorna_csv()

    def aggiorna_csv(self):
        
        df = pd.read_excel(file_excel, sheet_name = "Film")
        df = df[["titolo",
                 "titolo_originale",
                 "anno",
                 "durata",
                 "regia",
                 "lingua_originale",
                 "saga",
                 "id_prequel",
                 "id_sequel",
                 "poster",
                 "budget",
                 "incasso_primo_weekend_usa",
                 "incasso_usa",
                 "incasso_globale",
                 "valutazione_imdb"]]
        df.to_csv(file_csv, index = False)
        print("File CSV aggiornato con successo!")


if __name__ == "__main__":
    gestione_evento = AggiornaCSV()
    osservatore = Observer()
    osservatore.schedule(gestione_evento, path = os.path.dirname(file_excel), recursive = False)
    osservatore.start()
    
    print("Monitoraggio file Excel per aggiornamenti...")
    try:
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        osservatore.stop()
    osservatore.join()