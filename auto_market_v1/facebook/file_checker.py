# file_checker.py
import os
import csv

def is_file_in_database(filename, csv_path="logs/visited_urls.csv"):
    if not os.path.exists(csv_path):
        return False

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("filename") == filename:
                return True
    return False
