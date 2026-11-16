#!/usr/bin/env python3
"""Build the static Parsarium site from committed catalog evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_projects import fully_runnable


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
RANKING_ALIASES = {
    ("cpp", "svg", "qtbase"): "QtBase QImageReader",
    ("cpp", "svg", "qtdeclarative"): "QtDeclarative VectorImage",
    ("java", "ascii_ply", "f3d"): "F3D Java binding",
    ("java", "ascii_ply", "kotlin-assimp"): "Kotlin-graphics Assimp",
    ("java", "ascii_ply", "imaging-mesh"): "AIST Imaging Mesh",
    ("java", "ascii_ply", "bteterrarenderer-draco"): "BTETerraRenderer Draco module",
}
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


def ranking_rows(path: Path) -> tuple[str, dict[str, tuple[str, str, str]]]:
    """Read the recorded within-cell metric without inferring missing values."""
    metric = "recorded adoption metric"
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        columns = [part.strip() for part in line.strip("|").split("|")]
        if len(columns) < 4:
            continue
        if columns[0] == "Rank":
            metric = columns[3]
            continue
        package = re.search(r"\[([^\]]+)\]\([^)]+\)", columns[1])
        if package and (columns[0].rstrip("=").isdigit() or columns[0] in {"unranked", "—"}):
            rank = "unranked" if columns[0] == "—" else columns[0]
            rows[package.group(1).casefold()] = (rank, columns[3], columns[2])
    return metric, rows


def build(output: Path) -> None:
    cells_source = read_json(ROOT / "data/cells.json")["cells"]
    coverage = read_json(ROOT / "data/projects-coverage.json")
    readme_items = read_json(ROOT / "data/parser-readmes.json")["parsers"]
    readmes = {(item["format"], item["ecosystem"], item["name"]): item
               for item in readme_items}
    if len(readmes) != coverage["catalog_paths"]:
        raise ValueError("parser guides do not match catalog path count")
    coverage_by_cell = {(c["format"], c["ecosystem"]): c for c in coverage["cells"]}
    manifests = {}
    standard_projects = {}
    for path in sorted((ROOT / "projects").glob("*/*/*/manifest.json")):
        manifest = read_json(path)
        key = (manifest["format"], manifest["ecosystem"], manifest["package"], manifest["release"])
        manifests[key] = (path, manifest)
        if manifest.get("kind") == "standard" and fully_runnable(path, manifest):
            standard_projects[(manifest["format"], manifest["ecosystem"], manifest["api"])] = path

    parsers = []
    cells = []
    for cell in cells_source:
        fmt, eco = cell["format"], cell["ecosystem"]
        source = f"data/{eco}/{fmt}/parsers.json"
        entries = read_json(ROOT / source)
        if len(entries) != cell["verified_third_party_count"]:
            raise ValueError(f"count mismatch in {source}")
        metric, ranks = ranking_rows(ROOT / f"data/{eco}/{fmt}/ranking.md")
        normalized_rows = defaultdict(list)
        rows_by_release = defaultdict(list)
        for ranking_name, ranked_row in ranks.items():
            normalized_rows[re.sub(r"[^a-z0-9]", "", ranking_name)].append(ranked_row)
            rows_by_release[ranked_row[2]].append(ranked_row)
        entry_release_counts = Counter(entry["version"] for entry in entries)

        def rank_for(entry):
            direct = ranks.get(entry["name"].casefold())
            if direct:
                return direct
            alias = RANKING_ALIASES.get((eco, fmt, entry["name"]))
            if alias and alias.casefold() in ranks:
                return ranks[alias.casefold()]
            normalized = normalized_rows[re.sub(r"[^a-z0-9]", "", entry["name"].casefold())]
            if len(normalized) == 1:
                return normalized[0]
            # Some ranking labels describe a binding rather than repeat the
            # catalog package name. An exact, unique release identifies it.
            same_release = rows_by_release[entry["version"]]
            if entry_release_counts[entry["version"]] == 1 and len(same_release) == 1:
                return same_release[0]
            return None
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
            "cellGuideUrl": repo_link(f"catalog/{fmt}/{eco}/README.md"),
            "standardProjectUrl": None,
        })
        entries = sorted(entries, key=lambda entry: (
            int(rank_for(entry)[0].rstrip("="))
            if rank_for(entry) and rank_for(entry)[0].rstrip("=").isdigit()
            else 100_000
        ))
        for entry in entries:
            key = (fmt, eco, entry["name"], entry["version"])
            guide = readmes[(fmt, eco, entry["name"])]
            project = manifests.get(key) if guide["runnable"] else None
            if (guide["runnable"] and project is None) or not (ROOT / guide["readme"]).is_file():
                raise ValueError(f"parser guide and harness disagree: {fmt}/{eco}/{entry['name']}")
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
                "guideUrl": repo_link(guide["readme"]),
                "rankingUrl": repo_link(f"data/{eco}/{fmt}/ranking.md"),
            }
            ranked = rank_for(entry)
            if ranked:
                record["rank"] = ranked[0]
                record["popularityMetric"] = metric
                record["metricValue"] = ranked[1]
            if project:
                project_path, _ = project
                record["project"] = str(project_path.parent.relative_to(ROOT))
                record["projectUrl"] = repo_link(str((project_path.parent / "README.md").relative_to(ROOT)))
                record["targetId"] = f"{fmt}/{eco}/{project_path.parent.name}"
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
    for (fmt, eco, _api), project_path in sorted(standard_projects.items()):
        manifest = read_json(project_path)
        inventory_path = ROOT / manifest["standard_inventory"]
        inventory = read_json(inventory_path)
        documented_api = next(
            (api for api in inventory["verified_apis"]
             if (api.get("api") or api.get("name") or api.get("input_api")) == manifest["api"]),
            None,
        )
        if documented_api is None:
            raise ValueError(f"standard API missing from inventory: {project_path}")
        official_documentation = documented_api.get("documentation") or documented_api.get("official_documentation")
        if isinstance(official_documentation, list):
            official_documentation = official_documentation[0] if official_documentation else None
        if not official_documentation:
            raise ValueError(f"standard API documentation missing: {project_path}")
        standard_targets.append({
            "type": "standard",
            "format": fmt,
            "ecosystem": eco,
            "name": manifest["package"],
            "version": manifest["release"],
            "scope": "format-aware runtime API",
            "family": manifest["runtime"],
            "inputApi": manifest["api"],
            "documentation": official_documentation,
            "evidenceUrl": repo_link(str(inventory_path.relative_to(ROOT))),
            "guideUrl": repo_link(str((project_path.parent / "README.md").relative_to(ROOT))),
            "projectUrl": repo_link(str((project_path.parent / "README.md").relative_to(ROOT))),
            "project": str(project_path.parent.relative_to(ROOT)),
            "targetId": f"{fmt}/{eco}/{project_path.parent.name}",
        })

    targets = {}
    for record in [*parsers, *standard_targets]:
        target_id = record.get("targetId")
        if not target_id:
            continue
        project_dir = ROOT / record["project"]
        manifest = read_json(project_dir / "manifest.json")
        verification = read_json(project_dir / "verification.json")
        control_path = ROOT / manifest["control"]
        fmt, eco, slug = target_id.split("/")
        target_args = f"{fmt} {eco} {slug}"
        run_dir = f"runs/{fmt}-{slug}"
        targets[target_id] = {
            "format": fmt,
            "ecosystem": eco,
            "package": manifest["package"],
            "release": manifest["release"],
            "inputApi": record["inputApi"],
            "control": manifest["control"],
            "controlUrl": repo_link(manifest["control"]),
            "bytes": control_path.stat().st_size,
            "expectedOutput": manifest["expected_output"],
            "coverageLines": verification["parser_source_lines_covered"],
            "coverageKind": verification.get("coverage_kind", "source_lines"),
            "coverageTuples": (verification.get("binary_feedback") or {}).get("control_tuples"),
            "coverageLimit": manifest.get("coverage_limit") or manifest.get("underlying_coverage_limitation") or (
                "AFL++ edge feedback is scoped to the pinned underlying shared library; source-line coverage is unavailable."
                if verification.get("coverage_kind") == "native_binary_edges" else None
            ),
            "projectGuideUrl": record["projectUrl"],
            "controlCommand": f"python3 parsarium.py run {target_args} {manifest['control']} --results {run_dir}-control",
            "inputCommand": f"python3 parsarium.py run {target_args} INPUT_FILE --results {run_dir}-single",
            "replayCommand": f"python3 parsarium.py replay {target_args} CORPUS_DIR {run_dir}-replay",
            "aflCommands": [
                f"python3 parsarium.py afl build {target_args}",
                f"python3 parsarium.py afl prepare {target_args} {run_dir}-afl",
                f"python3 parsarium.py afl run {run_dir}-afl --seconds 60",
            ],
        }
    if len(targets) != coverage["containerized_verified"] + coverage["standard_containerized_verified"]:
        raise ValueError("run walkthrough targets do not match project coverage")

    format_counts = Counter(p["format"] for p in parsers)
    format_runs = Counter()
    for cell in cells:
        format_runs[cell["format"]] += cell["runnable"]
    formats = [
        {"id": fmt, "label": label, "category": category, "description": description,
         "verified": format_counts[fmt], "runnable": format_runs[fmt],
         "guideUrl": repo_link(f"catalog/{fmt}/README.md")}
        for fmt, label, category, description in FORMATS
    ]

    demos = []
    controls_output = output / "controls"
    if controls_output.exists():
        shutil.rmtree(controls_output)
    for source in DEMO_PROJECTS:
        manifest = read_json(ROOT / source)
        verification = read_json(ROOT / Path(source).parent / "verification.json")
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
            "coverageLines": verification["parser_source_lines_covered"],
            "coverageKind": verification.get("coverage_kind", "source_lines"),
            "coverageTuples": (verification.get("binary_feedback") or {}).get("control_tuples"),
            "manifestUrl": repo_link(source),
            "projectGuideUrl": repo_link(str((ROOT / source).parent.relative_to(ROOT) / "README.md")),
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
        "targets": targets,
        "demos": demos,
    }
    output.mkdir(parents=True, exist_ok=True)
    catalog_json = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    (output / "catalog.json").write_text(catalog_json + "\n", encoding="utf-8")
    html = (SITE / "index.html").read_text(encoding="utf-8")
    marker = "<!-- CATALOG_DATA -->"
    if html.count(marker) != 1:
        raise ValueError("index.html must contain one catalog placeholder")
    # Keep the JSON from terminating its own script element if catalog text contains HTML.
    inline_json = catalog_json.replace("<", "\\u003c")
    html = html.replace(marker, f'<script id="catalog-data" type="application/json">{inline_json}</script>')
    html = html.replace("{{RUNNABLE}}", f"{catalog['summary']['runnable']:,}")
    html = html.replace("{{VERIFIED}}", f"{catalog['summary']['verified']:,}")
    (output / "index.html").write_text(html, encoding="utf-8")
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
