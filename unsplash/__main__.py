from .alias import alias
from .auth import login, logout
from .collection import collection
from .directory import directory
from .entry import entry
from .settings import settings

entry.add_command(alias)
entry.add_command(collection)
entry.add_command(directory)
entry.add_command(login)
entry.add_command(logout)
entry.add_command(settings)

entry()
