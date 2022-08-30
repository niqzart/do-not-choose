from __future__ import annotations

from functools import wraps
from typing import Type, Callable

from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel, constr


class UserBase(BaseModel):
    username: constr(max_length=100)

    class Config:
        orm_mode = True


class User(UserBase):
    id: int


class UserSessionInput(BaseModel):
    device: str

    class Config:
        orm_mode = True


class UserSession(UserSessionInput):
    id: int


class Database:
    @staticmethod
    def generate_hash(password) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_hash(password, hashed) -> bool:
        return pbkdf2_sha256.verify(password, hashed)

    def _create_user(self, username: str, password: str) -> User:
        raise NotImplementedError()

    def create_user(self, username: str, password: str) -> User:
        return self._create_user(username, self.generate_hash(password))

    def find_user(self, user_id: int) -> User | None:
        raise NotImplementedError()

    def find_user_by_username(self, user_id: int) -> User | None:
        raise NotImplementedError()

    def check_password(self, user_id: int, password: str) -> bool | None:
        raise NotImplementedError()

    def create_user_session(self, user: User, user_session: UserSessionInput) -> UserSession:
        raise NotImplementedError()

    def find_user_session(self, session_id: int) -> UserSession | None:
        raise NotImplementedError()

    def delete_user_session(self, session_id: int) -> None:
        raise NotImplementedError()

    def list_user_sessions(self, user: User) -> list[UserSession]:
        raise NotImplementedError()

    def find_user_by_session_id(self, session_id: int) -> User | None:
        raise NotImplementedError()


def from_orm(model: Type[BaseModel]):
    def from_orm_wrapper(function) -> Callable[..., model | None]:
        @wraps(function)
        def from_orm_inner(*args, **kwargs):
            result = function(*args, **kwargs)
            if result is None:
                return None
            return model.from_orm(result)

        return from_orm_inner

    return from_orm_wrapper


def list_from_orm(model: Type[BaseModel]):
    def list_from_orm_wrapper(function) -> Callable[..., list[model]]:
        @wraps(function)
        def list_from_orm_inner(*args, **kwargs):
            return [model.from_orm(res)
                    for res in function(*args, **kwargs)]

        return list_from_orm_inner

    return list_from_orm_wrapper
