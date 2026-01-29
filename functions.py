from astropy.time import Time
from datetime import date
import inquirer, os, json

def convert_date_to_julian():
    normal_date = date.today()
    return str(Time(str(normal_date)).jd)

# First boot only functions
def init_bonus_question():
    yes_or_no = [
        inquirer.Confirm("Yes", message="Y for home screen / N for Romulans(ANGRY VULCANS) attack"),
    ]

    choice = inquirer.prompt(yes_or_no)
    return choice

# General functions used in multiple places
def editor_question():
    editor_choice = [
        inquirer.List(
            "editor",
            message="Choose what editor you want to use!",
            choices=["Nano", "Vim", "Neovim", "Gedit", "Kate", "Notepad"],
        )
    ]

    choice = inquirer.prompt(editor_choice)
    return choice

def yes_or_no_question():
    yes_or_no = [
        inquirer.Confirm("choice", message="Y for Yes / N for No."),
    ]

    choice = inquirer.prompt(yes_or_no)
    return choice

def menu_choice():
    menu_choice = [
        inquirer.List(
            "menu",
            message="Please choose an option!",
            choices=["Create Log", "Edit Log", "List logs", "Log Stats", "Edit settings", "About", "Quit"],
        )
    ]

    choice = inquirer.prompt(menu_choice)
    return choice

def edit_log_choice():
    with open("storage/config.json", "r") as f:
        data = json.load(f)
    log_directory = data["logs_location"]
    log_files = [file for file in os.listdir(log_directory)]

    log_choice = [
        inquirer.List(
            "logs",
            message="Please choose a log!",
            choices=log_files,
        )
    ]

    choice = inquirer.prompt(log_choice)
    return choice

def name_question():
    questions = [
        inquirer.Text(name="name", message="What is your name?"),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer

def create_log_question():
    def log_name_validation(answer, current):
        if len(current) == 0:
            return False
        else:
            return True

    questions = [
        inquirer.Text(name="log_name", message="Type a name for your log!", validate=log_name_validation),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer


def init_logs_location_question():
    def logs_location_validation(answer, current):
        if len(current) == 0:
            return True
        elif os.path.isdir(f"{current}") == True:
            return True
        else:
            return False

    questions = [
        inquirer.Text(name="logs_location", message="Where to save your logs?", validate=logs_location_validation),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer

def MOTD_question():
    questions = [
        inquirer.Text(name="MOTD", message="What would you like the MOTD to be?"),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer


# Settings questions
# Some questions need to be modified and changed to be only used in this specific portion 
def settings_page():
    setting_choice = [
        inquirer.List(
            "setting",
            message="Please choose a value to change!",
            choices=["Name", "Editor", "Logs Location", "Custom MOTD"],
        )
    ]

    choice = inquirer.prompt(setting_choice)
    return choice

def name_change():
    questions = [
        inquirer.Text(name="name", message="What would you like to change your name to?"),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer
    
def change_MOTD_question():
    questions = [
        inquirer.Text(name="MOTD", message="What would you like the MOTD to be changed to?"),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer