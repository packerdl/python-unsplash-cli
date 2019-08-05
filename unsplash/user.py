import click
from halo import Halo

from . import api
from .settings import config
from .utils import pretty_dict


@click.group()
def user():
    pass


@user.command()
def me():
    spinner = Halo(text="Fetching current user's information...", spinner="dots").start()
    if "authorization" not in config:
        spinner.warn("Not logged into Unsplash. Please log in first.")
        return
    try:
        user = api.me()
        spinner.succeed("Information for user @%s:" % user["username"])
        click.echo("")
        pretty_dict(user)
    except Exception:
        spinner.fail("Unable to fetch user information.")


@user.command()
@click.argument("username")
def get(username):
    spinner = Halo(text="Fetching @%s's user information..." % username, spinner="dots").start()
    try:
        user = api.get_user(username)
        spinner.succeed("Information for user @%s:" % username)
        click.echo("")
        pretty_dict(user)
    except Exception:
        spinner.fail("Unable to fetch user information.")
