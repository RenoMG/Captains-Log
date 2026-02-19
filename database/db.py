import sqlite3
from config.config import load_data, LOGS_DB
from pathlib import Path
from contextlib import closing

def reload_data():
    global config_data, l
    config_data = load_data()
    l = Path(config_data["logs_location"])

reload_data()

def database_conn_helper():
    return sqlite3.connect(l / LOGS_DB)

def list_log_names():
    with closing(database_conn_helper()) as db_file:
        db_file.row_factory = sqlite3.Row
        cursor = db_file.cursor()

        cursor.execute("""SELECT title FROM logs""")

        titles = []

        for title in cursor:
            titles.append(title[0])

        return titles

def list_all_log_data():
    with closing(database_conn_helper()) as db_file:
        cursor = db_file.cursor()
        cursor.execute("""SELECT title, date, body FROM logs""")
        get_all = cursor.fetchall()

    return get_all

def edit_log(title, body):
    with closing(database_conn_helper()) as db_file:
        try:
            with db_file:
                cursor = db_file.cursor()

                cursor.execute("""UPDATE logs SET body=? WHERE title=?""", (body, title))
        except Exception as e:
            print(f"Uh oh.. something went wrong... I was not able to edit the log! ERROR: {e}")

def edit_log_title(title_old, title_new):
    with closing(database_conn_helper()) as db_file:
        try:
            with db_file:
                cursor = db_file.cursor()

                cursor.execute("""UPDATE logs SET title=? WHERE title=?""", (title_new, title_old))
        except Exception as e:
            print(f"Uh oh.. something went wrong... I was not able to edit the log! ERROR: {e}")

def create_log(title, get_date_conversion):
    for log_title in list_log_names():
        if title == log_title:
            if title.endswith("Copy") != True and title[-3].endswith("-") != True:
                title += " Copy"
            elif title.endswith("Copy"):
                title += " - 1"
            elif title[-1].isdigit():
                num = int(title[-1]) + 1
                title = title[:-1] + f"{num}"

    with closing(database_conn_helper()) as db_file:
        try:
            with db_file:
                    cursor = db_file.cursor()

                    date = get_date_conversion
                    body = ""

                    cursor.execute(
                        """INSERT INTO logs(title, date, body) VALUES (?, ?, ?)""",
                        (title, date, body),
                    )
        except Exception as e:
            print(f"I can't create the log! {e}")

def delete_log(title):
    with closing(database_conn_helper()) as db_file:
        try:
            with db_file:
                cursor = db_file.cursor()

                cursor.execute("""DELETE FROM logs WHERE title=?""", (title,))
        except Exception as e:
            print(f"Uh oh.. something went wrong... I was not able to edit the log! ERROR: {e}")
     

# Functions for moving storage location if DB not exist
def create_new_db(get_date_conversion, content):
    reload_data()
    if Path(l / LOGS_DB).exists():
       raise FileExistsError

    with closing(database_conn_helper()) as db_file:
        try:
            with db_file:
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
                    body = content

                    cursor.execute(
                        """INSERT INTO logs(title, date, body) VALUES (?, ?, ?)""",
                        (title, date, body),
                    )
        except Exception as e:
            print(f"{e}")
