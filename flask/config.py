from os import getenv
from sys import modules
from traceback import format_tb

from flask import request, Response, Flask
from werkzeug.exceptions import NotFound

app: Flask = Flask(__name__)
app.config["TESTING"] = "pytest" in modules

for secret_name in ("SECRET_KEY", "SECURITY_PASSWORD_SALT", "JWT_SECRET_KEY"):
    app.config[secret_name] = getenv(secret_name, "hope it's local")


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
    message: str = error_text if app.debug else "Error occurred, check the logs"
    return {"message": message}, 500


@app.after_request
def add_header(res: Response):
    res.headers.add_header("X-Framework", "flask-fullstack")
    res.headers.add_header("X-Framework-Codename", "X")
    return res
