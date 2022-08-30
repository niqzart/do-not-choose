from __future__ import annotations

from sqlalchemy import (
    create_engine,
    select,
    MetaData,
    Column,
    Integer,
    String,
)

from .sqlalchemy_ext import Sessionmaker, Session, create_base
from ..interface import (
    Database,
    from_orm,
    User,
)


def configure_sqlalchemy(db_url: str):
    convention = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

    engine = create_engine(db_url, pool_recycle=280)  # echo=True
    db_meta = MetaData(bind=engine, naming_convention=convention)
    Base = create_base(db_meta)
    sessionmaker = Sessionmaker(bind=engine, class_=Session)

    return db_meta, Base, sessionmaker


def build_sqlalchemy_database(db_url: str, *config) -> Database:
    if len(config) != 3:
        config = configure_sqlalchemy(db_url)
    db_meta, Base, sessionmaker = config

    class UserORM(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        username = Column(String(100), nullable=False, index=True)
        password = Column(String(100), nullable=False)

    class SQLAlchemyDatabase(Database):
        def __init__(self):
            self.db_url = db_url
            self.meta = db_meta
            self.Base = Base

        def init_debug(self):
            self.meta.create_all()

        @sessionmaker.with_begin
        @from_orm(User)
        def _create_user(self, username: str, password: str, session) -> User:
            return UserORM.create(session, username=username, password=password)

        @sessionmaker.with_begin
        @from_orm(User)
        def find_user(self, user_id: int, session) -> UserORM | None:
            return session.get_first(select(UserORM).filter_by(id=user_id))

        @sessionmaker.with_begin
        @from_orm(User)
        def find_user_by_username(self, username: str, session) -> UserORM | None:
            return session.get_first(select(UserORM).filter_by(username=username))

    return SQLAlchemyDatabase()
