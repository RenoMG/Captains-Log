from init_computer import first_start
from menu import menu_init
import os

def main():
    if os.path.exists("memory/memories.json") == False:
        first_start()

    if os.path.exists("memory/memories.json") == True:
        menu_init()

main()