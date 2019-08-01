import os

from click import confirm, echo, group, style
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


@directory.command()
def clean():
    with Halo(text="Checking directory...", spinner="dots"):
        info = stats()
    spinner = Halo(text="Cleaning directory...", spinner="dots")
    confirmed = confirm(
        "\nThis will %s downloaded images. Continue?" % style("DELETE ALL", bold=True)
    )
    echo("")
    if confirmed:
        spinner.start()
        for img in info["images"]:
            os.remove(os.path.join(info["path"], img))
        spinner.succeed(
            "Directory cleaned. Removed %d images (%s)."
            % (len(info["images"]), size_format(info["size"]))
        )
    else:
        spinner.fail("Aborted. No files were deleted.")


def stats():
    directory = config["directory"]
    images = [x for x in os.listdir(directory) if ".jpg" in x]
    usage = sum(
        os.path.getsize(x) for x in [os.path.join(directory, img) for img in images]
    )
    return {"images": images, "path": directory, "size": usage}
