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
        if (not isinstance(item, dict) or not {"id", "label", "description", "phase"} <= set(item)
                or set(item) - {"id", "label", "description", "phase", "project_formats"}):
            raise ValueError("invalid format registry entry")
        name = item["id"]
        if (not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", name)
                or name in seen or item["phase"] not in {"active", "pilot"}
                or not isinstance(item["label"], str) or not item["label"].strip()
                or not isinstance(item["description"], str) or not item["description"].strip()):
            raise ValueError(f"invalid or duplicate format registry entry: {name!r}")
        aliases = item.get("project_formats", [name])
        if (not isinstance(aliases, list) or name not in aliases
                or any(not isinstance(alias, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", alias)
                       for alias in aliases)):
            raise ValueError(f"invalid project_formats for format registry entry: {name!r}")
        seen.add(name)
    if not formats or not any(item["phase"] == "active" for item in formats):
        raise ValueError("format registry has no active formats")
    return ecosystems, formats


ECOSYSTEMS, FORMAT_RECORDS = load_registry()
FORMAT_BY_ID = {item["id"]: item for item in FORMAT_RECORDS}
ACTIVE_FORMATS = tuple(item["id"] for item in FORMAT_RECORDS if item["phase"] == "active")
PILOT_FORMATS = tuple(item["id"] for item in FORMAT_RECORDS if item["phase"] == "pilot")
CATALOG_FORMATS = (*ACTIVE_FORMATS, *PILOT_FORMATS)


# A merged catalog format may keep projects under an older format directory.
# For example, MP3 projects verified on the ID3v2-tagged control still live in
# projects/mp3_id3v2/; they belong to the single catalog format "mp3".
PROJECT_FORMAT_TO_CATALOG = {alias: item["id"] for item in FORMAT_RECORDS
                             for alias in item.get("project_formats", [item["id"]])}
if len(PROJECT_FORMAT_TO_CATALOG) != sum(len(item.get("project_formats", [item["id"]]))
                                         for item in FORMAT_RECORDS):
    raise ValueError("a project format directory maps to more than one catalog format")
PROJECT_FORMATS = tuple(PROJECT_FORMAT_TO_CATALOG)
LEGACY_PROJECT_FORMATS = tuple(alias for alias, fmt in PROJECT_FORMAT_TO_CATALOG.items() if alias != fmt)
# Format names the command line accepts: catalog formats plus target directories
# kept under an older name (for example `parsarium run mp3_id3v2 java jaudiotagger ...`).
ALL_FORMATS = (*CATALOG_FORMATS, *LEGACY_PROJECT_FORMATS)


def catalog_format(format_name: str) -> str:
    """Return the catalog format for a catalog or project-directory format name."""
    return PROJECT_FORMAT_TO_CATALOG[format_name]


def resolve_data_path(relative: str) -> str:
    """Map a data/<eco>/<legacy-format>/... path recorded in a pinned manifest to its cell."""
    parts = relative.split("/")
    if len(parts) > 3 and parts[0] == "data" and parts[2] in LEGACY_PROJECT_FORMATS:
        parts[2] = PROJECT_FORMAT_TO_CATALOG[parts[2]]
    return "/".join(parts)


def phase(format_name: str) -> str:
    return FORMAT_BY_ID[catalog_format(format_name)]["phase"]
