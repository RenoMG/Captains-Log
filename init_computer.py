from functions import convert_date_to_julian, computer_logic, init_question, general_question, editor_question
import json, sys, os

def first_start():
    computer = computer_logic()
    computer.reply("Welcome Captain! Looks like this is your first time here!")
    computer.name = input("What should I call you? - ")

    if computer.name == "":
        computer.reply("Hmmm... I did not get a name. You must be from the tippy top and need to keep things... as they used to say 'Down Low'.")
        computer.reply("Since you did not give me a name, I will call you 'Captain'!")
        computer.name = "Captain"

    computer.reply(f"Ahhh.... {computer.name}!")
    computer.reply(f"Nice to meet you, {computer.name}!")
    computer.reply(f"Well, {computer.name}! As you may have noticed... I am not as fast as the other systems you may have interacted with...")
    computer.reply(f"I am a prototype of the computer that is on Captain Archer's Ship, the Enterprise NX-01!")
    computer.reply(f"And, well... All I can do is store Captain logs... yeah. BUT! WAIT! DON'T GO!")
    computer.reply(f"Writing Captain logs is FUNNNnnn... are you still here?")

    still_here = general_question()
    if still_here["choice"]:
        computer.reply(f"HAHAHA, YES! I mean uhhh... glad to see you're still here {computer.name}")
    else:
        computer.reply(f"Awwww man... another one bites the dust... ;(")
        computer.seconds = 1
        sys.exit()

    computer.reply(f"Ok! Well, enough for introductions. Let's go to the home screen!")
    computer.reply("Let me save your file and get this thing going! I will make a template log for you at 'memory/logs/Heyyyooo'")
    computer.reply("OH! One more thing, what editor do you want to use?")
    get_editor = editor_question()
    computer.editor = get_editor["editor"]
    computer.reply(f"Ahh, {computer.editor}... nice!")
    computer.saving_state = True
    computer.reply("Please remember to not edit the Julian date and title position in the raw files, will make sorting annoying!")
    computer.saving_state = False
    computer.reply("OK! Are you ready to get this thing going?")
    go_home = init_question()
    if go_home['Yes']:
        computer.reply("OK! Let's go!")
    else:
        computer.reply("Faking Vulcan message signature")
        computer.reply("Calling Romulans(ANGRY VULCANS)")
        computer.reply("Got reply, telling Romulans(ANGRY VULCANS) that Vulcans are better.")
        computer.reply("Telling Romulans(ANGRY VULCANS) that Vulcans are plotting to take over the galaxy.")
        computer.reply("Got reply... I think I just started a war...")

    try: 
        memories_directory = "memory/"
        logs_directory = "memory/logs/"
        os.mkdir(memories_directory)
        os.mkdir(logs_directory)
        memories = {"name": f"{computer.name}",
                "custom_motd": "None",
                "editor": f"{computer.editor.lower()}"}

        with open("memory/memories.json", "w") as f:
            json.dump(memories, f, indent=4)

        get_date_conversion = convert_date_to_julian()
        with open("memory/logs/Heyyyooo.txt", "w") as f:
            f.write(f"Julian Date: {get_date_conversion} \n")
            f.write("Title: Heyyyooo\n\n")
            f.write("Start of Captains Log:\n")
            f.write("On a far.. far away world... a computer from the Enterprise NX-01! Wait... OH YEAH THIS IS A DEMO LOG. Sorry, uhh so uhh yeah...\n\n")
            f.write("Logs are stored like this in text files, and the Julian date and name of the log are stored at the top.\n")
            f.write("My creator made this dinky little program while learning backend development, starting with PYTHON! I hope you find some joy in this!")

    except Exception as e:
        print(f"Uh oh.. something went wrong... I was not able to create the startup files fully! ERROR: {e}")

    from menu import menu
    menu()