#!/usr/bin/env python3
"""Build the static Parsarium site from committed catalog evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_projects import fully_runnable


ROOT = Path(__file__).resolve().parents[1]
SITE = Path(__file__).resolve().parent
REPO_URL = "https://github.com/joszamama/parsarium"
CLOUDFLARE_BEACON_TOKEN = "768b709cb62a40f8a65bacc76109381b"

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
    "projects/png/c/libpng/manifest.json",
    "projects/zip/rust/zip/manifest.json",
    "projects/mp4/php/getid3/manifest.json",
    "projects/wav/c/dr_wav/manifest.json",
    "projects/pdf/java/pdfbox/manifest.json",
    "projects/svg/rust/usvg/manifest.json",
    "projects/http11/go/fasthttp/manifest.json",
    "projects/ascii_ply/python/plyfile/manifest.json",
    "projects/ascii_pnm/go/gopnm/manifest.json",
    "projects/mp3_id3v2/java/jaudiotagger/manifest.json",
]

# Each clue is searched in the exact pinned valid control used by the featured
# parser. The site shows real file bytes and a field from that parser's receipt.
LESSON_SPECS = {
    "png": {
        "needle": b"IHDR", "question": "What does the IHDR chunk describe?",
        "choices": ["Image dimensions and color mode", "Archive entries", "Audio sample rate"],
        "answer": 0, "explanation": "IHDR is a required PNG chunk. Its payload includes width, height, bit depth, and color type.",
        "question_es": "¿Qué describe el bloque IHDR?",
        "choices_es": ["Las dimensiones de la imagen y el modo de color", "Las entradas de un archivo comprimido", "La frecuencia de muestreo del audio"],
        "explanation_es": "IHDR es un bloque obligatorio de PNG. Sus datos incluyen el ancho, el alto, la profundidad de bits y el tipo de color.",
        "output_keys": ["width", "height"],
    },
    "zip": {
        "needle": b"PK\x01\x02", "question": "What does this ZIP record help a reader find?",
        "choices": ["A pixel color", "The archive entry table", "An HTTP host"],
        "answer": 1, "explanation": "The central directory records the archive's entries and where their local data lives.",
        "question_es": "¿Qué ayuda a encontrar este registro de ZIP?",
        "choices_es": ["El color de un píxel", "La tabla de entradas del archivo", "Un host HTTP"],
        "explanation_es": "El directorio central guarda las entradas del archivo y dónde están sus datos locales.",
        "output_keys": ["name", "size"],
    },
    "mp4": {
        "needle": b"moov", "question": "What lives in the moov box?",
        "choices": ["The PDF page tree", "A ZIP file name", "Track and timing metadata"],
        "answer": 2, "explanation": "MP4 is built from nested boxes. The moov box carries movie and track metadata used to interpret media.",
        "question_es": "¿Qué hay dentro de la caja moov?",
        "choices_es": ["El árbol de páginas de un PDF", "El nombre de un archivo ZIP", "Los metadatos de pistas y tiempos"],
        "explanation_es": "MP4 se construye con cajas anidadas. La caja moov lleva los metadatos de la película y de las pistas que se usan para interpretar el contenido.",
        "output_keys": ["width", "height", "video_fourcc"],
    },
    "wav": {
        "needle": b"fmt ", "question": "What does the fmt chunk tell a WAV reader?",
        "choices": ["Archive compression level", "Sample encoding and channel layout", "Page count"],
        "answer": 1, "explanation": "The fmt chunk describes how to interpret the sample data, including rate, channel count, and sample format.",
        "question_es": "¿Qué le dice el bloque fmt a un lector de WAV?",
        "choices_es": ["El nivel de compresión del archivo", "La codificación de las muestras y la disposición de canales", "El número de páginas"],
        "explanation_es": "El bloque fmt describe cómo interpretar las muestras: frecuencia, número de canales y formato de muestra.",
        "output_keys": ["sample_rate", "channels"],
    },
    "pdf": {
        "needle": b"/Count 1", "question": "What does /Count 1 say about this page tree?",
        "choices": ["The file has one byte", "There is one font", "One page is below this node"],
        "answer": 2, "explanation": "A PDF page tree uses /Count to report the number of descendant pages. The parser resolves that structure.",
        "question_es": "¿Qué dice /Count 1 sobre este árbol de páginas?",
        "choices_es": ["Que el archivo tiene un byte", "Que hay una fuente", "Que hay una página por debajo de este nodo"],
        "explanation_es": "Un árbol de páginas de PDF usa /Count para indicar cuántas páginas descienden de él. El parser resuelve esa estructura.",
        "output_keys": ["pages"],
    },
    "svg": {
        "needle": b'width="2" height="1"', "question": "What do these root SVG attributes set?",
        "choices": ["The ZIP entry size", "The viewport dimensions", "The HTTP body length"],
        "answer": 1, "explanation": "The SVG root gives the image dimensions; child elements then describe vector shapes inside that space.",
        "question_es": "¿Qué fijan estos atributos de la raíz SVG?",
        "choices_es": ["El tamaño de una entrada ZIP", "Las dimensiones del lienzo", "La longitud del cuerpo HTTP"],
        "explanation_es": "La raíz SVG da las dimensiones de la imagen; los elementos hijos describen las formas dentro de ese espacio.",
        "output_keys": ["width", "height", "nodes"],
    },
    "http11": {
        "needle": b"Host: example.test", "question": "What does this header identify?",
        "choices": ["The audio codec", "The image width", "The requested host"],
        "answer": 2, "explanation": "An HTTP/1.1 request has a start line and headers. Host identifies the server name requested by the client.",
        "question_es": "¿Qué identifica esta cabecera?",
        "choices_es": ["El códec de audio", "El ancho de la imagen", "El host al que se hace la petición"],
        "explanation_es": "Una petición HTTP/1.1 tiene una línea inicial y cabeceras. Host indica el nombre del servidor que pide el cliente.",
        "output_keys": ["method", "target", "host"],
    },
    "ascii_ply": {
        "needle": b"element vertex 3", "question": "What does this PLY header line declare?",
        "choices": ["Three pixels follow", "Three vertex records follow", "Three audio channels follow"],
        "answer": 1, "explanation": "An ASCII PLY header declares the record layout before the vertex and face lines are read.",
        "question_es": "¿Qué declara esta línea de la cabecera PLY?",
        "choices_es": ["Que vienen tres píxeles", "Que vienen tres registros de vértices", "Que vienen tres canales de audio"],
        "explanation_es": "Una cabecera PLY en ASCII declara la estructura de los registros antes de que se lean las líneas de vértices y caras.",
        "output_keys": ["vertex_count", "face_count"],
    },
    "ascii_pnm": {
        "needle": b"P3", "question": "What does the P3 magic number select?",
        "choices": ["A compressed PNG chunk", "An ID3 title frame", "ASCII RGB samples"],
        "answer": 2, "explanation": "P3 marks an ASCII color PNM image. The reader then uses dimensions, maximum value, and sample triples.",
        "question_es": "¿Qué selecciona el número mágico P3?",
        "choices_es": ["Un bloque PNG comprimido", "Una trama de título ID3", "Muestras RGB en ASCII"],
        "explanation_es": "P3 marca una imagen PNM en color y en ASCII. Después el lector usa las dimensiones, el valor máximo y los tríos de muestras.",
        "output_keys": ["width", "height", "rgb0"],
    },
    "mp3_id3v2": {
        "needle": b"TIT2", "question": "What does this ID3v2 frame contain?",
        "choices": ["The MP3 sample rate", "The track title", "The file length"],
        "answer": 1, "explanation": "TIT2 is the ID3v2 title frame. It lives in the tag before the audio frames in this control.",
        "question_es": "¿Qué contiene esta trama ID3v2?",
        "choices_es": ["La frecuencia de muestreo del MP3", "El título de la pista", "La longitud del archivo"],
        "explanation_es": "TIT2 es la trama de título de ID3v2. Está en la etiqueta, antes de las tramas de audio en este control.",
        "output_keys": ["title", "artist"],
    },
}


def lesson_for(fmt: str, data: bytes, expected_output: dict) -> dict:
    spec = LESSON_SPECS[fmt]
    needle = spec["needle"]
    offset = data.find(needle)
    if offset < 0 or data.find(needle, offset + 1) >= 0:
        raise ValueError(f"lesson clue must occur exactly once in {fmt} control")
    if any(key not in expected_output for key in spec["output_keys"]):
        raise ValueError(f"lesson output keys missing from {fmt} control receipt")
    start = max(0, offset - 7)
    end = min(len(data), offset + len(needle) + 7)
    return {
        "question": spec["question"],
        "choices": spec["choices"],
        "answer": spec["answer"],
        "explanation": spec["explanation"],
        "es": {"question": spec["question_es"], "choices": spec["choices_es"],
               "explanation": spec["explanation_es"]},
        "output": {key: expected_output[key] for key in spec["output_keys"]},
        "clueOffset": offset,
        "clueLength": len(needle),
        "previewStart": start,
        "tokens": [{"hex": f"{byte:02X}", "ascii": chr(byte) if 32 <= byte < 127 else "·",
                    "focus": offset <= position < offset + len(needle)}
                   for position, byte in enumerate(data[start:end], start)],
    }


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
        afl_receipt_path = ROOT / "fuzzing/afl-native" / target_id / "verification.json"
        afl_receipt = read_json(afl_receipt_path) if afl_receipt_path.is_file() else {}
        targets[target_id] = {
            "format": fmt,
            "ecosystem": eco,
            "slug": slug,
            "type": record.get("type", "package"),
            "package": manifest["package"],
            "release": manifest["release"],
            "family": record["family"],
            "rank": record.get("rank"),
            "verifiedAt": verification.get("verified_at_utc"),
            "aflFeedback": afl_receipt.get("feedback_kind") or (
                "compiled_parser_edges" if afl_receipt.get("pass") else None),
            "aflEdges": afl_receipt.get("feedback_edges"),
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
        if parser_record is None or not parser_record.get("targetId"):
            raise ValueError(f"demo target is not fully runnable: {source}")
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
            "lesson": lesson_for(fmt, data, manifest["expected_output"]),
            "hex": data[:384].hex(),
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

    families = {(p["format"], p["family"]) for p in parsers}
    afl_overlays = sum(1 for t in targets.values() if t["aflFeedback"])
    catalog = {
        "summary": {
            "verified": len(parsers),
            "cells": len(cells),
            "formats": len(FORMATS),
            "ecosystems": len(ECOSYSTEMS),
            "runnable": coverage["containerized_verified"] + coverage["standard_containerized_verified"],
            "standard": coverage["standard_api_paths"],
            "families": len(families),
            "aflOverlays": afl_overlays,
        },
        "commit": build_commit(),
        "formats": formats,
        "ecosystems": ECOSYSTEMS,
        "cells": cells,
        "parsers": parsers,
        "standardTargets": standard_targets,
        "targets": targets,
    }
    output.mkdir(parents=True, exist_ok=True)
    catalog_json = json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
    (output / "catalog.json").write_text(catalog_json + "\n", encoding="utf-8")
    manual_data = {"demos": [{k: v for k, v in demo.items() if k != "aflCommands"} for demo in demos]}
    (output / "manual.json").write_text(
        json.dumps(manual_data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    (output / "CNAME").write_text("parsarium.com\n", encoding="utf-8")

    render_site(output, catalog, targets, demos)
    print(f"Built {output}: {len(parsers)} verified paths, {len(cells)} cells, "
          f"{len(manifests)} projects, {len(families)} families")


# --------------------------------------------------------------------------
# Rendering

ECO_LABELS = {"c": "C", "cpp": "C++", "go": "Go", "java": "Java", "javascript": "JavaScript",
              "python": "Python", "rust": "Rust", "php": "PHP"}

NAV = {
    "en": [("bench", "Bench"), ("atlas", "Atlas"), ("manual", "Manual"), ("about", "About")],
    "es": [("bench", "Banco"), ("atlas", "Atlas"), ("manual", "Manual"), ("about", "Acerca de")],
}

STRINGS = {
    "en": {
        "skip": "Skip to content", "home": "Parsarium home", "menu": "Menu",
        "nav": "Main navigation", "switch": "Versión en español",
        "readers_title": "Programs that read red-green.png",
        "regions": {"sig": "signature", "IHDR": "IHDR · size and colour type",
                    "IDAT": "IDAT · compressed pixels", "IEND": "IEND · end of image"},
        "verified": "verified", "runnable": "runnable",
        "footer_cite": "Cite Parsarium",
        "footer_line": "An open testbed of real parsers, by Pepe Zamudio at CISPA.",
        "built": "Built from commit", "chapter": "Chapter", "prev": "Previous", "next": "Next",
        "contents": "Contents", "redirect": "This page moved to",
        "day_label": "harness receipts",
        "min_read": "min read", "questions": "quiz questions", "exercises": "exercises",
        "glossary": "Glossary",
    },
    "es": {
        "skip": "Saltar al contenido", "home": "Inicio de Parsarium", "menu": "Menú",
        "nav": "Navegación principal", "switch": "English version",
        "readers_title": "Programas que leen red-green.png",
        "regions": {"sig": "firma", "IHDR": "IHDR · tamaño y tipo de color",
                    "IDAT": "IDAT · píxeles comprimidos", "IEND": "IEND · fin de la imagen"},
        "verified": "verificados", "runnable": "ejecutables",
        "footer_cite": "Citar Parsarium",
        "footer_line": "Un banco de pruebas abierto con parsers reales, por Pepe Zamudio en CISPA.",
        "built": "Construido desde el commit", "chapter": "Capítulo", "prev": "Anterior", "next": "Siguiente",
        "contents": "Índice", "redirect": "Esta página se ha movido a",
        "day_label": "registros de harness",
        "min_read": "min de lectura", "questions": "preguntas", "exercises": "ejercicios",
        "glossary": "Glosario",
    },
}

GLOSSARY_SUMMARY = {
    "en": "The terms used in this manual, in one place.",
    "es": "Los términos de este manual, en un solo sitio.",
}

MANUAL = [
    "what-a-parser-is",
    "formats-and-grammars",
    "controls-and-receipts",
    "choosing-targets",
    "coverage-feedback",
    "differential-testing",
    "fuzzing-at-scale",
    "triage-and-disclosure",
    "designing-an-experiment",
]


def build_commit() -> str:
    sha = os.environ.get("GITHUB_SHA")
    if sha:
        return sha[:8]
    try:
        return subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def png_regions(data: bytes) -> list[tuple[int, int, str]]:
    regions = [(0, 8, "sig")]
    position = 8
    while position + 8 <= len(data):
        length = int.from_bytes(data[position:position + 4], "big")
        kind = data[position + 4:position + 8].decode("latin-1")
        end = position + 12 + length
        regions.append((position, end, kind))
        position = end
    return regions


def hexdump_html(data: bytes, regions: list[tuple[int, int, str]]) -> str:
    def region_of(i):
        for start, end, kind in regions:
            if start <= i < end:
                return kind
        return ""
    rows = []
    for offset in range(0, len(data), 16):
        chunk = data[offset:offset + 16]
        cells = []
        chars = []
        for i, byte in enumerate(chunk, offset):
            kind = region_of(i)
            cells.append(f'<span class="b r-{kind}" data-r="{kind}">{byte:02x}</span>')
            ch = chr(byte) if 32 <= byte < 127 else "·"
            chars.append(f'<span class="r-{kind}" data-r="{kind}">{html.escape(ch)}</span>')
        pad = '<span class="b pad"></span>' * (16 - len(chunk))
        rows.append(f'<div class="hx-row"><span class="hx-off">{offset:08x}</span>'
                    f'<span class="hx-bytes">{"".join(cells)}{pad}</span>'
                    f'<span class="hx-ascii">{"".join(chars)}</span></div>')
    return "".join(rows)


def output_summary(expected: dict) -> str:
    if "width" in expected and "height" in expected:
        return f'width {expected["width"]} · height {expected["height"]}'
    keys = list(expected)[:2]
    return " · ".join(f"{k} {json.dumps(expected[k])}" for k in keys)


def render_site(output: Path, catalog: dict, targets: dict, demos: list) -> None:
    summary = catalog["summary"]
    commit = catalog["commit"]
    built_on = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Home hero: the PNG control and every target that reads it.
    hero_control = "controls/png/red-green.png"
    hero_bytes = (ROOT / hero_control).read_bytes()
    readers = sorted((t for t in targets.values() if t["control"] == hero_control),
                     key=lambda t: (ECOSYSTEMS.index(t["ecosystem"]), t["package"].casefold()))

    def readers_html() -> str:
        items = []
        for t in readers:
            items.append(
                f'<li><span class="rd-eco">{ECO_LABELS[t["ecosystem"]]}</span>'
                f'<span class="rd-pkg">{html.escape(t["package"])} <i>{html.escape(t["release"])}</i></span>'
                f'<span class="rd-out">{html.escape(output_summary(t["expectedOutput"]))}</span></li>')
        return "".join(items)

    def legend_html(lang: str) -> str:
        labels = STRINGS[lang]["regions"]
        return "".join(f'<li data-r="{k}"><span class="sw r-{k}"></span>{v}</li>'
                       for k, v in labels.items())

    # Format strip: the first bytes of each format's most-used control.
    def format_strip(lang: str) -> str:
        rows = []
        for fmt in catalog["formats"]:
            controls = Counter(t["control"] for t in targets.values() if t["format"] == fmt["id"])
            control = controls.most_common(1)[0][0]
            head = (ROOT / control).read_bytes()[:8]
            hexes = " ".join(f"{b:02x}" for b in head)
            ascii_ = html.escape("".join(chr(b) if 32 <= b < 127 else "·" for b in head))
            rows.append(
                f'<a class="fmt-row" href="{{{{ROOT}}}}atlas/?format={fmt["id"]}">'
                f'<span class="fmt-name">{fmt["label"]}</span>'
                f'<span class="fmt-hex">{hexes}</span><span class="fmt-ascii">{ascii_}</span>'
                f'<span class="fmt-file">{html.escape(Path(control).name)}</span>'
                f'<span class="fmt-num"><b>{fmt["runnable"]}</b> {STRINGS[lang]["runnable"]}</span></a>')
        return "".join(rows)

    # Receipt timeline: harness verifications per day.
    per_day = Counter((t["verifiedAt"] or "")[:10] for t in targets.values() if t["verifiedAt"])
    days = sorted(per_day)
    latest = sorted((t for t in targets.values() if t["verifiedAt"]),
                    key=lambda t: t["verifiedAt"], reverse=True)[:8]

    def receipts_html(lang: str) -> str:
        if not days:
            return ""
        peak = max(per_day.values())
        bars = []
        for day in days:
            height = max(4, round(120 * per_day[day] / peak))
            bars.append(f'<li><span class="bar" style="--h:{height}px"></span>'
                        f'<b>{per_day[day]}</b><time datetime="{day}">{day[5:]}</time></li>')
        recent = "".join(
            f'<li><time>{t["verifiedAt"][:16].replace("T", " ")}</time>'
            f'<code>{t["format"]}/{t["ecosystem"]}/{html.escape(t["slug"])}</code>'
            f'<span>{html.escape(t["package"])} {html.escape(t["release"])}</span></li>' for t in latest)
        return (f'<ol class="days" aria-label="{STRINGS[lang]["day_label"]}">{"".join(bars)}</ol>'
                f'<ol class="recent">{recent}</ol>')

    def chapter_meta(lang: str, slug: str) -> dict:
        source = (SITE / "manual" / lang / f"{slug}.html").read_text(encoding="utf-8")
        match = re.match(r"<!--\s*(\{.*?\})\s*-->", source, re.S)
        if not match:
            raise ValueError(f"manual chapter needs a meta comment: {lang}/{slug}")
        meta = json.loads(match.group(1))
        meta["body"] = source[match.end():]
        return meta

    def manual_toc(lang: str, root: str, current: str | None = None) -> str:
        items = []
        for number, slug in enumerate(MANUAL, 1):
            meta = chapter_meta(lang, slug)
            mark = ' aria-current="page"' if slug == current else ""
            exercises = meta["body"].count('<div class="exercise"')
            items.append(f'<li><a href="{root}manual/{slug}/"{mark} data-slug="{slug}" data-ex="{exercises}"><span class="toc-n">{number:02d}</span>'
                         f'<span class="toc-t">{html.escape(meta["title"])}</span>'
                         f'<span class="toc-s">{html.escape(meta["summary"])}</span></a></li>')
        gloss = ' aria-current="page"' if current == "glossary" else ""
        items.append(f'<li><a href="{root}manual/glossary/"{gloss}><span class="toc-n">A</span>'
                     f'<span class="toc-t">{STRINGS[lang]["glossary"]}</span>'
                     f'<span class="toc-s">{GLOSSARY_SUMMARY[lang]}</span></a></li>')
        return f'<ol class="toc">{"".join(items)}</ol>'

    def header(lang: str, root: str, asset_root: str, active: str, route: str) -> str:
        s = STRINGS[lang]
        links = "".join(
            f'<a href="{root}{key}/"{" aria-current=page" if key == active else ""}>{label}</a>'
            for key, label in NAV[lang])
        other = "es" if lang == "en" else "en"
        other_url = f"{asset_root}es/{route}" if lang == "en" else f"{asset_root}{route}"
        return f'''<a class="skip" href="#main">{s["skip"]}</a>
<header class="masthead"><div class="wrap mh">
  <a class="brand" href="{root or './'}" aria-label="{s["home"]}"><span class="px" aria-hidden="true"><i></i><i></i></span>parsarium</a>
  <nav class="nav" id="nav" aria-label="{s["nav"]}">{links}
    <a class="lang" href="{other_url}" hreflang="{other}" lang="{other}" aria-label="{s["switch"]}">{other.upper()}</a>
    <a class="gh" href="{REPO_URL}" rel="noopener">GitHub</a></nav>
  <button class="menu" type="button" aria-expanded="false" aria-controls="nav">{s["menu"]}</button>
</div></header>'''

    def footer(lang: str, root: str) -> str:
        s = STRINGS[lang]
        return f'''<footer class="foot"><div class="wrap ft">
  <p class="ft-line"><span class="px" aria-hidden="true"><i></i><i></i></span>{s["footer_line"]}</p>
  <p class="ft-meta">{s["built"]} <a href="{REPO_URL}/commit/{commit}"><code>{commit}</code></a> · {built_on} ·
    <a href="{root}about/#cite">{s["footer_cite"]}</a> · <a href="{REPO_URL}">github.com/joszamama/parsarium</a></p>
</div></footer>'''

    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600'
             '&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap">')
    beacon = ("<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
              f"data-cf-beacon='{{\"token\": \"{CLOUDFLARE_BEACON_TOKEN}\"}}'></script>")

    def page(lang: str, route: str, active: str, title: str, description: str, body: str,
             scripts: tuple[str, ...] = ()) -> None:
        depth = route.count("/")
        root = "../" * depth
        asset_root = root + ("../" if lang == "es" else "")
        canonical_en = f"https://parsarium.com/{route}"
        canonical_es = f"https://parsarium.com/es/{route}"
        script_tags = "".join(f'<script src="{asset_root}assets/{name}" defer></script>'
                              for name in ("site.js", *scripts))
        document = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(description)}">
<meta name="theme-color" content="#f3f0e8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14130f" media="(prefers-color-scheme: dark)">
<title>{html.escape(title)}</title>
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" type="image/svg+xml" href="{asset_root}favicon.svg">
{fonts}
<link rel="stylesheet" href="{asset_root}assets/styles.css">
<link rel="canonical" href="{canonical_es if lang == "es" else canonical_en}">
<link rel="alternate" hreflang="en" href="{canonical_en}">
<link rel="alternate" hreflang="es" href="{canonical_es}">
<link rel="alternate" hreflang="x-default" href="{canonical_en}">
</head>
<body data-page="{active}" data-root="{asset_root}" data-locale-root="{root}" data-lang="{lang}" data-commit="{commit}">
{header(lang, root, asset_root, active, route)}
<main id="main">
{body}
</main>
{footer(lang, root)}
{script_tags}
{beacon}
</body>
</html>
'''
        document = document.replace("{{ROOT}}", root).replace("{{ASSET_ROOT}}", asset_root)
        leftover = re.findall(r"\{\{[A-Z_]+\}\}", document)
        if leftover:
            raise ValueError(f"unreplaced placeholders in {lang}/{route}: {sorted(set(leftover))}")
        destination = output / ("es" if lang == "es" else "") / route
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "index.html").write_text(document, encoding="utf-8")

    def redirect(lang: str, route: str, target: str) -> None:
        depth = route.count("/")
        root = "../" * depth
        url = f"{root}{target}"
        destination = output / ("es" if lang == "es" else "") / route
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "index.html").write_text(
            f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={url}"><link rel="canonical" href="https://parsarium.com/'
            f'{"es/" if lang == "es" else ""}{target}"><title>Parsarium</title></head>'
            f'<body><p>{STRINGS[lang]["redirect"]} <a href="{url}">{url}</a>.</p></body></html>\n',
            encoding="utf-8")

    def fill(template: str, lang: str) -> str:
        def num(value: int) -> str:
            text = f"{value:,}"
            return text.replace(",", ".") if lang == "es" else text
        values = {
            "VERIFIED": num(summary['verified']),
            "RUNNABLE": num(summary['runnable']),
            "FAMILIES": num(summary['families']),
            "AFL": num(summary['aflOverlays']),
            "STANDARD": num(summary['standard']),
            "READERS_COUNT": str(len(readers)),
            "HERO_BYTES": str(len(hero_bytes)),
            "HEXDUMP": hexdump_html(hero_bytes, png_regions(hero_bytes)),
            "LEGEND": legend_html(lang),
            "READERS": readers_html(),
            "FORMAT_STRIP": format_strip(lang),
            "RECEIPTS": receipts_html(lang),
            "RECEIPT_DAYS": str(len(days)),
            "COMMIT": commit,
            "BUILT_ON": built_on,
            "YEAR": built_on[:4],
        }
        for key, value in values.items():
            template = template.replace("{{" + key + "}}", value)
        return template

    page_scripts = {"index": ("home.js",), "bench": ("bench.js",), "atlas": ("atlas.js",),
                    "manual": (), "glossary": (), "about": ()}
    for lang in ("en", "es"):
        for name, route in (("index", ""), ("bench", "bench/"), ("atlas", "atlas/"),
                            ("manual", "manual/"), ("glossary", "manual/glossary/"), ("about", "about/")):
            source = (SITE / "pages" / lang / f"{name}.html").read_text(encoding="utf-8")
            match = re.match(r"<!--\s*(\{.*?\})\s*-->", source, re.S)
            if not match:
                raise ValueError(f"page needs a meta comment: {lang}/{name}")
            meta = json.loads(match.group(1))
            body = fill(source[match.end():], lang).replace("{{MANUAL_TOC}}", manual_toc(lang, "../" * route.count("/")))
            page(lang, route, "manual" if name == "glossary" else name, meta["title"], meta["description"],
                 body, page_scripts[name])
        for number, slug in enumerate(MANUAL, 1):
            meta = chapter_meta(lang, slug)
            route = f"manual/{slug}/"
            root = "../../"
            prev_slug = MANUAL[number - 2] if number > 1 else None
            next_slug = MANUAL[number] if number < len(MANUAL) else None
            s = STRINGS[lang]
            pager = '<nav class="pager">'
            if prev_slug:
                pager += (f'<a class="prev" href="{root}manual/{prev_slug}/"><span>{s["prev"]}</span>'
                          f'{html.escape(chapter_meta(lang, prev_slug)["title"])}</a>')
            if next_slug:
                pager += (f'<a class="next" href="{root}manual/{next_slug}/"><span>{s["next"]}</span>'
                          f'{html.escape(chapter_meta(lang, next_slug)["title"])}</a>')
            pager += "</nav>"
            words = len(re.sub(r"<pre.*?</pre>|<[^>]+>", " ", meta["body"], flags=re.S).split())
            minutes = max(1, round(words / 200))
            questions = meta["body"].count('<div class="q"')
            exercises = meta["body"].count('<div class="exercise"')
            body = f'''<div class="wrap chapter">
  <aside class="chapter-side"><p class="label">{s["contents"]}</p>{manual_toc(lang, root, slug)}</aside>
  <article class="prose" data-slug="{slug}">
    <header class="chapter-head"><p class="label">{s["chapter"]} {number:02d}</p>
      <h1>{html.escape(meta["title"])}</h1><p class="dek">{html.escape(meta["summary"])}</p>
      <p class="chapter-meta"><span>{minutes} {s["min_read"]}</span><span>{questions} {s["questions"]}</span><span>{exercises} {s["exercises"]}</span></p></header>
    {fill(meta["body"], lang)}
    {pager}
  </article>
</div>'''
            page(lang, route, "manual", f'{meta["title"]} — ' + ("manual de Parsarium" if lang == "es" else "Parsarium manual"), meta["summary"], body,
                 ("manual.js",))
        for old, new in (("run/", "bench/"), ("lab/", "manual/"), ("why/", "about/")):
            redirect(lang, old, new)

    shutil.copyfile(SITE / "favicon.svg", output / "favicon.svg")
    assets = output / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir()
    for name in ("styles.css", "site.js", "home.js", "bench.js", "atlas.js", "manual.js"):
        shutil.copyfile(SITE / "assets" / name, assets / name)
    routes = ["", "bench/", "atlas/", "manual/", "manual/glossary/", "about/", *(f"manual/{slug}/" for slug in MANUAL)]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for route in routes:
        sitemap.extend((f"  <url><loc>https://parsarium.com/{route}</loc></url>",
                        f"  <url><loc>https://parsarium.com/es/{route}</loc></url>"))
    sitemap.append("</urlset>")
    (output / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=SITE / "dist")
    args = parser.parse_args()
    build(args.output.resolve())
