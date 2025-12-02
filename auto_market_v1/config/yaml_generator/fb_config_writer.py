import json
import os

def save_fb_form_data(form_data):
    config_data = {
        "state": form_data.get("state", "CA"),
        "price_min": int(form_data.get("price_min", 0)),
        "price_max": int(form_data.get("price_max", 999999)),
    }

    config_folder = os.path.join(os.path.dirname(__file__), "..", "..", "facebook_config")
    os.makedirs(config_folder, exist_ok=True)

    config_path = os.path.join(config_folder, "facebook_form_config.json")

    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=2)
