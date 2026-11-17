"""rtoml 0.14.0: rtoml.loads over local TOML text (PyO3 _rtoml over the Rust toml 1.1.8 crate and toml_parser 1.1.5).

rtoml returns plain dict, list, str, int, float, bool, datetime, date and time
values built by its Rust deserializer; the typed tree rules are copied from
controls/toml/check_controls.py and format those Python values, never the input text.
"""

from datetime import date, datetime, time, timezone
from decimal import Decimal

import rtoml
from rtoml import _rtoml

assert rtoml.__version__ == "0.14.0"
assert _rtoml.__file__.endswith(".so")


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
    return typed(rtoml.loads(data.decode("utf-8")))


def fuzz_one_input(data: bytes):
    try:
        parse_toml(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        # rtoml.TomlParsingError is a ValueError subclass.
        pass
