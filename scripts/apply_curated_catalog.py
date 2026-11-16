"""Apply the reviewed ten-path plan while preserving the pre-curation evidence."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "data/curation/preten"
SMOKE_REPORTS = (
    "fuzz-case-smoke.json", "fuzz-batch-smoke.json", "native-plan-smoke.json",
    "afl-native-smoke.json", "afl-rust-smoke.json", "ecosystem-feedback-smoke.json",
    "afl-python-smoke.json", "afl-bridge-smoke.json", "afl-plan-smoke.json",
)


def read(path: Path):
    return json.loads(path.read_text())


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--apply", action="store_true", help="write the curated catalog")
    args = cli.parse_args()
    plan = read(ROOT / "data/curation/plan.json")
    if ARCHIVE.exists():
        raise ValueError("pre-curation archive already exists; refusing to apply twice")
    if len(plan["cells"]) != 80 or plan["selected_total"] != 775:
        raise ValueError("unexpected plan size")
    selected_keys = set()
    excluded_keys = set()
    cell_updates = []
    for choice in plan["cells"]:
        ecosystem, fmt = choice["ecosystem"], choice["format"]
        directory = ROOT / "data" / ecosystem / fmt
        parsers_path = directory / "parsers.json"
        snapshot_path = directory / "registry-snapshot.json"
        if sha256(parsers_path.read_bytes()).hexdigest() != choice["parsers_sha256"]:
            raise ValueError(f"parser evidence changed: {ecosystem}/{fmt}")
        if sha256(snapshot_path.read_bytes()).hexdigest() != choice["snapshot_sha256"]:
            raise ValueError(f"registry evidence changed: {ecosystem}/{fmt}")
        parsers = read(parsers_path)
        verification = read(directory / "verification.json")
        cell = read(directory / "cell.json")
        selected_names = {item["name"] for item in choice["selected"]}
        excluded_names = {item["name"] for item in choice["excluded"]}
        if ({item["name"] for item in parsers} != selected_names | excluded_names
                or selected_names & excluded_names or len(selected_names) > 10):
            raise ValueError(f"plan does not partition {ecosystem}/{fmt}")
        rows_key = "results" if (ecosystem, fmt) == ("javascript", "png") else "third_party"
        if {item["package"] for item in verification[rows_key]} != {
                item["name"] for item in parsers}:
            raise ValueError(f"verification does not match {ecosystem}/{fmt}")
        for name in selected_names:
            selected_keys.add((fmt, ecosystem, name))
        for name in excluded_names:
            excluded_keys.add((fmt, ecosystem, name))
        selected_parsers = [item for item in parsers if item["name"] in selected_names]
        selected_verification = dict(verification)
        selected_verification[rows_key] = [item for item in verification[rows_key]
                                           if item["package"] in selected_names]
        updated_cell = dict(cell)
        updated_cell.update(
            status=("curated_ten_search_bounded" if len(selected_names) == 10
                    else "curated_below_ten_search_bounded"),
            working_target=10,
            ceiling=10,
            verified_third_party_count=len(selected_names),
            uncertainty=(f"{len(selected_names)} of {len(parsers)} control-verified paths "
                         "retain a positive numeric adoption signal under the ten-path "
                         "selection policy. Search remains bounded by the recorded queries, "
                         "limits and unresolved leads. The pre-curation evidence and "
                         "package-level inclusion/exclusion reasons are in "
                         f"data/curation/preten/{ecosystem}/{fmt}/ and "
                         "data/curation/plan.json. One valid control does not establish "
                         "complete format support or independent parser families."),
            curation_plan="data/curation/plan.json",
            precuration_evidence=f"data/curation/preten/{ecosystem}/{fmt}",
        )
        if "verified_document_input_count" in updated_cell:
            updated_cell["verified_document_input_count"] = sum(
                item["input_variant"] == "svg_document" for item in selected_parsers)
            updated_cell["verified_path_data_only_count"] = sum(
                item["input_variant"] == "svg_path_data" for item in selected_parsers)
        cell_updates.append((directory, ecosystem, fmt, parsers, verification, cell,
                             selected_parsers, selected_verification, updated_cell))
    if len(selected_keys) != plan["selected_total"] or len(excluded_keys) != plan["excluded_total"]:
        raise ValueError("aggregate selection mismatch")

    third_party_remove = []
    kept_project_dirs = set()
    for manifest_path in (ROOT / "projects").glob("*/*/*/manifest.json"):
        manifest = read(manifest_path)
        relative = manifest_path.parent.relative_to(ROOT / "projects")
        if manifest.get("kind") == "standard":
            kept_project_dirs.add(relative.as_posix())
            continue
        key = (manifest["format"], manifest["ecosystem"], manifest["package"])
        if key in excluded_keys:
            third_party_remove.append(manifest_path.parent)
        elif key in selected_keys:
            kept_project_dirs.add(relative.as_posix())
        else:
            raise ValueError(f"uncataloged project: {manifest_path}")
    guides = read(ROOT / "data/parser-readmes.json")["parsers"]
    if {(i["format"], i["ecosystem"], i["name"]) for i in guides} != (
            selected_keys | excluded_keys):
        raise ValueError("parser guide index does not match catalog")
    guide_dirs = {ROOT / item["readme"] for item in guides}
    if not all(path.name == "README.md" and path.is_file() for path in guide_dirs):
        raise ValueError("parser guide path is missing")
    known_project_dirs = kept_project_dirs | {
        path.relative_to(ROOT / "projects").as_posix() for path in third_party_remove}
    filtered_reports = {}
    for name in SMOKE_REPORTS:
        report = read(ROOT / "data" / name)
        if not {item["project"] for item in report["results"]} <= known_project_dirs:
            raise ValueError(f"unexpected smoke project set: {name}")
        results = [item for item in report["results"]
                   if item["project"] in kept_project_dirs]
        report["results"] = results
        report["projects_total"] = len(results)
        for key in ("projects_verified", "projects_ready", "projects_passing"):
            if key in report:
                report[key] = len(results)
        if "batch_passing" in report:
            report["batch_passing"] = sum(item["status"] == "ok" for item in results)
            report["per_case_only"] = sum(item["status"] == "per_case_only"
                                          for item in results)
        filtered_reports[name] = report
    print(f"Plan: {len(selected_keys)} retained, {len(excluded_keys)} removed; "
          f"{len(third_party_remove)} project directories and {len(guide_dirs)} "
          "generated parser guides to replace")
    if not args.apply:
        return
    for directory, ecosystem, fmt, parsers, verification, cell, selected_parsers, \
            selected_verification, updated_cell in cell_updates:
        archive = ARCHIVE / ecosystem / fmt
        archive.mkdir(parents=True, exist_ok=True)
        for name in ("parsers.json", "verification.json", "cell.json"):
            shutil.copyfile(directory / name, archive / name)
        write(directory / "parsers.json", selected_parsers)
        write(directory / "verification.json", selected_verification)
        write(directory / "cell.json", updated_cell)
    for directory in third_party_remove:
        shutil.rmtree(directory)
        overlay = ROOT / "fuzzing/afl-native" / directory.relative_to(ROOT / "projects")
        if overlay.exists():
            shutil.rmtree(overlay)
    for readme in guide_dirs:
        shutil.rmtree(readme.parent)
    for name, report in filtered_reports.items():
        write(ROOT / "data" / name, report)
    print("Applied the selection; regenerate matrix, rankings, coverage and guides")


if __name__ == "__main__":
    main()
