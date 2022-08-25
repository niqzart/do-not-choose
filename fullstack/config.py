from sys import modules
from traceback import format_tb

from flask import request
from werkzeug.exceptions import NotFound

from __lib__.flask_fullstack import Flask
from __lib__.flask_fullstack.sqlalchemy import create_base, Sessionmaker, Session
from common import db_meta, engine

Base = create_base(db_meta)
sessionmaker = Sessionmaker(bind=engine, class_=Session)

app: Flask = Flask(__name__)
app.config["TESTING"] = "pytest" in modules.keys()
app.secrets_from_env("hope it's local")
# app.configure_cors()
app.config["RESTX_INCLUDE_ALL_MODELS"] = True


@app.errorhandler(NotFound)
def on_not_found(_):
    return app.return_error(404, "Not Found")


@app.errorhandler(Exception)
def on_any_exception(error: Exception):
    error_text: str = (
            f"Requested URL: {request.path}\n"
            + "".join(format_tb(error.__traceback__))
            + f"Error: {repr(error)}"
    )
    print(error_text)
    return app.return_error(500, error_text if app.debug else "Error occurred, check the logs")
