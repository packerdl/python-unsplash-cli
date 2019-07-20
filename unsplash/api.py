import requests

from .settings import config

BASE_URL = "https://api.unsplash.com"
OAUTH = "https://unsplash.com/oauth/token"
PHOTO = BASE_URL + "/photos"
RANDOM = BASE_URL + "/photos/random"


def auth_header():
    try:
        token = config["authorization"]["access_token"]
        return {"Authorization": "Bearer %s" % token}
    except KeyError:
        return {"Authorization": "Client-ID %s" % config["access_key"]}


def token(code, redirect_uri):
    data = {
        "client_id": config["access_key"],
        "client_secret": config["secret_key"],
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    r = requests.post(OAUTH, data=data)
    r.raise_for_status()
    return r.json()


def photo(id):
    r = requests.get(PHOTO, headers=auth_header())
    r.raise_for_status()
    return r.json()


def random(params={}):
    r = requests.get(RANDOM, headers=auth_header(), params=params)
    r.raise_for_status()
    return r.json()


def download_location(id):
    r = requests.get("%s/photos/%s/download" % (BASE_URL, id), headers=auth_header())
    r.raise_for_status()
