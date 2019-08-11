import click
from halo import Halo

from . import api


@click.command()
@click.argument("id")
def like(id):
    """Like a photo.

    Likes photo with identifier ID.
    """
    spinner = Halo(text="Liking photo...", spinner="dots").start()
    try:
        api.like(id)
        spinner.succeed("Liked")
    except Exception:
        spinner.fail("Failed to like photo.")


@click.command()
@click.argument("id")
def unlike(id):
    """Unlike a photo.

    Removes like from photo with identifier ID.
    """
    spinner = Halo(text="Unliking photo...", spinner="dots").start()
    try:
        api.unlike(id)
        spinner.succeed("Unliked")
    except Exception:
        spinner.fail("Failed to unlike photo.")
