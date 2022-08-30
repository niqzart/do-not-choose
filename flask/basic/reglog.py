from __future__ import annotations

from flask import Blueprint, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from common import db, User
from utils import argument_parser

controller = Blueprint("reglog", __name__, url_prefix="/")


def home_response(user: User):
    return {"message": "Success", "id": user.id}


def authorized_response(user: User):
    response = jsonify(home_response(user))
    set_access_cookies(response, create_access_token(identity=user.id))
    return response


@controller.route("/sign-up/", methods=("POST",))
@argument_parser("username", "password", require_all=True, strings_only=True)
def sign_up(username: str, password: str):
    if db.find_user_by_username(username) is not None:
        return {"message": "Username already taken"}

    user: User = db.create_user(username, password)
    return authorized_response(user)


@controller.route("/sign-in/", methods=("POST",))
@argument_parser("username", "password", require_all=True, strings_only=True)
def sign_in(username: str, password: str):
    user: User = db.find_user_by_username(username)
    if user is None:
        return {"message": "User does not exist"}

    if not db.verify_hash(password, user.password):
        return {"message": "Wrong password"}

    return authorized_response(user)


@controller.route("/sing-out/", methods=("POST",))
@jwt_required()
def sign_out():
    db.block_token(get_jwt()["jti"])
    response = jsonify(message="Success")
    unset_jwt_cookies(response)
    return response


@controller.route("/home/", methods=("GET",))
@jwt_required()
def home():
    return home_response(db.find_user(get_jwt_identity()))
