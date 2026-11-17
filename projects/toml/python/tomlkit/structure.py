"""Print the typed TOML tree for one local file under one API mode.

Modes: ``tomlkit-items`` (tomlkit.parse on decoded text, walked by item type; the
harness path), ``tomlkit-unwrap`` (tomlkit.parse(text).unwrap()), ``tomlkit-bytes``
(tomlkit.parse on the raw bytes, walked by item type) and ``tomlkit-stream``
(tomlkit.load on a local binary stream, walked by item type). ``stdlib`` is the
CPython tomllib cross-check; it runs under /usr/bin/python3 -I where tomlkit is absent.
"""
from datetime import date, datetime, time, timezone
from decimal import Decimal
from io import BytesIO
import json
import sys
from pathlib import Path


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


def main() -> None:
    mode, path = sys.argv[1], Path(sys.argv[2])
    data = path.read_bytes()
    report = {"mode": mode}
    if mode == "stdlib":
        try:
            import tomlkit  # noqa: F401
        except ModuleNotFoundError:
            pass
        else:
            raise SystemExit("stdlib cross-check must not see tomlkit")
        import tomllib
        tree = typed(tomllib.loads(data.decode("utf-8")))
        report["python"] = sys.version.split()[0]
    elif mode.startswith("tomlkit-"):
        # The tomlkit parse path must not hand the document to tomllib.
        sys.modules["tomllib"] = None
        import tomlkit
        from harness import parse_toml, typed_item
        if mode == "tomlkit-items":
            tree = parse_toml(data)
        elif mode == "tomlkit-unwrap":
            tree = typed(tomlkit.parse(data.decode("utf-8")).unwrap())
        elif mode == "tomlkit-bytes":
            tree = typed_item(tomlkit.parse(data))
        elif mode == "tomlkit-stream":
            tree = typed_item(tomlkit.load(BytesIO(data)))
        else:
            raise SystemExit(f"unknown mode {mode}")
        report["tomlkit"] = tomlkit.__version__
    else:
        raise SystemExit(f"unknown mode {mode}")
    report["tree"] = tree
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
