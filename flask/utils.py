from __future__ import annotations

from functools import wraps

from flask import request


def parse_arguments(*keys: str) -> dict[str, str | None]:
    json_data = request.json or {}
    return {
        key: json_data.get(key) or request.values.get(key)
        for key in keys
    }


def argument_parser(*keys: str, require_all: bool = False, strings_only: bool = False):
    def argument_parser_wrapper(function):
        @wraps(function)
        def argument_parser_inner(*args, **kwargs):
            result: dict[str, ...] = parse_arguments(*keys)

            if require_all:
                for key, value in result.items():
                    if value is None:
                        return {"message": f"Missing required argument: {key}"}, 400

            if strings_only:
                result = {
                    key: value if value is None else str(value)
                    for key, value in result.items()
                }

            kwargs.update(result)
            return function(*args, **kwargs)

        return argument_parser_inner

    return argument_parser_wrapper
