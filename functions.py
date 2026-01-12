from astropy.time import Time
from datetime import date
import time, inquirer, os

def convert_date_to_julian():
    normal_date = date.today()
    return str(Time(str(normal_date)).jd)

class computer_logic():
    def __init__(self):
        self.name = "Captain"
        self.seconds = 1.5
        self.saving_state = False
        self.typing_speed = 0.1
        self.editor = None
        self.file_path = "memory/"
        self.custom_MOTD = False
        self.MOTD_text = None

    def computer_loading_animation(self):
        loading_ch = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷", "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷", "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷", "⣾"]
        for ch in loading_ch:
            print(f"{ch} Loading", end="\r")
            time.sleep(0.1)

    def computer_saving_animation(self):
        saving_ch = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷", "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷", "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷", "⣾"]
        timer = 0
        for ch in saving_ch:
            if timer != 24:
                print(f"{ch} Saving Data", end="\r")
                time.sleep(0.1)
                timer += 1
            else:
                print(f"Data Saved!       ", end="\r")
                print("\n")


    def reply(self, computer_msg):
        if self.saving_state:
            time.sleep(self.seconds)
            self.computer_saving_animation()
            text_string = ""
            for letter in computer_msg:
                print(f"{text_string}{letter}", end="\r")
                text_string += letter
                time.sleep(self.typing_speed)
            print("\n")
        else:
            time.sleep(self.seconds)
            text_string = ""
            for letter in computer_msg:
                print(f"{text_string}{letter}", end="\r")
                text_string += letter
                time.sleep(self.typing_speed)
            print("\n")

def init_bonus_question():
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

def init_name_question():
    questions = [
        inquirer.Text(name="name", message="What is your name?"),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer


def init_file_path_question():
    def file_path_validation(answer, current):
        if len(current) == 0:
            return True
        elif os.path.isdir(f"{current}") == True:
            return True
        else:
            return False

    questions = [
        inquirer.Text(name="file_path", message="Where to save my files?", validate=file_path_validation),
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