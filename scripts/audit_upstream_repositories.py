#!/usr/bin/env python3
"""Check data/curation/upstream-repositories.json against the parser records.

Every selected third-party parser path (data/<eco>/<fmt>/parsers.json) needs
exactly one row; shown URLs are https; a row without a repository explains
why in repository_note; fetched evidence carries its capture time and hash.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/curation/upstream-repositories.json"
ECOSYSTEMS = ("c", "cpp", "go", "java", "javascript", "php", "python", "rust")


REGISTRY_NAMES = {
    "pypi.org": "PyPI", "www.npmjs.com": "npm", "crates.io": "crates.io", "packagist.org": "Packagist",
    "pkg.go.dev": "pkg.go.dev", "central.sonatype.com": "Maven Central", "conan.io": "Conan Center",
    "tracker.debian.org": "Debian",
}


def registry_name(url: str | None) -> str | None:
    """Display name of the registry behind a registry_url."""
    if not url:
        return None
    host = url.split("/")[2]
    return REGISTRY_NAMES.get(host, host)


def load_rows() -> dict:
    """Rows keyed "<eco>/<fmt>/<name>"."""
    return json.loads(DATA.read_text())["rows"]


def parser_keys(root: Path = ROOT) -> set[str]:
    keys = set()
    for eco in ECOSYSTEMS:
        for path in (root / "data" / eco).glob("*/parsers.json"):
            for row in json.loads(path.read_text()):
                keys.add(f"{eco}/{path.parent.name}/{row['name']}")
    return keys


def problems(doc: dict, keys: set[str]) -> list[str]:
    rows = doc.get("rows", {})
    out = [f"missing upstream row: {k}" for k in sorted(keys - rows.keys())]
    out += [f"upstream row without a parser record: {k}" for k in sorted(rows.keys() - keys)]
    for key, row in sorted(rows.items()):
        eco, fmt, name = key.split("/", 2)
        if (row.get("ecosystem"), row.get("format"), row.get("name")) != (eco, fmt, name):
            out.append(f"row fields disagree with key: {key}")
        for field in ("repository", "registry_url", "homepage"):
            value = row.get(field)
            if value is not None and (not isinstance(value, str) or not value.startswith("https://")):
                out.append(f"{field} is not https: {key}")
        if row.get("repository"):
            if not row.get("source"):
                out.append(f"repository without source: {key}")
        elif not (isinstance(row.get("repository_note"), str) and row["repository_note"].strip()):
            out.append(f"no repository and no repository_note: {key}")
        if row.get("captured_at_utc") and not re.fullmatch(r"[0-9a-f]{64}", str(row.get("response_sha256"))):
            out.append(f"fetched row without response_sha256: {key}")
    return out


def main() -> int:
    found = problems(json.loads(DATA.read_text()), parser_keys())
    for line in found:
        print(line, file=sys.stderr)
    if found:
        return 1
    print("Upstream repository rows cover every parser path")
    return 0


if __name__ == "__main__":
    sys.exit(main())
