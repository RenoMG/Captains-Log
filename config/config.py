import json
from pathlib import Path

STORAGE_LOCATION = "storage/"
DEFAULT_MOTD_LOCATION = ""
LOGS_DB = "logs.db"

# Load config location with pathlib for multi-os compatibility
p = Path(STORAGE_LOCATION)
config_file = "config.json"

m = Path(DEFAULT_MOTD_LOCATION)
motd_file = "motd.json"

# This is used to load data from json into memory for Class assignment
def load_data():
    try:
        with open(p / config_file, "r") as f:
            config_data = json.load(f)
            return config_data
    except Exception as e:
        print(f"Oops! I cannot load my system config! ERROR:{e}")

# Load default MOTDs from JSON
with open(m / motd_file, "r") as f:
    motd = json.load(f)

# Write data to config
def config_json_write(config_data):
    with open(p / config_file, "w") as f:
        json.dump(config_data, f, indent=4)

# Make dir on first boot
def first_boot_dir(logs_location):
    logs = Path(logs_location)

    if p.exists() == False:
        p.mkdir()
    if logs.exists() == False:
        logs.mkdir()