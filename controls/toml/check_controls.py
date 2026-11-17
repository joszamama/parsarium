"""Check TOML controls against their committed typed trees.

The two controls are hand-written TOML 1.0.0 documents in UTF-8 with LF line
endings. Their expected typed trees (``*.expected.json``) were written by hand
from the TOML 1.0.0 specification. This script parses each control with
Python's standard-library ``tomllib`` (Python 3.11+), converts the result to the
same typed tree every harness reports, and requires equality with the committed
file. ``tomllib`` is the oracle. It is a vendored copy of the third-party
``tomli`` parser, so for the Python ``tomli`` path the hand-written expected
tree, not ``tomllib``, is the independent check.

Typed tree (modeled on the toml-test JSON encoding):

* a table is a JSON object and an array is a JSON array;
* every scalar is ``{"type": T, "value": S}`` with ``S`` a string;
* ``string``: the decoded string;
* ``integer``: the decimal value with an optional leading ``-``;
* ``float``: the shortest round-trip decimal digits, written positionally
  (no exponent) with at least one fractional digit, e.g. ``1000.0``;
* ``bool``: ``true`` or ``false``;
* ``datetime`` (offset date-time): the UTC instant
  ``YYYY-MM-DDTHH:MM:SS[.fraction]Z``;
* ``datetime-local``: ``YYYY-MM-DDTHH:MM:SS[.fraction]``;
* ``date-local``: ``YYYY-MM-DD``;
* ``time-local``: ``HH:MM:SS[.fraction]``.

A fraction keeps its significant digits only (no trailing zeros) and is
omitted when zero. Object key order is not significant; the canonical
serialization sorts keys.
"""

from datetime import date, datetime, time, timezone
from decimal import Decimal
from hashlib import sha256
import json
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parent
CONTROLS = {
    "service-config.toml": "590659301fe3d555dd34803e1aa70ea0befbd5546c8b2ed23f0e0a932a806257",
    "typed-scalars.toml": "bfd655fd12df79f6b61ecb258d5713a300b03197f46a7f84f2b1f6d7a19d36d0",
}


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


def canonical(tree) -> str:
    return json.dumps(tree, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


if __name__ == "__main__":
    for name, digest in CONTROLS.items():
        data = (ROOT / name).read_bytes()
        assert sha256(data).hexdigest() == digest, (name, sha256(data).hexdigest())
        assert b"\r" not in data and data.endswith(b"\n"), name
        observed = typed(tomllib.loads(data.decode("utf-8")))
        expected = json.loads((ROOT / name.replace(".toml", ".expected.json")).read_text(encoding="utf-8"))
        assert observed == expected, (name, canonical(observed))
        print(name, len(data), "bytes", sha256(canonical(expected).encode()).hexdigest())
