import json

with open("config.json", "r") as f:
    config = json.load(f)
    config = json.dumps(config, indent=4)

print("\033[31m", config, "\033[0m")
