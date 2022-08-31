from __future__ import annotations

from wsgiref.simple_server import make_server

from falcon import App

from simple import SimpleResource
from utils import XHeaderMiddleware

app = App(middleware=[
    XHeaderMiddleware()
])

app.add_route("/simple/", SimpleResource())

if __name__ == "__main__":
    httpd = make_server("", 6000, app)
    print("Flying Falcon")
    httpd.serve_forever()
