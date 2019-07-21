import click
from halo import Halo

from . import aliases, api, oauth, utils, settings as cfg


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--orientation",
    type=click.Choice(["any", "landscape", "portrait", "squarish"]),
    help="Only return images of given orientation",
    default="any",
    show_default=True,
)
@click.option(
    "--featured",
    is_flag=True,
    default=False,
    help="Only return featured images",
    show_default=True,
)
@click.option("--query", help="Only return images matching term")
@click.option(
    "--collections",
    help="Only return images from given collections. "
    + "Specify multiple collections with commas.",
)
def entry(ctx, **kwargs):
    if ctx.invoked_subcommand is None:
        spinner = Halo(text="Selecting an image...", spinner="dots").start()
        if kwargs["orientation"] == "any":
            kwargs.pop("orientation", None)
        if kwargs["collections"]:
            kwargs["collections"] = aliases.resolve(kwargs["collections"])
        image = api.random(kwargs)
        spinner.text = "Downloading image..."
        image_path = utils.download(image["id"], image["urls"]["full"])
        utils.set_wallpaper(image_path)
        spinner.succeed(
            "Photo by %s (@%s)" % (image["user"]["name"], image["user"]["username"])
        )
        utils.pretty_print_info(image)


@entry.command()
def login():
    oauth.login()


@entry.command()
def logout():
    with Halo(text="Logging out...", spinner="dots") as spinner:
        cfg.clear("authorization")
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


@entry.group()
def alias():
    pass


@alias.command()
@click.argument("alias")
@click.argument("value")
def add(alias, value):
    spinner = Halo(text="Adding alias...", spinner="dots").start()
    try:
        aliases.add(alias, value)
        spinner.succeed("Added alias %s" % alias)
    except ValueError as e:
        spinner.fail(text=str(e))


@alias.command()
@click.argument("alias")
def remove(alias):
    spinner = Halo(text="Removing alias...", spinner="dots").start()
    try:
        aliases.remove(alias)
        spinner.succeed("Removed alias %s" % alias)
    except ValueError as e:
        spinner.fail(text=str(e))


@alias.command(name="list")
def alias_show():
    aliases.show()
