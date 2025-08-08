import json
import os
from desktop.patcher import patch_app

def save_app_command(command, config_path="data/apps_config.json"):
    os.makedirs("data", exist_ok=True)
    config = {"app_command": command}

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

    patch_app(command,command)

