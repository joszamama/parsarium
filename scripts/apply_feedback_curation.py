"""Apply the recorded parser-feedback gate to three active catalog cells.

Run after ``plan_curated_catalog.py --write``. This only updates catalog data;
remove the listed unselected project scaffolds, regenerate guides and reports,
and run the catalog and fuzzing audits before committing.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: Path):
    return json.loads(path.read_text())


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    plan = read(ROOT / "data/curation/plan.json")
    blocked = read(ROOT / "data/curation/feedback-exclusions.json")["paths"]
    choices = {(row["ecosystem"], row["format"]): row for row in plan["cells"]}
    by_cell = {}
    for row in blocked:
        by_cell.setdefault((row["ecosystem"], row["format"]), set()).add(row["name"])
    for (ecosystem, fmt), names in by_cell.items():
        choice = choices[(ecosystem, fmt)]
        selected = {row["name"] for row in choice["selected"]}
        exclusions = {row["name"]: row for row in choice["excluded"]}
        if names & selected or any(exclusions[name]["reason"] != next(
                row["reason"] for row in blocked if row["name"] == name
                and row["ecosystem"] == ecosystem and row["format"] == fmt)
                for name in names):
            raise ValueError(f"feedback exclusion differs from plan: {ecosystem}/{fmt}")
        base = ROOT / "data" / ecosystem / fmt
        parser_path = base / "parsers.json"
        result_path = base / "verification.json"
        cell_path = base / "cell.json"
        parsers = read(parser_path)
        results = read(result_path)
        kept = [row for row in parsers if row["name"] in selected]
        if len(kept) != choice["selected_count"]:
            raise ValueError(f"selected parser count differs: {ecosystem}/{fmt}")
        key = "results" if ecosystem == "javascript" and fmt == "png" else "third_party"
        runs = [row for row in results[key] if row["package"] in selected]
        if {row["package"] for row in runs} != selected:
            raise ValueError(f"selected control results differ: {ecosystem}/{fmt}")
        results[key] = runs
        cell = read(cell_path)
        old = cell["uncertainty"]
        marker = "Post-selection parser-feedback gate:"
        if marker not in old:
            tail = old.split(". ", 1)[1] if ". " in old else old
            cell["uncertainty"] = (
                f"{marker} {len(kept)} selected paths have a verified container "
                "control and parser-derived AFL++ feedback. "
                f"{len(names)} higher-adoption control-verified candidates remain "
                "excluded without backfilling lower-ranked leads; their positive "
                "metrics and exact blockers are in data/curation/plan.json and "
                "data/curation/feedback-exclusions.json. " + tail)
        cell["verified_third_party_count"] = len(kept)
        cell["status"] = "curated_below_ten_search_bounded"
        write(parser_path, kept)
        write(result_path, results)
        write(cell_path, cell)
        print(f"{ecosystem}/{fmt}: {len(kept)} selected; {len(names)} feedback exclusions")


if __name__ == "__main__":
    main()
