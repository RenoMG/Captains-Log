import json, editor
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

# Log manipulation operations

def list_log_names():
    config_data = load_data()

    l = Path(config_data["logs_location"])

    db_file = sqlite3.connect(l / LOGS_DB)
    db_file.row_factory = sqlite3.Row
    cursor = db_file.cursor()

    cursor.execute("""SELECT title FROM logs""")

    titles = []

    for title in cursor:
        titles.append(title[0])

    return titles

def list_all_log_data():
    config_data = load_data()

    l = Path(config_data["logs_location"])

    db_file = sqlite3.connect(l / LOGS_DB)
    cursor = db_file.cursor()

    cursor.execute("""SELECT title, date, body FROM logs""")
    get_all = cursor.fetchall()

    return get_all

def edit_log(title):
    try:
        config_data = load_data()

        l = Path(config_data["logs_location"])

        db_file = sqlite3.connect(l / LOGS_DB)
        cursor = db_file.cursor()

        cursor.execute("""SELECT title, date, body FROM logs WHERE title=?""", (title,))

        fetch_body = cursor.fetchone()[2]
        
        capture_edit = editor.editor(text=fetch_body)

        cursor.execute("""UPDATE logs SET body=? WHERE title=?""", (capture_edit, title))
        db_file.commit()
    except Exception as e:
        print(f"Uh oh.. something went wrong... I was not able to edit the log! ERROR: {e}")
        input()

def create_log(title, get_date_conversion):

    for log_title in list_log_names():
        if title == log_title:
            print("ERROR: Log entry with that title already present!")
            input()
            return

    config_data = load_data()
    l = Path(config_data["logs_location"])

    # Create db connection
    db_file = sqlite3.connect(l / LOGS_DB)
    cursor = db_file.cursor()

    date = get_date_conversion
    body = None

    cursor.execute(
        """INSERT INTO logs(title, date, body) VALUES (?, ?, ?)""",
        (title, date, body),
    )

    db_file.commit()

    edit_log(title)
     

# First boot data operations

# Make dir on first boot
def first_boot_dir(logs_location):
    logs = Path(logs_location)

    if p.exists() == False:
        Path.mkdir(STORAGE_LOCATION)
    if logs.exists() == False:
        Path.mkdir(logs_location)

# Create database and insert example log
def first_boot_db(contents, logs_location, get_date_conversion):

    logs = Path(logs_location)

    # Create database on first boot
    db_file = sqlite3.connect(logs / LOGS_DB)
    cursor = db_file.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS logs(
                        title TEXT unique,
                        date REAL,
                        body TEXT
        )"""
    )

    title = "Heyyyooo"
    date = get_date_conversion
    body = contents

    cursor.execute(
        """INSERT INTO logs(title, date, body) VALUES (?, ?, ?)""",
        (title, date, body),
    )

    db_file.commit()