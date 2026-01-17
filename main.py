import os
from first_boot import init_computer

def main():
    if os.path.exists("storage/config.json") == False:
        init_computer()

    if os.path.exists("storage/config.json") == True:
        from menu import menu_init
        menu_init()

main()