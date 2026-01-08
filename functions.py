from astropy.time import Time
from datetime import date
import time, inquirer, os

def convert_date_to_julian():
    normal_date = date.today()
    return str(Time(str(normal_date)).jd)

class computer_logic():
    def __init__(self, name, seconds, saving_state, editor):
        self.name = name
        self.seconds = seconds
        self.saving_state = saving_state
        self.editor = editor
        self.thinking_output = True

    def computer_reply(self, computer_msg):
        if self.thinking_output == False:
            return print(computer_msg)

        if self.saving_state:
            time.sleep(self.seconds)
            print("Computer is saving data...")
            time.sleep(self.seconds)
            print(computer_msg)
        else:
            print("Computer is thinking...")
            time.sleep(self.seconds)
            print(computer_msg)
            time.sleep(self.seconds)

def init_question():
    yes_or_no = [
        inquirer.Confirm("Yes", message="Y for home screen / N for Romulans(ANGRY VULCANS) attack"),
    ]

    choice = inquirer.prompt(yes_or_no)
    return choice

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

def general_question():
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