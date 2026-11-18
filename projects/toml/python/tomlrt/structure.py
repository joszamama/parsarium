"""Print the typed TOML tree for one local file under one API mode.

Modes: ``tomlrt-str`` (tomlrt.loads on decoded text; the harness path) and
``tomlrt-stream`` (tomlrt.load on a local binary stream). ``stdlib`` runs CPython
tomllib under /usr/bin/python3 -I where tomlrt is absent; tomllib is the tomli family,
independent of tomlrt.
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
            import tomlrt  # noqa: F401
        except ModuleNotFoundError:
            pass
        else:
            raise SystemExit("stdlib cross-check must not see tomlrt")
        import tomllib
        tree = typed(tomllib.loads(data.decode("utf-8")))
        report["python"] = sys.version.split()[0]
    elif mode in ("tomlrt-str", "tomlrt-stream"):
        # The tomlrt parse path must not hand the document to tomllib.
        sys.modules["tomllib"] = None
        import importlib.metadata
        import tomlrt
        from harness import parse_toml
        tree = parse_toml(data) if mode == "tomlrt-str" else typed(tomlrt.load(BytesIO(data)))
        report["tomlrt"] = importlib.metadata.version("tomlrt")
    else:
        raise SystemExit(f"unknown mode {mode}")
    report["tree"] = tree
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
