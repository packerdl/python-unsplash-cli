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


@user.command()
@click.option("--username", help="Desired screen name")
@click.option("--first-name", help="Your first name")
@click.option("--last-name", help="Your last name")
@click.option("--email", help="Account email address")
@click.option("--url", help="Portfolio or personal webpage URL")
@click.option("--location", help="Your location")
@click.option("--bio", help="Personal description")
@click.option("--instagram-username", help="Associated Instagram account")
def update(**kwargs):
    spinner = Halo(text="Updating user information...", spinner="dots").start()
    if not any(kwargs.values()):
        spinner.warn("No values to update were supplied.")
        return
    try:
        api.update_user(kwargs)
        spinner.succeed("Account successfully updated.")
    except Exception:
        spinner.fail("Unable to update account information.")
