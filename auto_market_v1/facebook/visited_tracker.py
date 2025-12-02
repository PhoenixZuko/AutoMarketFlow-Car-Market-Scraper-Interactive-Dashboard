import os
import csv
from datetime import datetime

class VisitedTracker:
    def __init__(self, txt_path="logs/visited_urls.txt", csv_path="logs/visited_urls.csv"):
        self.txt_path = txt_path
        self.csv_path = csv_path
        self.visited = set()
        self._ensure_directories()
        self._load_txt()

    def _ensure_directories(self):
        # Creează folderul pentru .txt și .csv dacă nu există
        os.makedirs(os.path.dirname(self.txt_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

    def _load_txt(self):
        if os.path.exists(self.txt_path):
            with open(self.txt_path, "r", encoding="utf-8") as f:
                self.visited = set(line.strip() for line in f if line.strip())

    def has_visited(self, url):
        return url in self.visited

    def mark_visited(self, url, filename=None):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not self.has_visited(url):
            # Salvează în .txt
            with open(self.txt_path, "a", encoding="utf-8") as f:
                f.write(url + "\n")
            self.visited.add(url)
            print(f"[📝] URL save in {self.txt_path}: {url}")

            # Salvează și în .csv dacă avem filename
            if filename:
                write_header = not os.path.exists(self.csv_path)
                with open(self.csv_path, "a", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    if write_header:
                        writer.writerow(["url", "data_salvare", "filename"])
                    writer.writerow([url, now, filename])
                print(f"[📄] Details save in {self.csv_path}: {filename}")
        else:
            print(f"[⏭️] URL deja vizitat: {url}")
