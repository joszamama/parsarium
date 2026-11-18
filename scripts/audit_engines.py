#!/usr/bin/env python3
"""Check the engine maps in data/curation/engines/<format>.json.

Each selected third-party parser path is mapped exactly once to the engine that
parses the format's bytes, with its relation to that engine:

own         the package is the engine
wrapper     engine written in the package's language (C and C++ count as one)
binding     engine in another language, reached through native code
subprocess  the package runs an external program
wasm        engine compiled to WebAssembly
port        translation of an engine into another language
vendored    the package includes a copy of the engine's source
fork        derived from the engine's code base
"""
from __future__ import annotations

import glob
import json
from pathlib import Path

from audit_upstream_repositories import parser_keys

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = {"own", "wrapper", "binding", "subprocess", "wasm", "port", "vendored", "fork"}
LANGUAGES = {"c", "cpp", "go", "java", "javascript", "python", "rust", "php"}
CONFIDENCE = {"high", "medium", "low"}
SAME = {("c", "cpp"), ("cpp", "c")}


def load() -> list[dict]:
    return [json.loads(Path(f).read_text()) for f in sorted(glob.glob(str(ROOT / "data/curation/engines/*.json")))]


def problems(maps: list[dict], keys: set[str]) -> list[str]:
    found: list[str] = []
    seen: dict[str, int] = {}
    languages: dict[str, str] = {}
    for data in maps:
        fmt = data.get("format")
        for engine, info in data.get("engines", {}).items():
            lang = info.get("language", "")
            if lang not in LANGUAGES and not lang.startswith("other:"):
                found.append(f"{fmt}: engine {engine} has unknown language {lang!r}")
            if engine in languages and languages[engine] != lang:
                found.append(f"engine {engine} has two languages: {languages[engine]}, {lang}")
            languages.setdefault(engine, lang)
            repo = info.get("repository")
            if repo is not None and not str(repo).startswith("https://"):
                found.append(f"{fmt}: engine {engine} repository is not https")
        used = set()
        for row in data.get("paths", []):
            path = row.get("path", "")
            seen[path] = seen.get(path, 0) + 1
            if not path.split("/")[1:2] == [fmt]:
                found.append(f"{path}: listed under format {fmt}")
            engine = row.get("engine")
            if engine not in data.get("engines", {}):
                found.append(f"{path}: engine {engine!r} is not defined in {fmt}.json")
                continue
            used.add(engine)
            relation = row.get("relation")
            if relation not in RELATIONS:
                found.append(f"{path}: unknown relation {relation!r}")
            if row.get("confidence") not in CONFIDENCE:
                found.append(f"{path}: confidence must be high, medium or low")
            if not row.get("evidence"):
                found.append(f"{path}: no evidence")
            eco, lang = path.split("/")[0], data["engines"][engine]["language"]
            same = lang == eco or (eco, lang) in SAME
            if relation == "wrapper" and not same:
                found.append(f"{path}: wrapper of a {lang} engine from {eco}; use binding")
            if relation == "binding" and same:
                found.append(f"{path}: binding of a {lang} engine from {eco}; use wrapper")
        for engine in set(data.get("engines", {})) - used:
            found.append(f"{fmt}: engine {engine} is defined but not used")
    for path in sorted(keys - set(seen)):
        found.append(f"{path}: no engine row")
    for path in sorted(set(seen) - keys):
        found.append(f"{path}: engine row for an unknown parser path")
    for path, count in seen.items():
        if count > 1:
            found.append(f"{path}: {count} engine rows")
    return found


if __name__ == "__main__":
    issues = problems(load(), parser_keys())
    for issue in issues:
        print(issue)
    raise SystemExit(1 if issues else 0)
