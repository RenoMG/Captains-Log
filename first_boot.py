import json, os
from functions import *
from classes import computer_logic

def init_computer():
    computer = computer_logic()
    computer.reply("Welcome Captain! Looks like this is your first time here!")
    computer.reply("Let's begin the setup process!")
    computer.reply("I will now ask you some questions to get started! Let's start with your name")
    name_answer = name_question()
    computer.name = name_answer["name"]
    computer.saving_state = True

    if computer.name == "":
        computer.saving_state = False
        computer.reply("Hmmm... I did not get a name. You must be from the tippy top and need to keep things... as they used to say 'Down Low'.")
        computer.reply("Since you did not give me a name, I will call you 'Captain'!")
        computer.saving_state = True
        computer.name = "Captain"

    computer.reply(f"Nice to meet you, {computer.name}!")
    computer.saving_state = False

    computer.reply(f"Ok, {computer.name}. I don't have the functionality of a full text editor... I was never programmed with it.")
    computer.reply(f"I am actually a prototype of the computer that is on Captain Archer's Ship, the Enterprise NX-01!")
    computer.reply(f"And, well... All I can do is store Captain logs... yeah. BUT! WAIT! DON'T GO!")
    computer.reply(f"All you have to do is choose an external editor on your system and I can use that!")
    computer.saving_state = True
    get_editor = editor_question()
    
    if get_editor["editor"] == "Neovim":
        computer.editor = "nvim"
    else:
        computer.editor = get_editor["editor"]
    computer.reply(f"Ahh, {computer.editor}... nice!")
    computer.saving_state = False

    computer.reply(f"Ok! Now, where do you want me to save your log's, {computer.name}?")
    computer.reply(f"You can just press 'enter' on the question for the default save location.")
    computer.reply(f"Please make sure you enter the absolute path")
    computer.saving_state = True
    logs_location = init_logs_location_question()

    if logs_location["logs_location"] == "":
        computer.reply(f"Ok, the default path will be used! File Path: '{computer.logs_location}'.")
        computer.saving_state = False
    else:
        if logs_location["logs_location"].endswith('/'):
            computer.logs_location = logs_location["logs_location"]
            computer.reply(f"Ok, {computer.logs_location} sounds good!")
            computer.saving_state = False
        else:
            computer.logs_location = logs_location["logs_location"] + "/"
            computer.reply(f"Ok, {computer.logs_location} sounds good!")
            computer.saving_state = False

    computer.reply(f"Ok, lets set a custom MOTD! Again, just press 'enter' for the default MOTD.")
    MOTD = MOTD_question()
    computer.saving_state = True

    if MOTD["MOTD"] == "":
        computer.reply("Ok! Default MOTD it is!")
        computer.custom_MOTD = False
        computer.saving_state = False
    else:
        computer.MOTD_text = MOTD["MOTD"]
        computer.custom_MOTD = True
        computer.reply(f"Ok, '{computer.MOTD_text}' has been set as the MOTD!")
        computer.saving_state = False   

    computer.reply("Ok! Everything is now set!")
    computer.reply("Here is some useful information.")
    computer.reply("I save titles and dates in the top two lines of each log.")
    computer.reply("Dates are stored in the Julian time format.")
    computer.reply("All files are stored locally and no data is transmitted from this secure terminal, unless you make a system for it.")
    computer.reply("So, if you accidentally delete everything... I will literally lose my mind.")
    computer.reply("Please remember to not edit the Julian date and title position in the raw files, will make sorting annoying!")
    computer.reply(f"Ok! Well, enough for introductions. Let's go to the home screen!")

    computer.reply("OK! Are you ready to get this thing going?")
    go_home = init_bonus_question()
    if go_home['Yes']:
        computer.reply("OK! Let's go!")
    else:
        computer.reply("Faking Vulcan message signature")
        computer.reply("Calling Romulans(ANGRY VULCANS)")
        computer.reply("Got reply, telling Romulans(ANGRY VULCANS) that Vulcans are better.")
        computer.reply("Telling Romulans(ANGRY VULCANS) that Vulcans are plotting to take over the galaxy.")
        computer.reply("Got reply... I think I just started a war...")

    try: 
        os.mkdir("storage/")
        config = {"name": f"{computer.name}",
                "custom_MOTD_enabled": computer.custom_MOTD,
                "custom_motd": f"{computer.MOTD_text}",
                "editor": f"{computer.editor.lower()}",
                "logs_location": f"{computer.logs_location}"}

        with open(f"storage/config.json", "w") as f:
            json.dump(config, f, indent=4)

        os.mkdir(f"{computer.logs_location}")

        get_date_conversion = convert_date_to_julian()
        with open(f"{computer.logs_location}Heyyyooo.txt", "w") as f:
            f.write(f"Julian Date: {get_date_conversion} \n")
            f.write("Title: Heyyyooo\n\n")
            f.write("Start of Captains Log:\n")
            f.write("On a far.. far away world... a computer from the Enterprise NX-01! Wait... OH YEAH THIS IS A DEMO LOG. Sorry, uhh so uhh yeah...\n\n")
            f.write("Logs are stored like this in text files, and the Julian date and name of the log are stored at the top.\n")
            f.write("My creator made this dinky little program while learning backend development, starting with PYTHON! I hope you find some joy in this!")

    except Exception as e:
        print(f"Uh oh.. something went wrong... I was not able to create the startup files fully! ERROR: {e}")

    from menu import menu
    menu()