from functions import computer_logic, general_question, editor_question, menu_choice
import json, sys, os, random

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
    menu_choice()
    


