from os import getenv
from sys import modules
from traceback import format_tb

from flask import request, Response
from werkzeug.exceptions import NotFound

from __lib__.flask_fullstack import Flask
from common.relational import configure_sqlalchemy, build_sqlalchemy_database

db_url = getenv("DB_LINK", "sqlite:///app.db")
db_meta, Base, sessionmaker = configure_sqlalchemy(db_url)
db = build_sqlalchemy_database(db_url, db_meta, Base, sessionmaker)

app: Flask = Flask(__name__)
app.config["TESTING"] = "pytest" in modules.keys()
app.secrets_from_env("hope it's local")
# app.configure_cors()
app.config["RESTX_INCLUDE_ALL_MODELS"] = True


@app.errorhandler(NotFound)
def on_not_found(_):
    return {"message": "Not Found"}, 404


@app.errorhandler(Exception)
def on_any_exception(error: Exception):
    error_text: str = (
            f"Requested URL: {request.path}\n"
            + "".join(format_tb(error.__traceback__))
            + f"Error: {repr(error)}"
    )
    print(error_text)
    return app.return_error(500, error_text if app.debug else "Error occurred, check the logs")


@app.after_request
def add_header(res: Response):
    res.headers.add_header("X-Framework", "flask-fullstack")
    res.headers.add_header("X-Framework-Codename", "X")
    return res
