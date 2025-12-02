import os
import yaml
from craigslist.scraper import run_scraper

def load_config():
    config_path = os.path.join("config", "craigslist.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    # Save the current process ID to a file
    with open("craiglist_pid.txt", "w") as f:
        f.write(str(os.getpid()))

    # Load the configuration and start the scraper
    config = load_config()
    run_scraper(config)
