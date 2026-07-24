from pathlib import Path
import json
from model_browser import ModelBrowserWindow

# Get config path
def get_config_dir(app_name="BlaBlaText"):
    home = Path.home()

    config_dir = home / f".{app_name.lower()}"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

# Path of config
CONFIG_FILE = get_config_dir() / "config.json"

def save_settings(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_settings():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {} # Default setting, if the file is missing

