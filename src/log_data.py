import os
from datetime import datetime


class DataLogger:
    def __init__(self):
        """
        Erstellt automatisch einen /logs/ Ordner auf Projektebene
        und eine CSV-Datei mit schön formatierten Einträgen.
        """
        # Projekt-Hauptverzeichnis bestimmen (eine Ebene über src)
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.log_dir = os.path.join(self.project_root, "logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # Dateiname mit Zeitstempel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(self.log_dir, f"detections_{timestamp}.csv")

        # CSV-Header schreiben (mit Leerzeichen nach Kommas)
        with open(self.log_path, mode="w", newline="", encoding="utf-8") as file:
            file.write("timestamp, color, shape\n")

        print(f"[Logger] Started logging to {self.log_path}")

    def log(self, shape, color):
        """Schreibt eine Zeile mit Zeitstempel, Farbe und Form."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, mode="a", newline="", encoding="utf-8") as file:
            file.write(f"{timestamp}, {color}, {shape}\n")
