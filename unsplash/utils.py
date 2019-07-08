import os

import requests

from . import api

HOME = os.getenv("HOME", "./")
DOWNLOAD_LOCATION = os.path.join(HOME, "Pictures", "Unsplash")


def download(image_id, image_url=None):
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION, exist_ok=True)
    file_path = os.path.join(DOWNLOAD_LOCATION, "%s.jpg" % image_id)
    api.download_location(image_id)
    with requests.get(image_url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as fid:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    fid.write(chunk)
    return file_path
