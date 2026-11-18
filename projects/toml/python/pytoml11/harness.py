"""pytoml11 0.0.5: pytoml11.loads over local TOML text (pybind11 _value over the vendored C++ toml11 parser).

pytoml11.loads returns its own Item tree (Table, Array, Integer, Float, String,
Boolean, DateTime, Date, Time) built from the toml11 value; the harness walks
Table keys and Array items and reads each scalar's documented ``value`` property
(str, int, float, bool, datetime, date or time). The typed tree rules are copied
from controls/toml/check_controls.py and format those Python values, never the
input text.
"""

from datetime import date, datetime, time, timezone
from decimal import Decimal

import pytoml11
from pytoml11 import _value

assert _value.__file__.endswith(".so")


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


# Each pytoml11 scalar item type and the plain Python type its value property must return.
SCALARS = (
    (pytoml11.Boolean, bool), (pytoml11.Integer, int), (pytoml11.Float, float), (pytoml11.String, str),
    (pytoml11.DateTime, datetime), (pytoml11.Date, date), (pytoml11.Time, time),
)


def plain(item):
    """Convert a pytoml11 Item to plain Python values through its documented API."""
    if isinstance(item, pytoml11.Table):
        return {key: plain(item[key]) for key in item.value}
    if isinstance(item, pytoml11.Array):
        return [plain(item[index]) for index in range(len(item))]
    for item_type, plain_type in SCALARS:
        if isinstance(item, item_type):
            value = item.value
            if type(value) is not plain_type:
                raise TypeError(f"{type(item).__name__}.value is {type(value).__name__}")
            return value
    raise TypeError(f"unexpected pytoml11 item {type(item).__name__}")


def parse_toml(data: bytes):
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    return typed(plain(pytoml11.loads(data.decode("utf-8"))))


def fuzz_one_input(data: bytes):
    try:
        parse_toml(data)
    except (pytoml11.TomlError, ValueError, TypeError, UnicodeError, OverflowError, RecursionError):
        pass
