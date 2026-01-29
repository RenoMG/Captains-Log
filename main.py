from pathlib import Path
from first_boot import init_computer

# Check config location with pathlib for multi-os compatibility
p = Path("storage/")

def main():
    if p.exists() == False:
        init_computer()

    if p.exists():
        from menu import menu_init
        menu_init()

main()