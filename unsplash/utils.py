import ctypes
import os
import sys

from click import echo, style


def size_format(n_bytes):
    power = 10 ** 3
    level = 0
    units = ["B", "KB", "MB", "GB", "TB"]
    while n_bytes > power:
        n_bytes /= power
        level += 1
    return "%.2f %s" % (n_bytes, units[level])


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


def pretty_dict(d, indent=0, indent_size=2, key_fg="blue", value_fg="green"):
    for key, value in d.items():
        if isinstance(value, dict):
            echo(" " * (indent + indent_size) + style("%s: " % key, fg=key_fg, bold=True))
            pretty_dict(value, indent + indent_size)
        else:
            key_txt = style("%s:" % key, fg=key_fg, bold=True)
            val_txt = style("%s" % value, fg=value_fg)
            echo(" " * (indent + indent_size) + "%s %s" % (key_txt, val_txt))
