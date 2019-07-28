import os

from click import echo, group, style

from .settings import config
from .utils import size_format


@group()
def directory():
    pass


@directory.command()
def info():
    directory = config["directory"]
    images = [x for x in os.listdir(directory) if ".jpg" in x]
    usage = sum(os.path.getsize(x) for x in [os.path.join(directory, img) for img in images])
    echo("\n" + style("Directory: ", bold=True) + "%s" % directory)
    echo(style("Number of Images: ", bold=True) + "%d" % len(images))
    echo(style("Space Usage: ", bold=True) + size_format(usage))
