from first_boot import init_computer
import os

def main():
    if os.path.exists("memory/memories.json") == False:
        init_computer()

    if os.path.exists("memory/memories.json") == True:
        from menu import menu_init
        menu_init()

main()