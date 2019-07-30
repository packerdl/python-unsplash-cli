import os

from click import echo, group, style
from halo import Halo

from .settings import config
from .utils import size_format


@group()
def directory():
    pass


@directory.command()
def info():
    with Halo(text="Checking local folder...", spinner="dots"):
        info = stats()
    echo("\n" + style("Directory: ", bold=True) + "%s" % info["path"])
    echo(style("Number of Images: ", bold=True) + "%d" % len(info["images"]))
    echo(style("Space Usage: ", bold=True) + size_format(info["size"]))


def stats():
    directory = config["directory"]
    images = [x for x in os.listdir(directory) if ".jpg" in x]
    usage = sum(os.path.getsize(x) for x in [os.path.join(directory, img) for img in images])
    return {
        "images": images,
        "path": directory,
        "size": usage,
    }
