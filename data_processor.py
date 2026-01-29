import json
from pathlib import Path

STORAGE_LOCATION = "storage/"

# Load config location with pathlib for multi-os compatibility
p = Path(STORAGE_LOCATION)
config_file = "config.json"

# This is used to load data from json into memory for Class assignment
try:
    if p.exists() != False:   

        with open(p / config_file, "r") as f:
            config_data = json.load(f)
except Exception as e:
    print(f"Oops! I cannot load my system config! ERROR:{e}")

# Load default MOTDs
with open("motd.json", "r") as f:
    motd = json.load(f)

# Write data to config
def config_json_write(config_data):
    with open(p / config_file, "w") as f:
        json.dump(config_data, f, indent=4)