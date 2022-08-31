from __future__ import annotations

from sqlalchemy import create_engine, MetaData

from .sqlalchemy_ext import Sessionmaker, Session, create_base


def configure_sqlalchemy(db_url: str):
    convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    engine = create_engine(db_url, pool_recycle=280)  # echo=True
    db_meta = MetaData(bind=engine, naming_convention=convention)
    Base = create_base(db_meta)
    sessionmaker = Sessionmaker(bind=engine, class_=Session)

    return db_meta, Base, sessionmaker
