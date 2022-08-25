from sys import modules

from __lib__.flask_fullstack import Flask
from __lib__.flask_fullstack.sqlalchemy import create_base, Sessionmaker, Session
from common import db_meta, engine

Base = create_base(db_meta)
sessionmaker = Sessionmaker(bind=engine, class_=Session)

app: Flask = Flask(__name__)
app.config["TESTING"] = "pytest" in modules.keys()
app.secrets_from_env("hope it's local")
# app.configure_cors()

app.configure_error_handlers(print)
app.config["RESTX_INCLUDE_ALL_MODELS"] = True
