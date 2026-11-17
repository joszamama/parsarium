"""Declarative active and pilot format registry shared by catalog tools and CLI."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def load_registry(path: Path = ROOT / "data/formats.json") -> tuple[tuple[str, ...], tuple[dict, ...]]:
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1 or not isinstance(data.get("ecosystems"), list) or \
            not isinstance(data.get("formats"), list):
        raise ValueError("invalid format registry schema")
    ecosystems = tuple(data["ecosystems"])
    if len(ecosystems) != len(set(ecosystems)) or not ecosystems or any(
            not isinstance(item, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", item)
            for item in ecosystems):
        raise ValueError("invalid or duplicate ecosystem in format registry")
    formats = tuple(data["formats"])
    seen = set()
    for item in formats:
        if not isinstance(item, dict) or set(item) != {"id", "label", "description", "phase"}:
            raise ValueError("invalid format registry entry")
        name = item["id"]
        if (not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", name)
                or name in seen or item["phase"] not in {"active", "pilot"}
                or not isinstance(item["label"], str) or not item["label"].strip()
                or not isinstance(item["description"], str) or not item["description"].strip()):
            raise ValueError(f"invalid or duplicate format registry entry: {name!r}")
        seen.add(name)
    if not formats or not any(item["phase"] == "active" for item in formats):
        raise ValueError("format registry has no active formats")
    return ecosystems, formats


ECOSYSTEMS, FORMAT_RECORDS = load_registry()
FORMAT_BY_ID = {item["id"]: item for item in FORMAT_RECORDS}
ACTIVE_FORMATS = tuple(item["id"] for item in FORMAT_RECORDS if item["phase"] == "active")
PILOT_FORMATS = tuple(item["id"] for item in FORMAT_RECORDS if item["phase"] == "pilot")
ALL_FORMATS = (*ACTIVE_FORMATS, *PILOT_FORMATS)


def phase(format_name: str) -> str:
    return FORMAT_BY_ID[format_name]["phase"]
