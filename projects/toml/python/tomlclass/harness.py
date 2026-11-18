"""tomlclass 0.4.1 pure-Python TOML parser over local TOML bytes through tomlclass.loads.

tomlclass.loads parses with its own parser into a lossless Document and returns its
tomllib-compatible plain dict of str, int, float, bool, datetime, date and time values;
the typed tree rules are copied from controls/toml/check_controls.py.
"""

from datetime import date, datetime, time, timezone
from decimal import Decimal

import tomlclass


def fraction(microsecond: int) -> str:
    return ("." + f"{microsecond:06d}".rstrip("0")) if microsecond else ""


def float_text(value: float) -> str:
    text = format(Decimal(repr(value)), "f")
    return text if "." in text else text + ".0"


def typed(value):
    if isinstance(value, dict):
        return {key: typed(item) for key, item in value.items()}
    if isinstance(value, list):
        return [typed(item) for item in value]
    if isinstance(value, bool):
        return {"type": "bool", "value": "true" if value else "false"}
    if isinstance(value, int):
        return {"type": "integer", "value": str(value)}
    if isinstance(value, float):
        return {"type": "float", "value": float_text(value)}
    if isinstance(value, str):
        return {"type": "string", "value": value}
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return {"type": "datetime-local",
                    "value": value.strftime("%Y-%m-%dT%H:%M:%S") + fraction(value.microsecond)}
        utc = value.astimezone(timezone.utc)
        return {"type": "datetime",
                "value": utc.strftime("%Y-%m-%dT%H:%M:%S") + fraction(utc.microsecond) + "Z"}
    if isinstance(value, date):
        return {"type": "date-local", "value": value.isoformat()}
    if isinstance(value, time):
        return {"type": "time-local", "value": value.strftime("%H:%M:%S") + fraction(value.microsecond)}
    raise TypeError(type(value))


def parse_toml(data: bytes):
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    return typed(tomlclass.loads(data.decode("utf-8"), toml_version="1.0"))


def fuzz_one_input(data: bytes):
    try:
        parse_toml(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        # tomlclass parse errors are ValueError subclasses.
        pass
