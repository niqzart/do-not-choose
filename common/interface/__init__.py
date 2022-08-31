from abc import ABC

from .db_utils import from_orm, list_from_orm
from .users_db import UserDatabase, User


class Database(UserDatabase, ABC):
    def init_debug(self):
        pass
