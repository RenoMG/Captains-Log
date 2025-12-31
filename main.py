from init_computer import first_start
import os

def main():
    if os.path.exists("memory/memories.json") == False:
        first_start()

    if os.path.exists("memory/memories.json") == True:
        start()

main()