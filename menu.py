from functions import computer_logic, init_question, general_question, editor_question
import json, sys, os

def menu_init():
    with open("memory/memories.json", "r") as f:
        data = json.load(f)

    computer = computer_logic(data["name"], 2, False, data["editor"])
    