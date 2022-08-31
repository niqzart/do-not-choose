from __future__ import annotations

from sqlalchemy import Column, Integer, String, select

from ..interface import UserDatabase, User, from_orm


def build_user_database(base_klass, sessionmaker) -> type[UserDatabase]:
    class UserORM(base_klass):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        username = Column(String(100), nullable=False, index=True)
        password = Column(String(100), nullable=False)

    class BlockedToken(base_klass):
        __tablename__ = "blocked_tokens"

        id = Column(Integer, primary_key=True)
        jti = Column(String(36), nullable=False, index=True)

    class SQLAlchemyDatabase(UserDatabase):
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

        @sessionmaker.with_begin
        def block_token(self, jti: str, session) -> None:
            return BlockedToken.create(session, jti=jti)

        @sessionmaker.with_begin
        def is_token_blocked(self, jti: str, session) -> bool:
            return session.get_first(select(BlockedToken).filter_by(jti=jti)) is not None

    return SQLAlchemyDatabase
