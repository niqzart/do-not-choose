from __future__ import annotations

from functools import wraps

from flask import request


def parse_arguments(*keys: str) -> dict[str, str | None]:
    json_data = request.json or {}
    return {
        key: json_data.get(key) or request.values.get(key)
        for key in keys
    }


def argument_parser(*keys: str):
    def argument_parser_wrapper(function):
        @wraps(function)
        def argument_parser_inner(*args, **kwargs):
            kwargs.update(parse_arguments(*keys))
            return function(*args, **kwargs)

        return argument_parser_inner

    return argument_parser_wrapper
