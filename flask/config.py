from os import getenv
from sys import modules

from flask import Response, Flask
from werkzeug.exceptions import NotFound, InternalServerError

app: Flask = Flask(__name__)
app.config["TESTING"] = "pytest" in modules

for secret_name in ("SECRET_KEY", "SECURITY_PASSWORD_SALT", "JWT_SECRET_KEY"):
    app.config[secret_name] = getenv(secret_name, "hope it's local")


@app.errorhandler(NotFound)
def on_not_found(_):
    return {"message": "Not Found"}, 404


@app.errorhandler(InternalServerError)
def on_any_exception(_: InternalServerError):
    return {"message": "Error occurred, check the logs"}, 500


@app.after_request
def add_header(res: Response):
    res.headers.add_header("X-Framework", "flask-fullstack")
    res.headers.add_header("X-Framework-Codename", "X")
    return res
