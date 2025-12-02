# facebook/search_loader.py

import yaml

def load_facebook_search_tasks(config_path="config/facebook.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        return config.get("search_tasks", [])
