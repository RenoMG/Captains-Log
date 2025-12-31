from functions import thinking, saving
import json, sys, os

def first_start():
    print("Welcome Captain! Looks like this is your first time here!")
    name = input("What should I call you? - ")

    if name == "":
        thinking(2)
        print("Hmmm... I did not get a name. You must be from the tippy top and need to keep things... as they used to say 'Down Low'.")
        thinking(2)
        print("Since you did not give me a name, I will call you 'Captain'!")
        name = "Captain"

    thinking(3)
    print(f"Ahhh.... {name}!")
    thinking(3)
    print(f"Nice to meet you, {name}!")
    thinking(3)
    print(f"Well, {name}! As you may have noticed... I am not as fast as the other systems you may have interacted with...")
    thinking(3)
    print(f"I am a prototype of the computer that is on Captain Archer's Ship, the Enterprise NX-01!")
    thinking(3)
    print(f"And, well... All I can do is store Captain logs... yeah. BUT! WAIT! DON'T GO!")
    thinking(3)
    user_present = input(f"Writing Captain logs is FUNNNnnn... are you still here? - ")

    if len(user_present) > 0:
        thinking(2)
        print(f"HAHAHA, YES! I mean uhhh... glad to see you're still here {name}")

    if user_present == "":
        thinking(2)
        print(f"Awwww man... another one bites the dust... ;(")
        thinking(1)
        sys.exit()

    print(f"Ok! Well, enough for introductions. Let's go to the home screen!")
    thinking(2)
    print("Let me save your file and get this thing going!")
    saving(2)

    memories_directory = "memory/"
    os.mkdir(memories_directory)
    memories = {"name": name,
            "custom_motd": None,}
    
    with open("memory/memories.json", "w") as f:
        json.dump(memories, f, indent=4)

    return True