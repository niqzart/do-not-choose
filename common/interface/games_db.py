from __future__ import annotations

from enum import auto

from pydantic import BaseModel, constr

from .db_utils import NamedIntEnum, patch_model
from .users_db import User


# noinspection PyArgumentList
class AccessType(NamedIntEnum):
    PUBLIC = auto()
    PRIVATE = auto()


# noinspection PyArgumentList
class GameType(NamedIntEnum):
    DEFAULT = auto()


# noinspection PyArgumentList
class GameStatus(NamedIntEnum):
    CREATED = auto()
    STARTED = auto()
    CLOSED = auto()


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
    status: GameStatus
    max_players: int


class Game(GameInput):
    id: int
    owner: User
    joined_players: int


class ParticipantInput(BaseModel):
    role: ParticipantRole
    joined: bool

    def to_participant(self, user: User) -> Participant:
        return Participant(**self.dict(), **user.dict())


ParticipantPatch = patch_model(ParticipantInput)


class Participant(User, ParticipantInput):
    @classmethod
    def combine(cls, user: User, data: ParticipantInput) -> Participant:
        return data.to_participant(user)


class GameCRUDLDatabase:
    def _create_game(self, data: GameInput, creator: User) -> Game:
        raise NotImplementedError()

    def create_game(self, data: GameInput, creator: User) -> Game:
        game = self._create_game(data, creator)
        owner = ParticipantInput(role=ParticipantRole.OWNER, joined=True)
        self.create_participant(game, Participant.combine(creator, owner))
        return game

    def find_game(self, game_id: int) -> Game:
        raise NotImplementedError()

    def update_game(self, data: GameInput) -> Game:
        raise NotImplementedError()

    def delete_game(self, game_id: int) -> bool:
        raise NotImplementedError()

    def create_participant(self, game: Game, user: Participant) -> Participant:
        raise NotImplementedError()

    def update_participant(self, game: Game, user: ParticipantPatch) -> Participant:
        raise NotImplementedError()

    def kick_participant(self, game: Game, user_id: int) -> bool:
        raise NotImplementedError()
