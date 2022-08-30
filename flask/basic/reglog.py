from __future__ import annotations

from flask import Blueprint

from common import db
from common.interface import User
from utils import argument_parser

controller = Blueprint("reglog", __name__, url_prefix="/")


@controller.route("/sign-up/", methods=("POST",))
@argument_parser("username", "password", require_all=True, strings_only=True)
def sign_up(username: str, password: str):
    if db.find_user_by_username(username) is not None:
        return {"message": "Username already taken"}

    user: User = db.create_user(username, password)
    return {"message": "Success", "id": user.id}


@controller.route("/sign-in/", methods=("POST",))
@argument_parser("username", "password", require_all=True, strings_only=True)
def sign_in(username: str, password: str):
    user: User = db.find_user_by_username(username)
    if user is None:
        return {"message": "User does not exist"}

    if not db.verify_hash(password, user.password):
        return {"message": "Wrong password"}

    return {"message": "Success"}
