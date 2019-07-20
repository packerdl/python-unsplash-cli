import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

import click
from requests import HTTPError

import _thread

from . import api, settings
from .settings import config

AUTH = "https://unsplash.com/oauth/authorize"
SCOPES = "public+read_photos+read_collections"


class OAuthServer(HTTPServer):
    def __init__(self, *args):
        super().__init__(*args)
        self.auth_success = False


class RequestHandler(BaseHTTPRequestHandler):
    def _page_path(self, page):
        pkg_folder = os.path.dirname(os.path.abspath(api.__file__))
        return os.path.join(pkg_folder, "pages", page)

    def _serve_page(self, page, status):
        page_path = self._page_path(page)
        with open(page_path, "rb") as fid:
            self.send_response(status)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(fid.read())

    def log_message(self, *args, **kwargs):
        pass

    def do_GET(self):
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in qs:
            # Use authorization code to acquire token
            try:
                response = api.token(qs["code"], config["redirect_uri"])
            except HTTPError:
                # Token was not returned
                self._serve_page("failure.html", 400)
                return
            settings.set("authorization", response)
            self._serve_page("success.html", 200)
            self.server.auth_success = True
        else:
            # Authorization code was not present.
            self._serve_page("failure.html", 400)
        _thread.start_new_thread(self.server.shutdown, ())


def login():
    auth_url = "%s?client_id=%s&redirect_uri=%s&response_type=code&scope=%s" % (
        AUTH,
        config["access_key"],
        urllib.parse.quote(config["redirect_uri"]),
        SCOPES,
    )
    click.launch(auth_url)
    parse = urllib.parse.urlparse(config["redirect_uri"])
    server = OAuthServer((parse.hostname, parse.port), RequestHandler)
    server.serve_forever()
    if server.auth_success:
        print("Authorization Success")
    else:
        print("Authorization Failed")
