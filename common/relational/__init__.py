from __future__ import annotations

from sqlalchemy import (
    create_engine, select, MetaData, Column, ForeignKey,
    Integer, String, Text
)
from sqlalchemy.orm import relationship

from .sqlalchemy_ext import Sessionmaker, Session, create_base
from ..interface import (
    Database, from_orm, list_from_orm,
    UserInput, User, UserSession, UserSessionInput,
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
        username = Column(String(100), nullable=False)
        password = Column(String(100), nullable=False)

    class UserSessionORM(Base):
        __tablename__ = "user_sessions"

        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey(UserORM.id),
                         nullable=False, index=True)
        user = relationship(UserORM, foreign_keys=[user_id])
        device = Column(Text, nullable=False)

        @classmethod
        def find_by_id(cls, session, session_id: int) -> UserSessionORM | None:
            return session.get_first(select(UserSessionORM).filter_by(id=session_id))

    class SQLAlchemyDatabase(Database):
        @sessionmaker.with_begin
        @from_orm(User)
        def create_user(self, session, user: UserInput) -> UserORM:
            return UserORM.create(session, **user.dict())

        @sessionmaker.with_begin
        @from_orm(User)
        def find_user(self, session, user_id: int) -> UserORM | None:
            return session.get_first(select(UserORM).filter_by(id=user_id))

        @sessionmaker.with_begin
        @from_orm(UserSession)
        def create_user_session(self, session, user: User, user_session: UserSessionInput) -> UserSessionORM:
            return UserSessionORM.create(session, **user_session.dict())

        @sessionmaker.with_begin
        @from_orm(UserSession)
        def find_user_session(self, session, session_id: int) -> UserSessionORM | None:
            return UserSessionORM.find_by_id(session, session_id)

        @sessionmaker.with_begin
        def delete_user_session(self, session, session_id: int) -> None:
            user_session = UserSessionORM.find_by_id(session, session_id)
            user_session.delete(session)

        @sessionmaker.with_begin
        @list_from_orm(UserSession)
        def list_user_sessions(self, session, user: User) -> list[UserSession]:
            return session.get_all(select(UserSessionORM).filter_by(user_id=user.id))

        @sessionmaker.with_begin
        @from_orm(User)
        def find_user_by_session_id(self, session, session_id: int) -> User | None:
            user_session = UserSessionORM.find_by_id(session, session_id)
            return None if user_session is None else user_session.user

    return SQLAlchemyDatabase()
