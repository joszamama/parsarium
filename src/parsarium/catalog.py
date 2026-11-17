"""Read the Parsarium catalog from Python.

    >>> from parsarium import catalog
    >>> pngs = catalog.targets(format="png")
    >>> pngs[0].id, pngs[0].package, pngs[0].input_api

Only runnable targets are returned: verified package paths and standard APIs
with a current harness receipt and AFL++ overlay, the same set the website and
``parsarium run-format`` use.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .snapshot import home

ECOSYSTEMS = ("c", "cpp", "go", "java", "javascript", "python", "rust", "php")


@dataclass(frozen=True)
class Target:
    id: str
    format: str
    ecosystem: str
    slug: str
    package: str
    release: str
    kind: str
    family: str | None
    input_api: str | None
    control: str
    expected_output: dict = field(compare=False, repr=False)
    path: Path = field(compare=False, repr=False)


def _runnable_check(root: Path):
    scripts = str(root / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    from audit_projects import fully_runnable  # type: ignore[import-not-found]
    return fully_runnable


def _formats(root: Path) -> tuple[str, ...]:
    """Read available format names from this version's pinned catalog."""
    return tuple(sorted({path.parent.name for path in (root / "data").glob("*/*/cell.json")}))


@lru_cache(maxsize=4)
def _load(root: Path) -> tuple[Target, ...]:
    fully_runnable = _runnable_check(root)
    found = []
    for path in sorted((root / "projects").glob("*/*/*/manifest.json")):
        manifest = json.loads(path.read_text())
        if not fully_runnable(path, manifest):
            continue
        release = manifest.get("release") or manifest.get("runtime")
        if not release:
            raise ValueError(f"runnable target has no release or runtime: {path}")
        family = manifest.get("runtime")
        input_api = manifest.get("api")
        if manifest.get("catalog_parser"):
            entries = json.loads((root / manifest["catalog_parser"]).read_text())
            entry = next((e for e in entries if e["name"] == manifest["package"]), None)
            if entry:
                family = entry.get("family")
                input_api = entry.get("input_api")
        fmt, eco, slug = path.parent.relative_to(root / "projects").parts
        found.append(Target(
            id=f"{fmt}/{eco}/{slug}", format=fmt, ecosystem=eco, slug=slug,
            package=manifest["package"], release=release,
            kind=manifest.get("kind", "third_party"), family=family, input_api=input_api,
            control=manifest["control"], expected_output=manifest.get("expected_output", {}),
            path=path.parent))
    return tuple(found)


def targets(format: str | None = None, ecosystem: str | None = None) -> list[Target]:
    """Runnable targets, optionally filtered by format and language."""
    root = home()
    formats = _formats(root)
    if format and format not in formats:
        raise ValueError(f"unknown format {format!r}; choose from {', '.join(formats)}")
    if ecosystem and ecosystem not in ECOSYSTEMS:
        raise ValueError(f"unknown ecosystem {ecosystem!r}; choose from {', '.join(ECOSYSTEMS)}")
    return [t for t in _load(root)
            if (not format or t.format == format) and (not ecosystem or t.ecosystem == ecosystem)]


def target(target_id: str) -> Target:
    """One target by its ID, such as ``"png/c/libpng"``."""
    for t in _load(home()):
        if t.id == target_id:
            return t
    raise KeyError(f"no runnable target {target_id!r}")


def control_path(t: Target) -> Path:
    """Absolute path of a target's valid control file."""
    return home() / t.control
