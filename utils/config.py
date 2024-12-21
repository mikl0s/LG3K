
import json
import os

def load_config(config_file):
    if not os.path.exists(config_file):
        print(f"Config file {config_file} not found. Creating a default one.")
        config = {
            "services": ["web_server"],
            "total_logs": 1000,
            "split_size": 100,
            "max_threads": 4
        }
        with open(config_file, "w") as file:
            json.dump(config, file, indent=4)
        return config
    with open(config_file, "r") as file:
        return json.load(file)
