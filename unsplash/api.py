import os

import requests


BASE_URL = "https://api.unsplash.com"
RANDOM = BASE_URL + "/photos/random"
ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


if not ACCESS_KEY:
    raise LookupError("Environment variable UNSPLASH_ACCESS_KEY not set")

PUBLIC_AUTH = {"Authorization": "Client-ID %s" % ACCESS_KEY}


def random(params={}):
    r = requests.get(RANDOM, headers=PUBLIC_AUTH, params=params)
    r.raise_for_status()
    return r.json()


def download_location(id):
    r = requests.get("%s/photos/%s/download" % (BASE_URL, id), headers=PUBLIC_AUTH)
    r.raise_for_status()
