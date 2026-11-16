"""Report which verified parser paths have a comparable cell ranking metric."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
METRIC_FIELD = {
    "c": "dynamic",
    "cpp": "dynamic",
    "go": "imported_by_packages",
    "java": "direct_dependent_count",
    "javascript": "downloads",
    "python": "downloads",
    "rust": "recent_downloads",
    "php": "downloads",
}


def read(path: Path):
    return json.loads(path.read_text())


def build_report() -> dict:
    cells = read(ROOT / "data/cells.json")["cells"]
    plan = read(ROOT / "data/curation/plan.json")
    selected = {(cell["ecosystem"], cell["format"]): {
        item["name"]: item for item in cell["selected"]} for cell in plan["cells"]}
    rows = []
    for cell in cells:
        ecosystem, format_name = cell["ecosystem"], cell["format"]
        directory = ROOT / "data" / ecosystem / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metric = snapshot.get("download_metric", snapshot.get("popularity_metric", {}))
        packages = metric.get("packages", {})
        field = METRIC_FIELD[ecosystem]
        if field == "dynamic":
            field = ("install_on_request_365d" if metric.get("metric")
                     == "Homebrew install-on-request count over 365 days" else "stars")
        measured = zero = missing = supplemental = 0
        for parser in parsers:
            value = packages.get(parser["name"], {}).get(field)
            choice = selected[(ecosystem, format_name)].get(parser["name"])
            if choice and choice["selection"] == "supplemental_numeric_metric":
                assert choice["supplemental_metric"] > 0
                supplemental += 1
            if value is None:
                missing += 1
            else:
                if not isinstance(value, int) or value < 0:
                    raise ValueError((ecosystem, format_name, parser["name"], value))
                measured += 1
                zero += value == 0
        assert measured + missing == cell["verified_third_party_count"]
        rows.append({
            "ecosystem": ecosystem,
            "format": format_name,
            "verified_count": len(parsers),
            "with_comparable_metric": measured,
            "without_comparable_metric": missing,
            "zero_metric_count": zero,
            "with_supplemental_numeric_metric": supplemental,
            "without_positive_numeric_signal": len(parsers) - (measured - zero) - supplemental,
            "working_target_met": len(parsers) >= cell["working_target"],
        })
    report = {
        "description": "Metric availability among verified package paths. Primary within-cell rankings and supplemental numeric signals are separate; values are never compared across ecosystems.",
        "verified_paths": sum(row["verified_count"] for row in rows),
        "with_comparable_metric": sum(row["with_comparable_metric"] for row in rows),
        "without_comparable_metric": sum(row["without_comparable_metric"] for row in rows),
        "zero_metric_count": sum(row["zero_metric_count"] for row in rows),
        "with_supplemental_numeric_metric": sum(row["with_supplemental_numeric_metric"] for row in rows),
        "without_positive_numeric_signal": sum(row["without_positive_numeric_signal"] for row in rows),
        "cells_at_working_target": sum(row["working_target_met"] for row in rows),
        "cells": rows,
    }
    return report


def main() -> None:
    report = build_report()
    path = ROOT / "data/popularity-coverage.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"{report['verified_paths']} verified paths; "
          f"{report['with_comparable_metric']} with a cell metric; "
          f"{report['with_supplemental_numeric_metric']} with supplemental numeric evidence; "
          f"{report['without_positive_numeric_signal']} without a positive numeric signal; "
          f"{report['cells_at_working_target']}/{len(report['cells'])} cells at 10")


if __name__ == "__main__":
    main()
