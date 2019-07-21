from . import settings


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


def add(alias, value):
    if exists(alias):
        raise ValueError("Alias already exists")
    aliases = settings.config["aliases"]
    aliases[alias] = value
    settings.set("aliases", aliases)


def remove(alias):
    if not exists(alias):
        raise ValueError("Alias not found")
    aliases = settings.config["aliases"]
    aliases.pop(alias, None)
    settings.set("aliases", aliases)


def show():
    print(settings.config["aliases"])
