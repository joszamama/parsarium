#!/usr/bin/env python3
"""Build the static Parsarium site from committed catalog evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = Path(__file__).resolve().parent
REPO_URL = "https://github.com/joszamama/parsarium"

FORMATS = [
    ("png", "PNG", "Image", "A tiny grid of pixels, carried in chunks."),
    ("zip", "ZIP", "Archive", "Files within a file, with a directory at the end."),
    ("mp4", "MP4", "Media", "Boxes that organize moving pictures and sound."),
    ("wav", "WAV", "Audio", "A familiar RIFF wrapper around sound samples."),
    ("pdf", "PDF", "Document", "Pages, objects, and a trail of references."),
    ("svg", "SVG", "Vector", "Shapes described as XML."),
    ("http11", "HTTP/1.1", "Protocol", "Requests and headers travelling as text."),
    ("ascii_ply", "ASCII PLY", "Geometry", "Vertices and faces in a readable mesh."),
    ("ascii_pnm", "ASCII PNM", "Image", "Plain text pixels with very little ceremony."),
    ("mp3_id3v2", "MP3 + ID3v2", "Audio", "Compressed audio with a metadata prelude."),
]
ECOSYSTEMS = ["c", "cpp", "go", "java", "javascript", "python", "rust", "php"]
DEMO_PROJECTS = [
    "projects/png/python/pypng/manifest.json",
    "projects/zip/rust/zip/manifest.json",
    "projects/mp4/php/getid3/manifest.json",
    "projects/wav/c/dr_wav/manifest.json",
    "projects/pdf/java/pdfbox/manifest.json",
    "projects/svg/rust/usvg/manifest.json",
    "projects/http11/python/h11/manifest.json",
    "projects/ascii_ply/python/plyfile/manifest.json",
    "projects/ascii_pnm/python/netpbmfile/manifest.json",
    "projects/mp3_id3v2/python/mutagen/manifest.json",
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def repo_link(path: str) -> str:
    return f"{REPO_URL}/blob/main/{path}"


def build(output: Path) -> None:
    cells_source = read_json(ROOT / "data/cells.json")["cells"]
    coverage = read_json(ROOT / "data/projects-coverage.json")
    coverage_by_cell = {(c["format"], c["ecosystem"]): c for c in coverage["cells"]}
    manifests = {}
    standard_projects = {}
    for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json")):
        manifest = read_json(path)
        key = (manifest["format"], manifest["ecosystem"], manifest["package"], manifest["release"])
        manifests[key] = (path, manifest)
        if manifest.get("kind") == "standard":
            standard_projects[(manifest["format"], manifest["ecosystem"])] = path

    parsers = []
    cells = []
    for cell in cells_source:
        fmt, eco = cell["format"], cell["ecosystem"]
        source = f"data/{eco}/{fmt}/parsers.json"
        entries = read_json(ROOT / source)
        if len(entries) != cell["verified_third_party_count"]:
            raise ValueError(f"count mismatch in {source}")
        c = coverage_by_cell[(fmt, eco)]
        cells.append({
            "format": fmt,
            "ecosystem": eco,
            "verified": len(entries),
            "standard": cell["verified_standard_or_runtime_count"],
            "runnable": c["containerized_verified"] + c["standard_containerized_verified"],
            "unresolved": cell["unresolved_documentation_leads"],
            "uncertainty": cell["uncertainty"],
            "rankingUrl": repo_link(f"data/{eco}/{fmt}/ranking.md"),
            "evidenceUrl": repo_link(source),
            "standardUrl": repo_link(f"data/{eco}/{fmt}/standard.json"),
            "standardProjectUrl": (
                repo_link(str(standard_projects[(fmt, eco)].relative_to(ROOT)))
                if (fmt, eco) in standard_projects else None
            ),
        })
        for entry in entries:
            key = (fmt, eco, entry["name"], entry["version"])
            project = manifests.get(key)
            record = {
                "format": fmt,
                "ecosystem": eco,
                "name": entry["name"],
                "version": entry["version"],
                "scope": entry["scope"],
                "family": entry["family"],
                "license": entry["license"],
                "inputApi": entry["input_api"],
                "documentation": entry["documentation"],
                "evidenceUrl": repo_link(source),
            }
            if project:
                project_path, _ = project
                record["project"] = str(project_path.parent.relative_to(ROOT))
                record["projectUrl"] = repo_link(str(project_path.relative_to(ROOT)))
            parsers.append(record)

    if len(parsers) != coverage["catalog_paths"]:
        raise ValueError("catalog total does not match project coverage")
    if len(cells) != 80:
        raise ValueError("expected all 80 format × ecosystem cells")
    if sum("projectUrl" in parser for parser in parsers) != coverage["containerized_verified"]:
        raise ValueError("third-party project links do not match project coverage")
    if len(standard_projects) != coverage["standard_containerized_verified"]:
        raise ValueError("standard project links do not match project coverage")

    standard_targets = []
    for (fmt, eco), project_path in sorted(standard_projects.items()):
        manifest = read_json(project_path)
        inventory_path = ROOT / manifest["standard_inventory"]
        inventory = read_json(inventory_path)
        documented_api = next(
            (api for api in inventory["verified_apis"] if api["api"] == manifest["api"]),
            None,
        )
        if documented_api is None:
            raise ValueError(f"standard API missing from inventory: {project_path}")
        standard_targets.append({
            "type": "standard",
            "format": fmt,
            "ecosystem": eco,
            "name": manifest["package"],
            "version": manifest["release"],
            "scope": "format-aware runtime API",
            "family": manifest["runtime"],
            "inputApi": manifest["api"],
            "documentation": documented_api["documentation"],
            "evidenceUrl": repo_link(str(inventory_path.relative_to(ROOT))),
            "projectUrl": repo_link(str(project_path.relative_to(ROOT))),
        })

    format_counts = Counter(p["format"] for p in parsers)
    format_runs = Counter()
    for cell in cells:
        format_runs[cell["format"]] += cell["runnable"]
    formats = [
        {"id": fmt, "label": label, "category": category, "description": description,
         "verified": format_counts[fmt], "runnable": format_runs[fmt]}
        for fmt, label, category, description in FORMATS
    ]

    demos = []
    controls_output = output / "controls"
    if controls_output.exists():
        shutil.rmtree(controls_output)
    for source in DEMO_PROJECTS:
        manifest = read_json(ROOT / source)
        fmt, eco, slug = manifest["format"], manifest["ecosystem"], Path(source).parent.name
        parser_record = next(
            (record for record in parsers if record["format"] == fmt
             and record["ecosystem"] == eco and record["name"] == manifest["package"]
             and record["version"] == manifest["release"]),
            None,
        )
        if parser_record is None:
            raise ValueError(f"demo target missing from verified catalog: {source}")
        control_path = ROOT / manifest["control"]
        data = control_path.read_bytes()
        if hashlib.sha256(data).hexdigest() != manifest["control_sha256"]:
            raise ValueError(f"control hash mismatch: {control_path}")
        destination = controls_output / manifest["format"] / control_path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(control_path, destination)
        target = f"{fmt} {eco} {slug}"
        run_dir = f"runs/{fmt}-{slug}"
        demos.append({
            "format": fmt,
            "ecosystem": eco,
            "package": manifest["package"],
            "release": manifest["release"],
            "inputApi": parser_record["inputApi"],
            "control": manifest["control"],
            "controlUrl": str(destination.relative_to(output)),
            "bytes": len(data),
            "expectedOutput": manifest["expected_output"],
            "manifestUrl": repo_link(source),
            "controlCommand": f"python3 parsarium.py run {target} {manifest['control']} --results {run_dir}-control",
            "inputCommand": f"python3 parsarium.py run {target} INPUT_FILE --results {run_dir}-single",
            "replayCommand": f"python3 parsarium.py replay {target} CORPUS_DIR {run_dir}-replay",
            "aflCommands": [
                f"python3 parsarium.py afl build {target}",
                f"python3 parsarium.py afl prepare {target} {run_dir}-afl",
                f"python3 parsarium.py afl run {run_dir}-afl --seconds 60",
            ],
        })
    if [demo["format"] for demo in demos] != [fmt for fmt, *_ in FORMATS]:
        raise ValueError("run examples must cover every format in display order")

    catalog = {
        "summary": {
            "verified": len(parsers),
            "cells": len(cells),
            "formats": len(FORMATS),
            "ecosystems": len(ECOSYSTEMS),
            "runnable": coverage["containerized_verified"] + coverage["standard_containerized_verified"],
            "standard": coverage["standard_api_paths"],
        },
        "formats": formats,
        "ecosystems": ECOSYSTEMS,
        "cells": cells,
        "parsers": parsers,
        "standardTargets": standard_targets,
        "demos": demos,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    shutil.copyfile(SITE / "index.html", output / "index.html")
    shutil.copyfile(SITE / "favicon.svg", output / "favicon.svg")
    assets = output / "assets"
    assets.mkdir(exist_ok=True)
    for name in ("styles.css", "app.js"):
        shutil.copyfile(SITE / name, assets / name)
    print(f"Built {output}: {len(parsers)} verified paths, {len(cells)} cells, {len(manifests)} projects")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=SITE / "dist")
    args = parser.parse_args()
    build(args.output.resolve())
