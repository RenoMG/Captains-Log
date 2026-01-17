from astropy.time import Time
from datetime import date
import inquirer, os

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
    log_directory = "memory/logs"
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