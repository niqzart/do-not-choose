from __future__ import annotations

from enum import auto

from pydantic import BaseModel, constr

from .db_utils import NamedIntEnum
from .users_db import User


# noinspection PyArgumentList
class AccessType(NamedIntEnum):
    PUBLIC = auto()
    PRIVATE = auto()


# noinspection PyArgumentList
class GameType(NamedIntEnum):
    DEFAULT = auto()


# noinspection PyArgumentList
class ParticipantRole(NamedIntEnum):
    OWNER = auto()
    ADMIN = auto()
    MODER = auto()
    BASIC = auto()


class GameInput(BaseModel):
    name: constr(max_length=100)
    type: GameType
    access: AccessType
    max_players: int


class Game(GameInput):
    id: int
    owner: User
    joined_players: int


class Participant(User):
    role: ParticipantRole
