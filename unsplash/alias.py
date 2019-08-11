import click
from halo import Halo

from . import settings
from .utils import pretty_dict


@click.group()
def alias():
    """Manage collection aliases.

    The Unsplash API requires collections to be specified by their
    numeric ID. For convenience, aliases can be used as a substitute
    wherever collection IDs are required.
    """
    pass


@alias.command()
@click.argument("alias")
@click.argument("value")
def add(alias, value):
    """Create a new alias.

    Define ALIAS as reference to collection with identifier VALUE.
    """
    spinner = Halo(text="Adding alias...", spinner="dots").start()
    try:
        _add(alias, value)
        spinner.succeed("Added alias %s" % alias)
    except ValueError as e:
        spinner.fail(text=str(e))


@alias.command()
@click.argument("alias")
def remove(alias):
    """Remove an alias.

    Removes definition of ALIAS. It will no longer resolve to its given value.
    """
    spinner = Halo(text="Removing alias...", spinner="dots").start()
    try:
        _remove(alias)
        spinner.succeed("Removed alias %s" % alias)
    except ValueError as e:
        spinner.fail(text=str(e))


@alias.command(name="list")
def show():
    """Display defined aliases."""
    aliases = settings.config["aliases"]
    click.echo("")
    pretty_dict(aliases)


def _add(alias, value):
    if exists(alias):
        raise ValueError("Alias already exists")
    aliases = settings.config["aliases"]
    aliases[alias] = value
    settings.set("aliases", aliases)


def _remove(alias):
    if not exists(alias):
        raise ValueError("Alias not found")
    aliases = settings.config["aliases"]
    aliases.pop(alias, None)
    settings.set("aliases", aliases)


def resolve(input):
    input = input.split(",")
    aliases = settings.config["aliases"]
    for (idx, item) in enumerate(input):
        value = aliases.get(item, None)
        if value:
            input[idx] = value
    return ",".join(input)


def exists(alias):
    aliases = settings.config["aliases"]
    if alias in aliases:
        return True
