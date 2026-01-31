import os, random, subprocess, webbrowser
from functions import *
from classes import computer_logic
from data_processor import *

# Setup Instance Variables for the menu
config_data = load_data()
computer = computer_logic()
computer.name = config_data["name"]
computer.custom_MOTD = config_data["custom_MOTD_enabled"]
computer.MOTD_text = config_data["custom_motd"]
computer.editor = config_data["editor"]
computer.logs_location = config_data["logs_location"]

def menu_init():
    computer.reply(f"Hello {computer.name}! It's nice to see you again!")
    computer.computer_loading_animation()
    os.system("clear")
    menu()

def menu():
    while True:
        os.system("clear")

        # Use custom MOTD if enabled
        if computer.custom_MOTD == False:
            get_motd = motd[random.randrange(len(motd))]
        else: 
            get_motd = computer.MOTD_text


        motd_name = computer.name
        computer.reply("MOTD: " + get_motd.format(captain_name=motd_name))
        get_choice = menu_choice()

        if get_choice["menu"] == "Create Log":
            os.system("clear")
            title = create_log_question()
            try: 
                if os.path.exists(f"{computer.logs_location}{title['log_name']}.txt") == True:
                    computer.reply("A log with that name already exists, opening it now!")

                get_date_conversion = convert_date_to_julian()
                with open(f"{computer.logs_location}{title['log_name']}.txt", "w") as f:
                    f.write(f"Julian Date: {get_date_conversion} \n")
                    f.write(f"Title: {title['log_name']}\n\n")

            except Exception as e:
                print(f"Uh oh.. something went wrong... I was not able to create the log! ERROR: {e}")

            computer.reply(f"The log has been created, {computer.name}! Time to get typing!")
            
            process = subprocess.Popen([computer.editor, f"{computer.logs_location}{title['log_name']}.txt"])
            process.wait()
            os.system("clear")

        if get_choice["menu"] == "Edit Log":
            os.system("clear")
            computer.reply(f"Ok, here is all of the logs you have. Please select one to edit!")
            log_to_edit = edit_log_choice()
            computer.reply(f"Ok, opening {log_to_edit['logs']}")
                
            edit_log(log_to_edit["logs"])

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
                    julian_date = f.readline().removeprefix("Julian Date: ").strip(" \n")

                with open(f"{computer.logs_location}{file}") as f: 
                    title_name = f.readlines()[1].removeprefix("Title: ").strip(" \n")

                print(f"-- \nFile Name: {file},\nTitle: {title_name},\nCreation Date: {julian_date}")
                
            input("--\nPress Enter to close.")

        if get_choice["menu"] == "Log Stats":
            os.system("clear")
            file_list = [file for file in os.listdir(computer.logs_location)]
            
            the_uses = []
            romulan_uses = []
            period_uses = []

            for file in file_list:
                with open(f"{computer.logs_location}{file}", "r") as f: 
                    text = f.read().lower().split(" ")

                for word in text:
                    if "the" in word:
                        the_uses.append(word)

                    if "romulan" in word or "romulans" in word:
                        romulan_uses.append(word)

                    for ch in word:
                        if "." in ch:
                                period_uses.append(ch)

            computer.reply("Here are the stats for your log files!")
            print(f"-- \nTotal Logs: {len(file_list)}")
            print(f"\nTotal Uses of the word 'The': {len(the_uses)}")
            print(f"\nTotal Uses of the word 'Romulan'(They scare me): {len(romulan_uses)}")
            print(f"\nTotal Periods: {len(period_uses)}")
                
            input("--\nPress Enter to close.")

        if get_choice["menu"] == "About":
            os.system("clear")
            computer.reply(f"Welcome to the about page!")
            computer.reply(f"This program was made by Reno! A beginner programmer!")
            computer.reply(f"I love watching Star Trek and thought this would be fun to make at my skill level!")
            computer.reply(f"Would you like to visit my website?")

            visit_website = yes_or_no_question()
            if visit_website["choice"]:
                try: 
                    webbrowser.open("https://renos.world", new=0, autoraise=True)
                except Exception as e:
                    input(f"Error: {e}, are you using a headless setup like WSL? Press enter to return to the menu.")
            else:
                computer.reply(input(f"Ah... ok... Well! Press any key to return to the menu!"))

            os.system("clear")

        if get_choice["menu"] == "Edit settings":
            os.system("clear")
            computer.computer_loading_animation()
            computer.reply(f"Here are all the available settings!")
            setting_choice = settings_page()

            if setting_choice["setting"] == "Name":
                computer.reply(f"Current Name Value: {computer.name}")
                new_name = name_change()
                if new_name["name"] == "":
                    computer.reply("Ok! Back to the default name it is, Captain!")
                    config_data["name"] = "Captain"
                    config_json_write(config_data)
                    computer.computer_saving_animation()
                else:
                    computer.name = new_name["name"]
                    computer.reply(f"Ok! Your name has been change to {computer.name}!")
                    config_data["name"] = computer.name
                    config_json_write(config_data)
                    computer.computer_saving_animation()
                computer.reply("Returning to the menu")
                os.system("clear")

            if setting_choice["setting"] == "Editor":
                computer.reply(f"Current Editor Value: {computer.editor}")
                new_editor = editor_question()
                computer.reply(f"Ok! Editor has now been changed to {new_editor['editor']}!")
                if new_editor["editor"] == "Neovim":
                    computer.editor = "nvim"
                else:
                    computer.editor = new_editor["editor"].lower()
                config_data["editor"] = computer.editor
                config_json_write(config_data)
                computer.computer_saving_animation()
                os.system("clear")

            if setting_choice["setting"] == "Logs Location":
                computer.reply(f"Current Logs Location: {computer.logs_location}")
                computer.reply("Please remember, when you change the logs location you will have to move all your current logs to the new location!")
                new_logs_location = init_logs_location_question()
                if new_logs_location["logs_location"] == "":
                    computer.logs_location = "storage/logs/"
                    computer.reply(f"Ok, the default path will be used! File Path: '{computer.logs_location}'.")
                    config_data["logs_location"] = computer.logs_location
                    config_json_write(config_data)
                    computer.computer_saving_animation()
                else:
                    if new_logs_location["logs_location"].endswith('/'):
                        computer.logs_location = new_logs_location["logs_location"]
                        computer.reply(f"Ok, {computer.logs_location} sounds good!")
                        config_data["logs_location"] = computer.logs_location
                        config_json_write(config_data)                   
                        computer.computer_saving_animation()
                    else:
                        computer.logs_location = new_logs_location["logs_location"] + "/"
                        computer.reply(f"Ok, {computer.logs_location} sounds good!")
                        config_data["logs_location"] = computer.logs_location
                        config_json_write(config_data)   
                        computer.computer_saving_animation()          
                os.system("clear")

            if setting_choice["setting"] == "Custom MOTD":
                computer.reply(f"Current MOTD Values: Custom Enabled: {computer.custom_MOTD}, MOTD Text: {computer.MOTD_text}")
                computer.reply("Use {captain_name} to place name in MOTD!")
                new_custom_MOTD = change_MOTD_question()
                if new_custom_MOTD["MOTD"] == "":
                    computer.reply("No value was given, default MOTD it is!")
                    computer.custom_MOTD = False
                    computer.MOTD_text = None
                    config_data["custom_MOTD_enabled"] = computer.custom_MOTD
                    config_data["custom_motd"] = computer.MOTD_text
                    config_json_write(config_data)
                    computer.computer_saving_animation()
                else:
                    computer.reply(f"Custom MOTD has been set to {new_custom_MOTD['MOTD']}")
                    computer.custom_MOTD = True
                    computer.MOTD_text = new_custom_MOTD["MOTD"]
                    config_data["custom_MOTD_enabled"] = computer.custom_MOTD
                    config_data["custom_motd"] = computer.MOTD_text
                    config_json_write(config_data)
                    computer.computer_saving_animation()
                os.system("clear")

