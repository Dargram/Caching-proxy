import json

def load_config(filepath="config.json"):
    with open(filepath, mode="r") as f:
        data = json.load(f)
    return data

config = load_config()
