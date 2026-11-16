"""Audit numeric adoption evidence and explain every unranked curation decision."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "data/curation/plan.json"
REPORT = ROOT / "data/curation/metric-exceptions.json"
PRIMARY = "primary_metric"
SUPPLEMENTAL = "supplemental_numeric_metric"


def build_report() -> dict:
    plan = json.loads(PLAN.read_text())
    selected = Counter()
    exceptions = []
    for cell in plan["cells"]:
        ecosystem, fmt = cell["ecosystem"], cell["format"]
        for item in cell["selected"]:
            kind = item["selection"]
            if kind == PRIMARY:
                assert isinstance(item["metric"], int) and item["metric"] > 0
            elif kind == SUPPLEMENTAL:
                assert item["metric"] is None or item["metric"] == 0
                assert isinstance(item["supplemental_metric"], int)
                assert item["supplemental_metric"] > 0
                assert item["supplemental_url"].startswith("https://")
            else:
                raise ValueError(f"unknown selection: {kind}")
            selected[kind] += 1
        for item in cell["excluded"]:
            if item["reason"] not in ("primary_metric_unavailable",
                                      "zero_recorded_adoption",
                                      "shared_parser_family_lower_adoption"):
                continue
            supplemental = item.get("supplemental_metric")
            if supplemental is None:
                disposition = "no_secondary_numeric_source_recorded"
            elif item["reason"] == "shared_parser_family_lower_adoption":
                disposition = "shared_family_duplicate"
            elif (item.get("supplemental_kind") == "debian_source_installed"
                  and supplemental < 1000) or (item.get("supplemental_kind") ==
                                                "github_source_stars" and supplemental < 100):
                disposition = "secondary_metric_below_policy_threshold"
            else:
                disposition = "qualified_secondary_metric_but_ten_path_ceiling"
            exceptions.append({
                "ecosystem": ecosystem, "format": fmt, "package": item["name"],
                "primary_metric_field": cell["metric_field"],
                "primary_value": item["metric"],
                "primary_reason": item["reason"],
                "secondary_metric_kind": item.get("supplemental_kind"),
                "secondary_value": supplemental,
                "secondary_source": item.get("supplemental_url"),
                "disposition": disposition,
            })
    assert sum(selected.values()) == plan["selected_total"]
    return {
        "schema_version": 1,
        "selected_paths": plan["selected_total"],
        "selected_with_positive_primary_metric": selected[PRIMARY],
        "selected_with_positive_secondary_metric": selected[SUPPLEMENTAL],
        "selected_without_numeric_metric": 0,
        "excluded_metric_exceptions": len(exceptions),
        "exception_reasons": dict(Counter(e["primary_reason"] for e in exceptions)),
        "dispositions": dict(Counter(e["disposition"] for e in exceptions)),
        "exceptions": exceptions,
    }


def main() -> None:
    report = build_report()
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(f"{report['selected_paths']} selected, all with a positive numeric signal; "
          f"{report['excluded_metric_exceptions']} documented metric exceptions")


if __name__ == "__main__":
    main()
