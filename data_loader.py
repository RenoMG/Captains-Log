import json

# This is only used for after first_boot operations.
try:
    with open("storage/config.json", "r") as f:
        config_data = json.load(f)
except Exception as e:
    print(f"Oops! I cannot load my system config! ERROR:{e}")