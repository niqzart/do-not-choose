from __future__ import annotations

from passlib.hash import pbkdf2_sha256
from pydantic import BaseModel, constr


class UserBase(BaseModel):
    username: constr(max_length=100)

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    password: str


class UserDatabase:
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

    def block_token(self, jti: str) -> None:
        raise NotImplementedError()

    def is_token_blocked(self, jti: str) -> bool:
        raise NotImplementedError()
