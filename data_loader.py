import json
from pathlib import Path

STORAGE_LOCATION = "storage/"

# Load config location with pathlib for multi-os compatibility
p = Path(STORAGE_LOCATION)
config_file = "config.json"

# This is only used for after first_boot operations.
try:
    with open(p / config_file, "r") as f:
        config_data = json.load(f)
except Exception as e:
    print(f"Oops! I cannot load my system config! ERROR:{e}")