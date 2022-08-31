from datetime import timedelta, datetime

from flask import Flask, Response
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt_identity,
    get_jwt,
)
from flask_jwt_extended.exceptions import JWTExtendedException

from common import db
from utils import error_response

configuration_options = {
    "JWT_TOKEN_LOCATION": ["cookies"],
    "JWT_COOKIE_CSRF_PROTECT": False,  # temp
    "JWT_COOKIE_SAMESITE": "None",  # temp
    "JWT_COOKIE_SECURE": False,  # temp
    "JWT_ACCESS_TOKEN_EXPIRES": timedelta(days=1),
    "X_JWT_AUTO_REFRESH": timedelta(hours=12),
}


def configure_jwt(app: Flask = None):
    app.config.update(configuration_options)
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def unauthorized_callback(callback: str):
        response = error_response(401, message=callback)
        unset_jwt_cookies(response)
        return response

    @jwt.expired_token_loader
    def expired_token_callback(*_):
        response = error_response(401, message="Expired token")
        unset_jwt_cookies(response)
        return response

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        response = error_response(422, message=f"Invalid token: {callback}")
        unset_jwt_cookies(response)
        return response

    @jwt.token_verification_failed_loader
    def verification_failed_callback(*_):
        response = error_response(401, message="Token verification failed")
        unset_jwt_cookies(response)
        return response

    auto_refresh = configuration_options.get("X_JWT_AUTO_REFRESH")
    if auto_refresh is not None:
        @app.after_request
        def refresh_expiring_jwt(response: Response):
            try:
                jwt_payload = get_jwt()
                target_timestamp = datetime.timestamp(datetime.utcnow() + auto_refresh)
                if target_timestamp > jwt_payload["exp"]:
                    token = create_access_token(identity=get_jwt_identity())
                    set_access_cookies(response, token)
            except (RuntimeError, JWTExtendedException):
                pass
            return response

    @jwt.token_in_blocklist_loader
    def blacklist_check(_, jwt_payload: dict) -> bool:
        return db.is_token_blocked(jwt_payload["jti"])

    return jwt
