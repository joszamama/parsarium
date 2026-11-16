"""Build concise format and per-parser READMEs from committed evidence."""

import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import re

from audit_projects import (browser_control_verified, native_source_control_verified,
                            macos_host_control_verified, fully_runnable)


ROOT = Path(__file__).resolve().parents[1]
FORMATS = {
    "png": ("PNG", "Chunked raster image"),
    "zip": ("ZIP", "Archive with a central directory"),
    "mp4": ("MP4", "ISO base media container"),
    "wav": ("WAV", "RIFF audio container"),
    "pdf": ("PDF", "Page and object document"),
    "svg": ("SVG", "XML vector image"),
    "http11": ("HTTP/1.1", "Text request and response protocol"),
    "ascii_ply": ("ASCII PLY", "Text mesh geometry"),
    "ascii_pnm": ("ASCII PNM", "Text portable image"),
    "mp3_id3v2": ("MP3 with ID3v2", "Audio with an ID3v2 tag"),
}
ECOSYSTEMS = ("c", "cpp", "go", "java", "javascript", "python", "rust", "php")
ECO_LABEL = {"c": "C", "cpp": "C++", "go": "Go", "java": "Java",
             "javascript": "JavaScript", "python": "Python", "rust": "Rust", "php": "PHP"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def link(directory: Path, target: Path) -> str:
    return os.path.relpath(target, directory).replace(os.sep, "/")


def label(value: str) -> str:
    return value.replace("[", "\\[").replace("]", "\\]").replace("|", "\\|")


def slug(name: str, collisions: Counter) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "parser"
    return base + ("-" + sha256(name.encode()).hexdigest()[:8] if collisions[base] > 1 else "")


def verified_result(entry: dict, verification: dict) -> tuple[str | None, object | None]:
    records = verification.get("third_party", verification.get("results", []))
    record = next((item for item in records if item.get("package") == entry["name"]
                   and item.get("version") == entry["version"]), None)
    if "expected_output" in entry:
        output = entry["expected_output"]
    elif record and record.get("pass") is True:
        output = record.get("output")
    else:
        output = None
    control = entry.get("control") or (record or {}).get("control") or verification.get("control")
    if (control is None or not str(control).startswith("controls/")) and verification.get("controls"):
        controls = verification["controls"]
        if isinstance(controls, dict):
            first_key, first_value = next(iter(controls.items()))
            control = first_key if first_key.startswith("controls/") else first_value
        else:
            control = controls[0]["path"]
    return control, output


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--check", action="store_true", help="check generated files without writing")
    args = cli.parse_args()
    manifest_paths = sorted((ROOT / "projects").glob("*/*/*/manifest.json"))
    projects = {}
    standard_projects = {}
    staged_browser_projects = {}
    staged_native_source_projects = {}
    staged_macos_projects = {}
    project_guides = 0
    for path in manifest_paths:
        manifest = read(path)
        if manifest.get("kind") == "standard" and browser_control_verified(path, manifest):
            staged_browser_projects[(manifest["format"], manifest["ecosystem"], manifest["api"])] = path
        if manifest.get("kind") == "standard" and native_source_control_verified(path, manifest):
            staged_native_source_projects[(manifest["format"], manifest["ecosystem"], manifest["api"])] = path
        if not fully_runnable(path, manifest):
            continue
        project_guides += 1
        if manifest.get("kind") == "standard":
            standard_projects[(manifest["format"], manifest["ecosystem"], manifest["api"])] = path
            continue
        key = (manifest["format"], manifest["ecosystem"], manifest["package"])
        if key in projects:
            raise ValueError(f"duplicate project path: {key}")
        projects[key] = (path, manifest)
    for path in sorted((ROOT / "projects").glob("*/*/*/macos-manifest.json")):
        manifest = read(path)
        if not macos_host_control_verified(path, manifest):
            raise ValueError(f"host-only control receipt mismatch: {path}")
        staged_macos_projects[(manifest["format"], manifest["ecosystem"], manifest["api"])] = path
    generated: dict[Path, str] = {}
    index = []
    standard_count = 0
    coverage = read(ROOT / "data/projects-coverage.json")
    by_cell = {(cell["format"], cell["ecosystem"]): cell for cell in coverage["cells"]}

    for fmt, (format_label, description) in FORMATS.items():
        format_rows = []
        format_projects = []
        for eco in ECOSYSTEMS:
            source = ROOT / "data" / eco / fmt
            entries = read(source / "parsers.json")
            verification = read(source / "verification.json")
            bases = Counter(re.sub(r"[^a-z0-9]+", "-", entry["name"].lower()).strip("-") or "parser"
                            for entry in entries)
            cell_dir = ROOT / "catalog" / fmt / eco
            cell_rows = []
            standard_rows = []
            for entry in entries:
                name = entry["name"]
                item_dir = cell_dir / slug(name, bases)
                readme = item_dir / "README.md"
                project = projects.get((fmt, eco, name))
                ready = bool(project and fully_runnable(project[0], project[1]))
                if project and project[1]["release"] != entry["version"]:
                    raise ValueError(f"release mismatch in {project[0]}")
                control, output = verified_result(entry, verification)
                if not control or output is None:
                    raise ValueError(f"missing control result: {fmt}/{eco}/{name}")
                if not (ROOT / control).is_file():
                    raise ValueError(f"missing control file: {control}")
                lines = [f"# {name} — {format_label} / {ECO_LABEL[eco]}", "",
                         f"- **Pinned release:** `{entry['version']}`",
                         f"- **License:** {entry['license']}",
                         f"- **Parsed scope:** {entry['scope']}",
                         f"- **Underlying family:** {entry['family']}",
                         f"- **Local input API:** `{entry['input_api']}`",
                         f"- **Documentation:** [API reference](<{entry['documentation']}>)",
                         f"- **Catalog evidence:** [parser record]({link(item_dir, source / 'parsers.json')}) · "
                         f"[control verification]({link(item_dir, source / 'verification.json')}) · "
                         f"[within-ecosystem ranking]({link(item_dir, source / 'ranking.md')})",
                         f"- **Valid control:** [`{control}`]({link(item_dir, ROOT / control)})", "",
                         "## Observed control result", "", "```json",
                         json.dumps(output, indent=2, ensure_ascii=False), "```", ""]
                if entry.get("family_note"):
                    lines += [entry["family_note"], ""]
                if ready:
                    project_path, manifest = project
                    project_dir = project_path.parent
                    lines += ["## Run this target", "",
                              f"[Docker harness and verification receipt]({link(item_dir, project_dir / 'README.md')})", "", "```sh",
                              f"python3 parsarium.py build {fmt} {eco} {project_dir.name}",
                              f"python3 parsarium.py run {fmt} {eco} {project_dir.name} {control}",
                              "```", ""]
                    if manifest.get("coverage_limit"):
                        lines += [f"**Coverage limit:** {manifest['coverage_limit']}", ""]
                    format_projects.append((eco, name, project_dir))
                else:
                    lines += ["## Runnable harness", "",
                              "A Docker harness with parser-source coverage has not yet been verified for this API path.", ""]
                generated[readme] = "\n".join(lines)
                index.append({"format": fmt, "ecosystem": eco, "name": name,
                              "readme": str(readme.relative_to(ROOT)), "runnable": ready})
                cell_rows.append(f"- [{label(name)}]({link(cell_dir, readme)}) — "
                                 f"{'Docker harness ready' if ready else 'verified API path'}")
            inventory = read(source / "standard.json")
            standard_entries = inventory["verified_apis"]
            standard_bases = Counter(re.sub(r"[^a-z0-9]+", "-", (item.get("name") or item.get("api") or "api").lower()).strip("-") or "api"
                                     for item in standard_entries)
            for item in standard_entries:
                api_name = item.get("name") or item.get("api")
                if not api_name:
                    raise ValueError(f"unnamed standard API: {source}")
                standard_count += 1
                item_dir = cell_dir / "standard" / slug(api_name, standard_bases)
                readme = item_dir / "README.md"
                docs = item.get("documentation") or item.get("official_documentation")
                doc_urls = [docs] if isinstance(docs, str) else docs or []
                if not doc_urls:
                    raise ValueError(f"missing standard API documentation: {source}/{api_name}")
                control = item["control"]
                if not (ROOT / control).is_file():
                    raise ValueError(f"missing standard API control: {control}")
                output = (item.get("expected") or item.get("expected_output") or
                          (item.get("result") if isinstance(item.get("result"), dict) else None))
                lines = [f"# {api_name} — {format_label} / {ECO_LABEL[eco]}", "",
                         f"- **Runtime:** {item.get('runtime') or inventory.get('runtime') or inventory['ecosystem']}",
                         f"- **Input API:** `{item.get('input_api') or item.get('api') or api_name}`",
                         f"- **Official documentation:** " + " · ".join(f"[reference]({url})" for url in doc_urls),
                         f"- **Valid control:** [`{control}`]({link(item_dir, ROOT / control)})",
                         f"- **Inventory and verification:** [standard API record]({link(item_dir, source / 'standard.json')}) · "
                         f"[saved result]({link(item_dir, source / 'verification.json')})", ""]
                if item.get("family"):
                    lines += [f"**Parser family:** {item['family']}", ""]
                if output is not None:
                    lines += ["## Observed control result", "", "```json",
                              json.dumps(output, indent=2, ensure_ascii=False), "```", ""]
                elif item.get("observable_result"):
                    lines += ["## Observed control result", "", item["observable_result"], ""]
                else:
                    lines += ["## Observed control result", "",
                              "See the linked saved verification record for this API.", ""]
                if item.get("adapter"):
                    lines += [f"[Control adapter]({link(item_dir, ROOT / item['adapter'])})", ""]
                standard_project = standard_projects.get((fmt, eco, item.get("api")))
                if standard_project and fully_runnable(standard_project, read(standard_project)):
                    slug_name = standard_project.parent.name
                    format_projects.append((eco, api_name, standard_project.parent))
                    lines += ["## Run this target", "", "```sh",
                              f"python3 parsarium.py build {fmt} {eco} {slug_name}",
                              f"python3 parsarium.py run {fmt} {eco} {slug_name} {control}", "```", ""]
                elif staged := staged_browser_projects.get((fmt, eco, item.get("api"))):
                    lines += ["## Run the valid control", "",
                              f"[Browser container and control receipt]({link(item_dir, staged.parent / 'README.md')})", "",
                              "```sh",
                              f"python3 {staged.parent.relative_to(ROOT)}/verify-control.py",
                              "```", "",
                              "The browser runs this control, but its native parser source coverage and "
                              "AFL++ parser feedback are unavailable. This path remains staged.", ""]
                elif staged := staged_native_source_projects.get((fmt, eco, item.get("api"))):
                    lines += ["## Run this control", "",
                              f"[Docker harness and control receipt]({link(item_dir, staged.parent / 'README.md')})", "",
                              "```sh",
                              f"python3 {staged.parent.relative_to(ROOT)}/verify-control.py",
                              "```", "",
                              "Tk's native PNG reader has measured source coverage on this control. "
                              "AFL++ parser feedback is unavailable, so this path remains staged.", ""]
                elif staged := staged_macos_projects.get((fmt, eco, item.get("api") or item.get("name"))):
                    lines += ["## Run this macOS control", "",
                              f"[Host harness and control receipt]({link(item_dir, staged.parent / 'README.md')})", "",
                              "```sh",
                              f"python3 {staged.parent.relative_to(ROOT)}/verify-control.py",
                              "```", "",
                              "Core Graphics runs on macOS. Its parser source and AFL++ feedback are "
                              "unavailable, so this path remains staged.", ""]
                else:
                    lines += ["## Runnable harness", "",
                              "A Docker harness with parser-source coverage has not yet been verified for this API path.", ""]
                generated[readme] = "\n".join(lines)
                standard_rows.append(f"- [{label(api_name)}]({link(cell_dir, readme)})")
            cell_count = by_cell[(fmt, eco)]
            format_rows.append(f"| [{ECO_LABEL[eco]}]({link(ROOT / 'catalog' / fmt, cell_dir / 'README.md')}) "
                               f"| {len(entries)} | {cell_count['containerized_verified']} |")
            generated[cell_dir / "README.md"] = "\n".join(
                [f"# {format_label} / {ECO_LABEL[eco]}", "",
                 f"{len(entries)} verified third-party API paths; "
                 f"{cell_count['containerized_verified']} have verified Docker harnesses.", "",
                 f"[Ranking and search limits]({link(cell_dir, source / 'ranking.md')}) · "
                 f"[standard API inventory]({link(cell_dir, source / 'standard.json')})", "",
                 "## Third-party parsers", "", *cell_rows, "",
                 "## Standard and runtime APIs", "", *(standard_rows or ["None documented in this inventory."]), ""])
        format_dir = ROOT / "catalog" / fmt
        generated[format_dir / "README.md"] = "\n".join(
            [f"# {format_label}", "", description + ".", "",
             f"The catalog records {sum(by_cell[(fmt, eco)]['catalog_paths'] for eco in ECOSYSTEMS)} "
             "verified third-party API paths across eight ecosystems. Each parser page names its "
             "pinned release, documented input API, valid control, observed result, family, and harness status.", "",
             "| Ecosystem | Verified paths | Docker harnesses |", "| --- | ---: | ---: |",
             *format_rows, "", "[Harness instructions](../../projects/README.md)", ""])
        project_format_dir = ROOT / "projects" / fmt
        project_rows = [f"- [{label(name)} / {ECO_LABEL[eco]}]({link(project_format_dir, path / 'README.md')})"
                        for eco, name, path in sorted(format_projects)]
        generated[project_format_dir / "README.md"] = "\n".join(
            [f"# {format_label} runnable targets", "",
             f"[Browse every verified {format_label} parser]({link(project_format_dir, format_dir / 'README.md')}). "
             "The targets below have pinned Docker builds, valid-control results, parser-source "
             "coverage, one-input replay, and AFL++ overlays.", "",
             "## Targets", "", *project_rows, ""])

    for path in manifest_paths:
        manifest = read(path)
        if not fully_runnable(path, manifest):
            continue
        fmt, eco, slug_name = manifest["format"], manifest["ecosystem"], path.parent.name
        project_dir = path.parent
        key = (fmt, eco, manifest["package"])
        catalog_readme = next((ROOT / item["readme"] for item in index
                               if (item["format"], item["ecosystem"], item["name"]) == key), None)
        lines = [f"# {manifest['package']} — {FORMATS[fmt][0]} / {ECO_LABEL[eco]}", "",
                 f"Pinned release: `{manifest['release']}`. "
                 f"[Manifest]({link(project_dir, path)}) · "
                 f"[verification receipt]({link(project_dir, project_dir / 'verification.json')})", ""]
        if catalog_readme:
            lines += [f"[API, control result, and parser family]({link(project_dir, catalog_readme)})", ""]
        else:
            lines += [f"[Standard API inventory]({link(project_dir, ROOT / manifest['standard_inventory'])})", ""]
        lines += ["## Run from the repository root", "", "```sh",
                  f"python3 parsarium.py build {fmt} {eco} {slug_name}",
                  f"python3 parsarium.py run {fmt} {eco} {slug_name} {manifest['control']}",
                  f"python3 parsarium.py replay {fmt} {eco} {slug_name} CORPUS_DIR runs/{fmt}-{slug_name}-replay",
                  f"python3 parsarium.py afl build {fmt} {eco} {slug_name}",
                  f"python3 parsarium.py afl prepare {fmt} {eco} {slug_name} runs/{fmt}-{slug_name}-afl",
                  "```", "",
                  "Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a "
                  "seeded run; it does not start a campaign.", ""]
        if manifest.get("coverage_limit"):
            lines += [f"**Coverage limit:** {manifest['coverage_limit']}", ""]
        if manifest.get("sanitizer_exception"):
            lines += [f"**Sanitizer exception:** {manifest['sanitizer_exception']}", ""]
        if manifest.get("coverage_kind") == "native_binary_edges":
            module = Path(manifest["binary_feedback_module"]).name
            lines += [
                f"**Feedback scope:** AFL++ observes edges in the pinned `{module}` shared library. "
                "This target does not claim source-line coverage. The verification receipt records "
                "the module hash and differential valid-control check.", "",
            ]
        generated[project_dir / "README.md"] = "\n".join(lines)

    index_path = ROOT / "data/parser-readmes.json"
    generated[index_path] = json.dumps({"schema_version": 1, "parsers": index}, indent=2) + "\n"
    if args.check:
        wrong = [str(path.relative_to(ROOT)) for path, content in generated.items()
                 if not path.is_file() or path.read_text(encoding="utf-8") != content]
        if wrong:
            raise SystemExit(f"stale parser READMEs: {len(wrong)}; first: {wrong[0]}")
    else:
        for path, content in generated.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print(f"{'Checked' if args.check else 'Built'} {len(FORMATS)} format guides, "
          f"{len(index)} third-party parser guides, {standard_count} standard API guides, "
          f"and {project_guides} project guides")


if __name__ == "__main__":
    main()
