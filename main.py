import os
from data_processor import p
from first_boot import init_computer

def main():
    if p.exists() == False:
        init_computer()

    if p.exists():
        from menu import menu_init
        os.system("clear")
        menu_init()

main()