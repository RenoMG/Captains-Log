from functions import convert_date_to_julian, computer_logic, general_question, editor_question, menu_choice, edit_log_choice
import json, sys, os, random, subprocess

#Load Captain memories
with open("memory/memories.json", "r") as f:
    data = json.load(f)

    computer = computer_logic(data["name"], 2, False, data["editor"])

#Load MOTD
with open("motd.json", "r") as f:
    motd = json.load(f)

def menu_init():
    computer.computer_reply(f"Hello {computer.name}! It's nice to see you again!")
    computer.computer_reply(f"Let me load the menu and get everything going!")
    os.system("clear")
    menu()

def menu():
    computer.thinking_output = False
    get_motd = motd[random.randrange(3)]
    motd_name = computer.name
    computer.computer_reply("MOTD: " + get_motd.format(captain_name=motd_name))
    get_choice = menu_choice()
    computer.thinking_output = True

    if get_choice["menu"] == "Create Log":
        title = input("What should the title be? - ")
        try: 
            if os.path.exists(f"memory/logs/{title}.txt") == True:
                computer.computer_reply("A log with that name already exists, opening it now!")

            get_date_conversion = convert_date_to_julian()
            with open(f"memory/logs/{title}.txt", "w") as f:
                f.write(f"Julian Date: {get_date_conversion} \n")
                f.write(f"Title: {title}\n\n")

        except Exception as e:
            print(f"Uh oh.. something went wrong... I was not able to create the log! ERROR: {e}")

        computer.computer_reply(f"The log has been created, {computer.name}! Time to get typing!")
        
        process = subprocess.Popen([computer.editor, f"memory/logs/{title}.txt"])
        process.wait()
        os.system("clear")
        menu()

    if get_choice["menu"] == "Edit Log":
        computer.computer_reply(f"Ok, here is all of the logs you have. Please select one to edit!")
        log_to_edit = edit_log_choice()
        computer.computer_reply(f"Ok, opening {log_to_edit["logs"]}")

        process = subprocess.Popen([computer.editor, f"memory/logs/{log_to_edit["logs"]}"])
        process.wait()
        os.system("clear")
        menu()

    if get_choice["menu"] == "Quit":
        computer.computer_reply(f"Awhhhh mannnn... ok {computer.name}! See you next time!")
        quit()


    


