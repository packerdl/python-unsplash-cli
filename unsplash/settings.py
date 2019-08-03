import json
import os

import click
from .utils import pretty_dict

CONFIG_DIR = click.get_app_dir("unsplash-cli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
DEFAULT_DIRECTORY = os.path.expanduser(os.path.join("~", "Pictures", "Unsplash"))

# Default configuration parameters
config = {
    "directory": DEFAULT_DIRECTORY,
    "redirect_uri": "http://localhost:8015",
    "access_key": "",
    "secret_key": "",
    "aliases": {
        "editorial": "317099",
        "wallpapers": "1065976",
    },
}


@click.group()
def settings():
    pass


@settings.command(name="set")
@click.argument("key", type=click.STRING)
@click.argument("value", type=click.STRING)
def cmd_set(key, value):
    set(key, value)


@settings.command()
def show():
    click.echo("")
    pretty_dict(config)


def _save():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    with open(CONFIG_PATH, "w") as fid:
        json.dump(config, fid, indent=2, sort_keys=True)


def _load():
    global config
    if not os.path.isfile(CONFIG_PATH) or os.path.getsize(CONFIG_PATH) == 0:
        _save()
    else:
        with open(CONFIG_PATH, "r") as fid:
            config_file = json.load(fid)
            config.update(config_file)
    return config


def set(key, value):
    global config
    config[key] = value
    _save()


def _clear(*keys):
    global config
    for key in keys:
        config.pop(key, None)
    _save()


def _reload():
    return _load()


_load()
