import ctypes
import os
import sys

import requests

from . import api
from .settings import config


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


def set_desktop_windows(image_path):
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 0)


def set_desktop_linux(image_path):
    os.system(
        "/usr/bin/gsettings set org.gnome.desktop.background picture-uri "
        + "file://%s" % image_path
    )


def set_wallpaper(image_path):
    platform = sys.platform
    if platform == "win32":
        set_desktop_windows(image_path)
    elif platform == "linux":
        set_desktop_linux(image_path)
    else:
        raise RuntimeError(
            "Unable to set wallpaper for platform %s. Try setting manually: %s"
            % (platform, image_path)
        )
