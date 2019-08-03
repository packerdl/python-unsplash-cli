import os

import click
import requests
from halo import Halo

from . import alias, api, utils
from .settings import config


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
@click.option(
    "--id",
    help="Fetch a specific photo by its ID. Overrides all other options."
)
def entry(ctx, **kwargs):
    if ctx.invoked_subcommand is None:
        spinner = Halo(text="Selecting an image...", spinner="dots").start()
        if kwargs["id"]:
            image = api.photo(kwargs["id"])
        else:
            if kwargs["orientation"] == "any":
                kwargs.pop("orientation", None)
            if kwargs["collections"]:
                kwargs["collections"] = alias.resolve(kwargs["collections"])
            image = api.random(kwargs)
        spinner.text = "Downloading image..."
        image_path = download(image["id"], image["urls"]["full"])
        utils.set_wallpaper(image_path)
        spinner.succeed(
            "Photo by %s (@%s)" % (image["user"]["name"], image["user"]["username"])
        )
        pretty_print_info(image)


def download(image_id, image_url=None):
    if not os.path.isdir(config["directory"]):
        os.makedirs(config["directory"], exist_ok=True)
    if not image_url:
        image = api.photo(image_id)
        image_url = image["urls"]["full"]
    api.download_location(image_id)
    file_path = os.path.join(config["directory"], "%s.jpg" % image_id)
    with requests.get(image_url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as fid:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    fid.write(chunk)
    return file_path


def pretty_print_info(photo):
    print("")
    if photo["description"]:
        click.secho(photo["description"], dim=True)
    if photo["alt_description"]:
        click.secho(photo["alt_description"], dim=True)
    if not photo["description"] and not photo["alt_description"]:
        click.secho("No description provided", dim=True)
    print("")
    click.secho("Downloads ", bold=True, nl=False)
    click.echo("%d / " % photo["downloads"], nl=False)
    click.secho("Views ", bold=True, nl=False)
    click.echo("%d / " % photo["views"], nl=False)
    click.secho("Likes ", bold=True, nl=False)
    click.echo(photo["likes"])
    click.secho(photo["id"], dim=True)
