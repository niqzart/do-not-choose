from __future__ import annotations

from .config_db import configure_sqlalchemy
from .sqlalchemy_ext import Sessionmaker, Session, create_base
from .users_rdb import build_user_database
from ..interface import Database


def build_sqlalchemy_database(db_url: str, *config) -> Database:
    if len(config) != 3:
        config = configure_sqlalchemy(db_url)
    db_meta, Base, sessionmaker = config

    UserDatabase = build_user_database(Base, sessionmaker)

    class SQLAlchemyDatabase(UserDatabase, Database):
        def init_debug(self):
            db_meta.create_all()

    return SQLAlchemyDatabase()
