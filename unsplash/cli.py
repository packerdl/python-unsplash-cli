import click
from halo import Halo

from . import api, oauth, utils, settings as cfg


@click.group()
def entry():
    pass


@entry.command()
def login():
    oauth.login()


@entry.command()
def logout():
    with Halo(text="Logging out...", spinner="dots") as spinner:
        cfg.clear("user", "authorization")
        spinner.succeed("Logged out of Unsplash")


@entry.group()
def settings():
    pass


@settings.command()
@click.argument("key", type=click.STRING)
@click.argument("value", type=click.STRING)
def set(key, value):
    cfg.set(key, value)


@settings.command()
def show():
    cfg.show()


@entry.command()
@click.option(
    "--orientation",
    type=click.Choice(["landscape", "portrait", "squarish"]),
    default="landscape",
    help="Only return images of given orientation",
    show_default=True,
)
@click.option(
    "--featured",
    is_flag=True,
    default=False,
    help="Only return featured images",
    show_default=True,
)
@click.option("-q", "--query", help="Only return images matching term")
def random(**kwargs):
    """Download a random image"""
    image = api.random(kwargs)
    utils.download(image["id"], image["urls"]["full"])
