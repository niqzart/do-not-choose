from __future__ import annotations

from enum import Enum
from functools import wraps
from typing import Type, Callable, TypeVar

from pydantic import BaseModel, create_model


class NamedIntEnum(int, Enum):
    value: int

    @property
    def label(self) -> str:
        return self.name.lower().replace("_", "-")


t = TypeVar("t", bound=BaseModel)


def patch_model(baseclass: type[t]) -> type[t]:
    # noinspection PyTypeChecker
    return create_model(
        f"{baseclass.__name__}Patch",
        **{key: (item.type_, None) for key, item in baseclass.__fields__.items()},
        __config__=baseclass.__config__,
        __validators__=baseclass.__validators__,
    )


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
