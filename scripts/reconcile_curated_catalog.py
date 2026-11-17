"""Reconcile a revised selection plan with the archived control evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

from plan_curated_catalog import ROOT, plan


def read(path: Path):
    return json.loads(path.read_text())


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--apply", action="store_true")
    args = cli.parse_args()
    path = ROOT / "data/curation/plan.json"
    old = read(path)
    new = plan()
    old_cells = {(item["ecosystem"], item["format"]): item for item in old["cells"]}
    updates = []
    guides = read(ROOT / "data/parser-readmes.json")["parsers"]
    guide_by_key = {(item["ecosystem"], item["format"], item["name"]): item
                    for item in guides}
    for choice in new["cells"]:
        ecosystem, fmt = choice["ecosystem"], choice["format"]
        previous = old_cells[(ecosystem, fmt)]
        former = {item["name"] for item in previous["selected"]}
        current = {item["name"] for item in choice["selected"]}
        if former == current:
            continue
        directory = ROOT / "data" / ecosystem / fmt
        archive = ROOT / "data/curation/preten" / ecosystem / fmt
        if {item["name"] for item in read(directory / "parsers.json")} != former:
            raise ValueError(f"live catalog does not match old plan: {ecosystem}/{fmt}")
        old_rows = read(archive / "parsers.json")
        old_verification = read(archive / "verification.json")
        rows_key = "results" if (ecosystem, fmt) == ("javascript", "png") else "third_party"
        selected_rows = [item for item in old_rows if item["name"] in current]
        selected_results = [item for item in old_verification[rows_key]
                            if item["package"] in current]
        if len(selected_rows) != len(current) or len(selected_results) != len(current):
            raise ValueError(f"archived evidence incomplete: {ecosystem}/{fmt}")
        removed = former - current
        for manifest_path in (ROOT / "projects" / fmt / ecosystem).glob("*/manifest.json"):
            manifest = read(manifest_path)
            if manifest.get("kind") != "standard" and manifest["package"] in removed:
                raise ValueError(f"retired path still has a project: {manifest_path}")
        obsolete_guides = [ROOT / guide_by_key[(ecosystem, fmt, name)]["readme"]
                           for name in removed]
        updates.append((directory, choice, selected_rows, selected_results,
                        rows_key, obsolete_guides, former, current))
    print(f"{len(updates)} cells with selection changes", flush=True)
    for _, choice, _, _, _, _, former, current in updates:
        print(f"  {choice['ecosystem']}/{choice['format']}: "
              f"-{sorted(former-current)} +{sorted(current-former)}", flush=True)
    if not args.apply:
        return
    for directory, choice, rows, results, rows_key, obsolete_guides, _, current in updates:
        verification = read(directory / "verification.json")
        verification[rows_key] = results
        cell = read(directory / "cell.json")
        cell["verified_third_party_count"] = len(current)
        cell["status"] = ("curated_ten_search_bounded" if len(current) == 10 else
                          "curated_below_ten_search_bounded")
        cell["uncertainty"] = (
            f"{len(current)} of {choice['original_count']} control-verified paths "
            "retain a positive numeric adoption signal under the ten-path selection "
            "policy. Search remains bounded by the recorded queries, limits and "
            "unresolved leads. The pre-curation evidence and package-level "
            "inclusion/exclusion reasons are in data/curation/preten/ and "
            "data/curation/plan.json. One valid control does not establish complete "
            "format support or independent parser families.")
        if "verified_document_input_count" in cell:
            cell["verified_document_input_count"] = sum(
                item["input_variant"] == "svg_document" for item in rows)
            cell["verified_path_data_only_count"] = sum(
                item["input_variant"] == "svg_path_data" for item in rows)
        write(directory / "parsers.json", rows)
        write(directory / "verification.json", verification)
        write(directory / "cell.json", cell)
        for guide in obsolete_guides:
            shutil.rmtree(guide.parent)
    write(path, new)
    for script, args in (("audit_curated_metrics.py", []), ("build_matrix.py", []),
                         ("audit_popularity_coverage.py", []), ("build_rankings.py", []),
                         ("audit_projects.py", ["--write"]), ("build_readmes.py", [])):
        subprocess.run([sys.executable, str(ROOT / "scripts" / script), *args],
                       cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
