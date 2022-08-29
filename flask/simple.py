from __future__ import annotations

from flask import Blueprint, request

from utils import argument_parser

controller = Blueprint("simple", __name__, url_prefix="/simple/")


@controller.route("/", methods=("GET", "POST"))
@argument_parser("error")
def simple(error: bool | str | None):
    if request.method == "GET":
        return {"message": "Hello World"}

    if error is True or isinstance(error, str) and error.lower() == "true":
        raise ValueError("User requested an error")
    elif not error or isinstance(error, str) and error.lower() == "false":
        return {"message": "I'm fine"}, 201
    return {"message": "Parameter error is not boolean"}, 400
