import click

from . import api, utils, settings as cfg


@click.group()
def entry():
    pass


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
