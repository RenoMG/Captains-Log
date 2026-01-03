from astropy.time import Time
from datetime import date
import time, inquirer

def convert_date_to_julian():
    normal_date = date.today()
    return str(Time(str(normal_date)).jd)

class computer_logic():
    def __init__(self, name, seconds, saving_state):
        self.name = name
        self.seconds = seconds
        self.saving_state = saving_state

    def computer_reply(self, computer_msg):
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

def general_question():
    yes_or_no = [
        inquirer.Confirm("choice", message="Y for Yes / N for No."),
    ]

    choice = inquirer.prompt(yes_or_no)
    return choice