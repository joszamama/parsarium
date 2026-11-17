"""Plan a smaller parser catalog from the recorded within-cell adoption metrics.

This is a read-only selection step unless --write is given. The plan retains
every inclusion and exclusion decision so a later pruning pass is reviewable.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path

from audit_popularity_coverage import METRIC_FIELD


ROOT = Path(__file__).resolve().parents[1]
LIMIT = 10
POPCON_MIN_INSTALLS = 1000
GITHUB_MIN_STARS = 100
POPCON_SLOTS = 3
# This distribution contains byte-identical parser files from Providence.
SUPPLEMENTAL_EXCLUSIONS = {("php", "ascii_ply", "collectiveaccess/pawtucket2")}
# PyPI explicitly describes this pinned release as an empty compatibility
# distribution; the parsing code is in the already selected PyMuPDF package.
ELIGIBILITY_EXCLUSIONS = {
    ("python", "pdf", "pymupdf4llm"):
        ("empty_compatibility_distribution", "https://pypi.org/project/pymupdf4llm/2.1/"),
}


def metric_field(ecosystem: str, metric: dict) -> str:
    field = METRIC_FIELD[ecosystem]
    if field == "dynamic":
        return ("install_on_request_365d" if metric.get("metric")
                == "Homebrew install-on-request count over 365 days" else "stars")
    return field


def plan() -> dict:
    cells = json.loads((ROOT / "data/cells.json").read_text())["cells"]
    feedback_file = ROOT / "data/curation/feedback-exclusions.json"
    feedback = json.loads(feedback_file.read_text())["paths"]
    feedback_by_key = {(row["ecosystem"], row["format"], row["name"]): row
                       for row in feedback}
    if len(feedback_by_key) != len(feedback):
        raise ValueError("duplicate parser-feedback exclusion")
    feedback_seen = set()
    backfill_file = ROOT / "data/curation/feedback-backfills.json"
    backfills = json.loads(backfill_file.read_text())["paths"]
    backfill_by_key = {(row["ecosystem"], row["format"], row["name"]): row
                       for row in backfills}
    if len(backfill_by_key) != len(backfills):
        raise ValueError("duplicate parser-feedback backfill")
    backfill_seen = set()
    popcon_file = ROOT / "data/curation/popcon-snapshot.json"
    github_file = ROOT / "data/curation/github-supplemental-stars.json"
    popcon = json.loads(popcon_file.read_text())
    github = json.loads(github_file.read_text())
    github_rows = {}
    for row in github["rows"]:
        for path in row["paths"]:
            ecosystem, name = path.split("/", 1)
            github_rows[(ecosystem, name)] = row
    result = []
    for cell in cells:
        ecosystem, format_name = cell["ecosystem"], cell["format"]
        source = ROOT / "data/curation/preten" / ecosystem / format_name
        if not source.exists():
            source = ROOT / "data" / ecosystem / format_name
        parser_file = source / "parsers.json"
        snapshot_file = ROOT / "data" / ecosystem / format_name / "registry-snapshot.json"
        parsers = json.loads(parser_file.read_text())
        snapshot = json.loads(snapshot_file.read_text())
        metric = snapshot.get("download_metric", snapshot.get("popularity_metric", {}))
        field = metric_field(ecosystem, metric)
        values = metric.get("packages", {})
        measured = []
        zero_or_missing = []
        supplemental = []
        ineligible = []
        for parser in parsers:
            value = values.get(parser["name"], {}).get(field)
            item = {"name": parser["name"], "version": parser["version"],
                    "family": parser["family"], "metric": value}
            exclusion = ELIGIBILITY_EXCLUSIONS.get((ecosystem, format_name, parser["name"]))
            if exclusion:
                ineligible.append({**item, "reason": exclusion[0], "evidence_url": exclusion[1]})
                continue
            supplemental_value = None
            supplemental_kind = None
            supplemental_url = None
            if value is None and ecosystem in {"c", "cpp"} and format_name != "ascii_ply":
                source = popcon["packages"].get(parser["name"])
                if source:
                    supplemental_value = source["installed"]
                    supplemental_kind = "debian_source_installed"
                    supplemental_url = source["source_identity"]
            elif value is None and format_name == "ascii_ply":
                source = github_rows.get((ecosystem, parser["name"]))
                if source:
                    supplemental_value = source["stars"]
                    supplemental_kind = "github_source_stars"
                    supplemental_url = source["resolved_url"]
            if supplemental_value is not None:
                item.update(supplemental_metric=supplemental_value,
                            supplemental_kind=supplemental_kind,
                            supplemental_url=supplemental_url)
            if value is None:
                zero_or_missing.append({**item, "reason": "primary_metric_unavailable"})
            elif not isinstance(value, int) or value < 0:
                raise ValueError(f"invalid metric: {ecosystem}/{format_name}/{parser['name']}: {value}")
            elif value == 0:
                zero_or_missing.append({**item, "reason": "zero_recorded_adoption"})
            else:
                measured.append(item)
        measured.sort(key=lambda item: (-item["metric"], item["name"].casefold()))
        for item in zero_or_missing:
            score = item.get("supplemental_metric")
            kind = item.get("supplemental_kind")
            if (ecosystem, format_name, item["name"]) in SUPPLEMENTAL_EXCLUSIONS:
                item["reason"] = "shared_parser_family_lower_adoption"
            elif kind == "debian_source_installed" and score >= POPCON_MIN_INSTALLS:
                supplemental.append(item)
            elif kind == "github_source_stars" and score >= GITHUB_MIN_STARS:
                supplemental.append(item)
        supplemental.sort(key=lambda item: (-item["supplemental_metric"],
                                             item["name"].casefold()))
        supplement_limit = (max(0, LIMIT - len(measured)) if format_name == "ascii_ply"
                            else POPCON_SLOTS)
        chosen_supplemental = supplemental[:min(supplement_limit, LIMIT)]
        primary_limit = LIMIT - len(chosen_supplemental)
        chosen_primary = measured[:primary_limit]
        if len(chosen_primary) < primary_limit:
            chosen_supplemental = supplemental[:LIMIT - len(chosen_primary)]
        selected = [{**item, "selection": "primary_metric", "rank": index}
                    for index, item in enumerate(chosen_primary, 1)]
        selected.extend({**item, "selection": "supplemental_numeric_metric",
                         "supplemental_rank": index}
                        for index, item in enumerate(chosen_supplemental, 1))
        selected_names = {item["name"] for item in selected}
        excluded = []
        for index, item in enumerate(measured, 1):
            if item["name"] not in selected_names:
                excluded.append({**item, "reason": "outside_ten_path_ceiling", "rank": index})
        for item in zero_or_missing:
            if item["name"] not in selected_names:
                excluded.append(item)
        excluded.extend(ineligible)
        # A positive adoption metric alone does not make an instrumented target.
        # Apply this gate after the ten-path ranking, leaving the slot empty.
        retained = []
        for item in selected:
            key = (ecosystem, format_name, item["name"])
            blocker = feedback_by_key.get(key)
            if blocker is None:
                retained.append(item)
                continue
            feedback_seen.add(key)
            evidence = ROOT / blocker["evidence"]
            if not evidence.is_file():
                raise ValueError(f"missing parser-feedback evidence: {evidence}")
            excluded.append({**item, "reason": blocker["reason"],
                             "feedback_evidence": blocker["evidence"],
                             "feedback_evidence_sha256": sha256(evidence.read_bytes()).hexdigest(),
                             "limitation": blocker["limitation"],
                             "prior_selected_rank": item.get("rank", item.get("supplemental_rank"))})
        # A vacated slot is refilled only in primary-rank order, and only by a
        # path whose own container control and AFL++ feedback receipt passed.
        # An unresolved next-ranked path stops the refill; a next-ranked path
        # with a recorded feedback blocker stays excluded and the walk continues.
        if len(retained) < len(selected):
            ceiling = sorted((item for item in excluded
                              if item["reason"] == "outside_ten_path_ceiling"),
                             key=lambda item: item["rank"])
            for item in ceiling:
                if len(retained) >= LIMIT:
                    break
                key = (ecosystem, format_name, item["name"])
                blocker = feedback_by_key.get(key)
                if blocker is not None:
                    feedback_seen.add(key)
                    evidence = ROOT / blocker["evidence"]
                    if not evidence.is_file():
                        raise ValueError(f"missing parser-feedback evidence: {evidence}")
                    item.update(reason=blocker["reason"], feedback_evidence=blocker["evidence"],
                                feedback_evidence_sha256=sha256(evidence.read_bytes()).hexdigest(),
                                limitation=blocker["limitation"],
                                prior_primary_rank=item.pop("rank"))
                    continue
                backfill = backfill_by_key.get(key)
                if backfill is None:
                    break
                backfill_seen.add(key)
                evidence = ROOT / backfill["evidence"]
                if not evidence.is_file() or not json.loads(evidence.read_text()).get("pass"):
                    raise ValueError(f"missing or failing backfill evidence: {evidence}")
                excluded.remove(item)
                retained.append({**{k: v for k, v in item.items() if k not in ("reason", "rank")},
                                 "selection": "primary_metric",
                                 "backfilled_after_feedback_exclusion": True,
                                 "prior_primary_rank": item["rank"],
                                 "feedback_evidence": backfill["evidence"],
                                 "feedback_evidence_sha256": sha256(evidence.read_bytes()).hexdigest()})
            retained.sort(key=lambda item: (item["selection"] != "primary_metric",
                                            -(item["metric"] or 0) if item["selection"] == "primary_metric"
                                            else -item["supplemental_metric"],
                                            item["name"].casefold()))
        selected = retained
        for index, item in enumerate((x for x in selected if x["selection"] == "primary_metric"), 1):
            item["rank"] = index
        for index, item in enumerate((x for x in selected if x["selection"] == "supplemental_numeric_metric"), 1):
            item["supplemental_rank"] = index
        excluded.sort(key=lambda item: item["name"].casefold())
        if len(selected) > LIMIT or len(selected) + len(excluded) != len(parsers):
            raise ValueError(f"selection mismatch: {ecosystem}/{format_name}")
        result.append({
            "ecosystem": ecosystem, "format": format_name,
            "metric_field": field,
            "metric_metadata": {key: value for key, value in metric.items() if key != "packages"},
            "parsers_sha256": sha256(parser_file.read_bytes()).hexdigest(),
            "snapshot_sha256": sha256(snapshot_file.read_bytes()).hexdigest(),
            "original_count": len(parsers), "selected_count": len(selected),
            "selected": selected, "excluded": excluded,
        })
    if backfill_seen != set(backfill_by_key):
        raise ValueError(f"backfill is not a next-ranked path: {set(backfill_by_key) - backfill_seen}")
    if feedback_seen != set(feedback_by_key):
        raise ValueError(f"feedback exclusion is not an adopted selected path: {set(feedback_by_key) - feedback_seen}")
    return {
        "schema_version": 1,
        "policy": "At most ten paths per cell. Rank positive primary adoption metrics only within a cell. A limited number of primary-unranked paths may qualify through separately recorded numeric evidence: Debian source-package installations (at least 1000, at most three slots per C/C++ non-PLY cell) or GitHub upstream stars (at least 100, filling remaining PLY slots). Different metrics are never combined into one rank. Zero primary values and missing values do not fill slots without supplemental evidence. A byte-identical lower-adoption PHP PLY family duplicate and a pinned empty Python PDF compatibility distribution are excluded. After adoption ranking, selected paths without a verified container control and parser-derived AFL++ feedback are excluded; a vacated slot is refilled only in primary-rank order by the next-ranked path with its own verified container control and parser-derived AFL++ feedback.",
        "supplemental_sources": {
            "popcon_snapshot_sha256": sha256(popcon_file.read_bytes()).hexdigest(),
            "github_snapshot_sha256": sha256(github_file.read_bytes()).hexdigest(),
            "feedback_exclusions_sha256": sha256(feedback_file.read_bytes()).hexdigest(),
            "feedback_backfills_sha256": sha256(backfill_file.read_bytes()).hexdigest(),
        },
        "cells": result,
        "selected_total": sum(cell["selected_count"] for cell in result),
        "excluded_total": sum(len(cell["excluded"]) for cell in result),
    }


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--write", action="store_true")
    args = cli.parse_args()
    result = plan()
    print(f"Proposed {result['selected_total']} selected paths, "
          f"{result['excluded_total']} excluded, across {len(result['cells'])} cells")
    for cell in result["cells"]:
        if cell["selected_count"] < LIMIT:
            print(f"  {cell['ecosystem']}/{cell['format']}: {cell['selected_count']} with recorded numeric signals")
    if args.write:
        path = ROOT / "data/curation/plan.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
