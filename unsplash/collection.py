import click
from halo import Halo

from . import api
from .alias import resolve


@click.group()
def collection():
    pass


@collection.command()
@click.option("--private", is_flag=True, default=False, show_default=True)
@click.argument("title")
@click.argument("description", nargs=-1)
def create(title, description, private):
    spinner = Halo(text="Creating collection...", spinner="dots").start()
    try:
        if description:
            description = " ".join(description)
        api.create_collection(title, description, private)
        spinner.succeed("Collection created")
    except Exception:
        spinner.fail("Failed to create collection")


@collection.command()
@click.argument("collection")
def delete(collection):
    spinner = Halo(text="Deleting collection...", spinner="dots")
    confirmed = click.confirm(
        "\nThis will %s your collection. Continue?"
        % click.style("permanently delete", bold=True)
    )
    click.echo("")
    if confirmed:
        try:
            spinner.start()
            collection_id = resolve(collection)
            api.delete_collection(collection_id)
            spinner.succeed("Collection deleted")
        except Exception:
            spinner.fail("Failed to delete collection")
    else:
        spinner.fail("Aborted. Collection was not deleted.")


@collection.command()
@click.argument("photo")
@click.argument("collection")
def add(photo, collection):
    spinner = Halo(text="Adding photo to collection...", spinner="dots").start()
    try:
        collection_id = resolve(collection)
        api.add_to_collection(collection_id, photo)
        spinner.succeed("Photo added to collection")
    except Exception:
        spinner.fail("Failed to add photo")


@collection.command()
@click.argument("photo")
@click.argument("collection")
def remove(photo, collection):
    spinner = Halo(text="Removing photo from collection...", spinner="dots").start()
    try:
        collection_id = resolve(collection)
        api.remove_from_collection(collection_id, photo)
        spinner.succeed("Photo removed from collection")
    except Exception:
        spinner.fail("Failed to add photo")
