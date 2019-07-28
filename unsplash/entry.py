import click
from halo import Halo

from . import alias, api, utils


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
            kwargs["collections"] = alias.resolve(kwargs["collections"])
        image = api.random(kwargs)
        spinner.text = "Downloading image..."
        image_path = utils.download(image["id"], image["urls"]["full"])
        utils.set_wallpaper(image_path)
        spinner.succeed(
            "Photo by %s (@%s)" % (image["user"]["name"], image["user"]["username"])
        )
        utils.pretty_print_info(image)
