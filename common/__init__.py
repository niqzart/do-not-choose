from os import getenv

from dotenv import load_dotenv

from .interface import Database, User, UserSession, UserSessionInput
from .relational import build_sqlalchemy_database

load_dotenv(".env")

db_choice = getenv("DB_CHOICE", "relational")

if db_choice == "relational":
    db_link = getenv("DB_LINK", "sqlite:///test.db")
    db = build_sqlalchemy_database(db_link)
    if db_link.startswith("sqlite://"):
        db.init_debug()
else:
    raise ImportError(f"Database choice {db_choice} not found")
