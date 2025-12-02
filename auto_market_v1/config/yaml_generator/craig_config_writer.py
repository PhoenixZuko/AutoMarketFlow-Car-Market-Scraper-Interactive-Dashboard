import json
from pathlib import Path

def save_craig_form_data(data, json_path=None):
    if json_path is None:
        json_path = Path(__file__).parent / "data" / "craig_form_data.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
