"""tomlkit 0.15.2 style-preserving TOML parser over local TOML bytes through tomlkit.parse.

The typed tree is built by walking the returned TOMLDocument by tomlkit item type
(Table, InlineTable, AoT, Array, Bool, Integer, Float, String, DateTime, Date, Time)
and unwrapping each scalar item; it must equal the tree built from
TOMLDocument.unwrap(). The scalar rules are copied from controls/toml/check_controls.py.
"""

from datetime import date, datetime, time, timezone
from decimal import Decimal

import tomlkit
from tomlkit import items
from tomlkit.exceptions import TOMLKitError
from tomlkit.container import Container, OutOfOrderTableProxy


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


# Each tomlkit scalar item type and the plain Python type its unwrap() must return.
SCALARS = (
    (items.Bool, bool), (items.Integer, int), (items.Float, float), (items.String, str),
    (items.DateTime, datetime), (items.Date, date), (items.Time, time),
)


def typed_item(node):
    if isinstance(node, (Container, items.AbstractTable)):
        return {key: typed_item(node.item(key)) for key in node}
    if isinstance(node, OutOfOrderTableProxy):
        # Split (out-of-order) tables only; neither control contains one.
        return typed(node.unwrap())
    if isinstance(node, items.AoT):
        return [typed_item(table) for table in node.body]
    if isinstance(node, items.Array):
        return [typed_item(node.item(index)) for index in range(len(node))]
    for item_type, plain_type in SCALARS:
        if isinstance(node, item_type):
            plain = node.unwrap()
            if (type(plain) is not plain_type or
                    (plain_type is date and isinstance(plain, datetime))):
                raise TypeError(f"{type(node).__name__} unwrapped to {type(plain).__name__}")
            return typed(plain)
    raise TypeError(f"unexpected tomlkit node {type(node).__name__}")


def parse_toml(data: bytes):
    if not data or len(data) > (1 << 20):
        raise ValueError("input outside harness limit")
    document = tomlkit.parse(data.decode("utf-8"))
    tree = typed_item(document)
    if tree != typed(document.unwrap()):
        raise ValueError("item-type tree differs from TOMLDocument.unwrap()")
    return tree


def fuzz_one_input(data: bytes):
    try:
        parse_toml(data)
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError,
            TOMLKitError):
        pass
