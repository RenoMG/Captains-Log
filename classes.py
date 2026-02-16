import time

class computer_logic():
    def __init__(self):
        self.name = "Captain"
        self.seconds = 1.5
        self.saving_state = False
        self.typing_speed = 0.1
        self.logs_location = "storage/logs/"
        self.custom_MOTD = False
        self.MOTD_text = None

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