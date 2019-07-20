import json
import os

import click

CONFIG_DIR = click.get_app_dir("unsplash-cli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
DEFAULT_DIRECTORY = os.path.expanduser(os.path.join("~", "Pictures", "Unsplash"))

# Default configuration parameters
config = {
    "directory": DEFAULT_DIRECTORY,
    "redirect_uri": "http://localhost:8015",
    "access_key": "",
    "secret_key": "",
}


def save():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    with open(CONFIG_PATH, "w") as fid:
        json.dump(config, fid, indent=2, sort_keys=True)


def load():
    global config
    if not os.path.isfile(CONFIG_PATH) or os.path.getsize(CONFIG_PATH) == 0:
        save()
    else:
        with open(CONFIG_PATH, "r") as fid:
            config_file = json.load(fid)
            config.update(config_file)


def set(key, value):
    global config
    config[key] = value
    save()


def clear(*keys):
    global config
    for key in keys:
        config.pop(key, None)
    save()


def show():
    print(config)


load()
