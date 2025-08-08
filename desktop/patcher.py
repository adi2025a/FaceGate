import os
import json
import shutil
from pathlib import Path

# Constants
LOCAL_DESKTOP_DIR = Path.home() / ".local/share/applications"
SYSTEM_DESKTOP_DIR = Path("/usr/share/applications")
CONFIG_PATH = Path(__file__).parent.parent / "data" / "apps_config.json"
LAUNCHER_PATH = Path(__file__).parent.parent / "launcher.py"

def load_app_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

def save_app_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def patch_app(app_name, exec_name):
    """
    Patches the .desktop launcher for the given app (e.g., google-chrome)
    """

    original_desktop = SYSTEM_DESKTOP_DIR / f"{app_name}.desktop"
    if not original_desktop.exists():
        print(f"Desktop file for {app_name} not found.")
        return False

    # Load original content
    with open(original_desktop, "r") as f:
        lines = f.readlines()

    # Backup original exec command
    original_exec = None
    new_lines = []
    for line in lines:
        if line.startswith("Exec="):
            original_exec = line.strip()
            # Replace Exec with facegate launcher
            new_exec = f"Exec=python3 {LAUNCHER_PATH} {exec_name} %U\n"
            new_lines.append(new_exec)
        else:
            new_lines.append(line)

    if not original_exec:
        print("No Exec line found in .desktop file.")
        return False

    # Write patched file to user's local applications dir
    LOCAL_DESKTOP_DIR.mkdir(parents=True, exist_ok=True)
    patched_path = LOCAL_DESKTOP_DIR / f"{app_name}.desktop"

    with open(patched_path, "w") as f:
        f.writelines(new_lines)

    # Save patch status to config
    config = load_app_config()
    config[app_name] = {
        "exec": exec_name,
        "original_exec": original_exec,
        "patched": True
    }
    save_app_config(config)

    print(f"Patched launcher saved to {patched_path}")
    return True

def unpatch_app(app_name):
    """
    Reverts the patched launcher for the given app
    """
    patched_path = LOCAL_DESKTOP_DIR / f"{app_name}.desktop"
    config = load_app_config()

    if not patched_path.exists():
        print("No patched launcher to remove.")
        return False

    if app_name in config:
        del config[app_name]
        save_app_config(config)

    patched_path.unlink()
    print(f"Unpatched and removed {patched_path}")
    return True

def is_patched(app_name):
    config = load_app_config()
    return config.get(app_name, {}).get("patched", False)
