import json, os, random, subprocess, webbrowser
from functions import *
from classes import computer_logic

# Load Computer Config Into Memory From File
try: 
    with open("storage/config.json", "r") as f:
        data = json.load(f)

        computer = computer_logic()
        computer.name = data["name"]
        computer.custom_MOTD = data["custom_MOTD_enabled"]
        computer.MOTD_text = data["custom_motd"]
        computer.editor = data["editor"]
        computer.logs_location = data["logs_location"]
except Exception as e:
    print(f"Oops! I cannot load my system config! ERROR:{e}")

# Don't load MOTD file if Custom MOTD is enabled
if computer.custom_MOTD == False:
    with open("motd.json", "r") as f:
        motd = json.load(f)

def menu_init():
    computer.reply(f"Hello {computer.name}! It's nice to see you again!")
    computer.reply(f"Let me load the menu and get everything going!")
    os.system("clear")
    menu()

def menu():
    os.system("clear")
    if computer.custom_MOTD == False:
        get_motd = motd[random.randrange(len(motd))]
    else: 
        get_motd = computer.custom_MOTD
    motd_name = computer.name
    computer.reply("MOTD: " + get_motd.format(captain_name=motd_name))
    get_choice = menu_choice()

    if get_choice["menu"] == "Create Log":
        os.system("clear")
        title = create_log_question()
        try: 
            if os.path.exists(f"{computer.logs_location}{title["log_name"]}.txt") == True:
                computer.reply("A log with that name already exists, opening it now!")

            get_date_conversion = convert_date_to_julian()
            with open(f"{computer.logs_location}{title["log_name"]}.txt", "w") as f:
                f.write(f"Julian Date: {get_date_conversion} \n")
                f.write(f"Title: {title["log_name"]}\n\n")

        except Exception as e:
            print(f"Uh oh.. something went wrong... I was not able to create the log! ERROR: {e}")

        computer.reply(f"The log has been created, {computer.name}! Time to get typing!")
        
        process = subprocess.Popen([computer.editor, f"{computer.logs_location}{title["log_name"]}.txt"])
        process.wait()
        os.system("clear")
        menu()

    if get_choice["menu"] == "Edit Log":
        os.system("clear")
        computer.reply(f"Ok, here is all of the logs you have. Please select one to edit!")
        log_to_edit = edit_log_choice()
        computer.reply(f"Ok, opening {log_to_edit["logs"]}")

        try: 
            process = subprocess.Popen([computer.editor, f"{computer.logs_location}{log_to_edit["logs"]}"])
            process.wait()
        except Exception as e:
            print(f"Uh oh.. something went wrong... I was not able to edit the log! ERROR: {e}")

        os.system("clear")
        menu()

    if get_choice["menu"] == "Quit":
        os.system("clear")
        computer.reply(f"Awhhhh mannnn... ok {computer.name}! See you next time!")
        quit()

    if get_choice["menu"] == "List logs":
        os.system("clear")
        file_list = [file for file in os.listdir(computer.logs_location)]
        print(f"Total Logs: {len(file_list)}")

        for file in file_list:
            with open(f"{computer.logs_location}{file}") as f: 
                julian_date = f.readline().strip("Julian Date: ").strip(" \n")

            with open(f"{computer.logs_location}{file}") as f: 
                title_name = f.readlines()[1].strip(" \n")

            print(f"-- \nFile Name: {file},\n{title_name},\nCreation Date: {julian_date}")
            
        input("--\nPress Enter to close.")
        menu()

    if get_choice["menu"] == "Log Stats":
        os.system("clear")
        file_list = [file for file in os.listdir(computer.logs_location)]
        
        the_uses = []
        romulan_uses = []
        period_uses = []

        for file in file_list:
            with open(f"{computer.logs_location}{file}", "r") as f: 
                text = f.read().lower().split(" ")

            with open(f"{computer.logs_location}{file}", "r") as f: 
                period_text = f.read()

            for word in text:
                if "the" in word:
                    the_uses.append(word)

                if "romulan" in word or "romulans" in word:
                    romulan_uses.append(word)

            for ch in period_text:
                if "." in ch:
                    period_uses.append(ch)

        computer.reply("Here are the stats for your log files!")
        print(f"-- \nTotal Logs: {len(file_list)}")
        print(f"\nTotal Uses of the word 'The': {len(the_uses)}")
        print(f"\nTotal Uses of the word 'Romulan'(They scare me): {len(romulan_uses)}")
        print(f"\nTotal Periods: {len(period_uses)}")
            
        input("--\nPress Enter to close.")
        menu()

    if get_choice["menu"] == "About":
        os.system("clear")
        computer.computer_reply(f"Welcome to the about page!")
        computer.computer_reply(f"This program was made by Reno! A beginner programmer!")
        computer.computer_reply(f"I love watching Star Trek and thought this would be fun to make at my skill level!")
        computer.computer_reply(f"Would you like to visit my website?")

        visit_website = about_website_question()
        if visit_website["choice"]:
            try: 
                webbrowser.open("https://renos.world", new=0, autoraise=True)
                raise RuntimeError("RuntimeError")
            except Exception as e:
                input(f"Error: {e}, are you using a headless setup like WSL? ")
        else:
            computer.computer_reply(input(f"Ah... ok... Well! Press any key to return to the menu!"))

        os.system("clear")
        menu()
    


