import json
from pathlib import Path
import sqlite3

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

# Load default MOTDs
with open(m / motd_file, "r") as f:
    motd = json.load(f)

# Write data to config
def config_json_write(config_data):
    with open(p / config_file, "w") as f:
        json.dump(config_data, f, indent=4)

# Make dir on first boot
def first_boot_dir(logs_location):
    Path.mkdir(STORAGE_LOCATION)
    Path.mkdir(logs_location)

# Create database and insert example log
def first_boot_db(contents, logs_location, get_date_conversion):

    logs = Path(logs_location)

    # Create database on first boot
    db_file = sqlite3.connect(logs / LOGS_DB)
    cursor = db_file.cursor()

    title = "Heyyyooo.txt"
    date = get_date_conversion
    body = contents

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS logs(
                        title TEXT unique,
                        date REAL,
                        body TEXT'
        )"""
    )

    cursor.execute(
        """INSERT INTO logs(title, date, body) VALUES (?, ?, ?)""",
        (title, date, body),
    )

    db_file.commit()