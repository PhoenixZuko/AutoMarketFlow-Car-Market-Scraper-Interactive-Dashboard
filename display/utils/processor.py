import json
import os

def get_car_data():
    import json
    with open("data/cars_tabulator.json", "r", encoding="utf-8") as f:
        return json.load(f)

