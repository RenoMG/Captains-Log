import os
from data_processor import p
from first_boot import init_computer

def main():
    if p.exists() == False:
        init_computer()

    if p.exists():
        from main_ui import run_main
        os.system("clear")
        run_main()

main()