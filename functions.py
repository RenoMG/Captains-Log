import inquirer
from astropy.time import Time
from datetime import date
from data_processor import *
from pathlib import Path
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt

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
def yes_or_no_question():
    yes_or_no = [
        inquirer.Confirm("choice", message="Y for Yes / N for No."),
    ]

    choice = inquirer.prompt(yes_or_no)
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
        p = Path(current)
        if len(current) == 0:
            return True
        elif p.is_dir():
            return True
        else:
            return False

    questions = [
        inquirer.Text(name="logs_location", message="Where to save your logs?", validate=logs_location_validation),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer

class change_logs_location_question(Validator):
    def validate(self, document):
        text = document.text.strip()
        p = Path(text)
        if len(text) == 0:
            raise ValidationError(
                message="Please enter a value!"
            )
        if p.is_dir() == False:
            raise ValidationError(
                message="Path does not exist!"
            )

def MOTD_question():
    questions = [
        inquirer.Text(name="MOTD", message="What would you like the MOTD to be?"),
    ]

    answer = inquirer.prompt(questions)
    print("\n")
    return answer