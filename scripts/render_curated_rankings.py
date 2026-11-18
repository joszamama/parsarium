"""Render the reviewed ten-path rankings without mixing adoption metrics."""

from __future__ import annotations

import json
from pathlib import Path

from metric_labels import SUPPLEMENTAL_BY_KIND, primary_label


ROOT = Path(__file__).resolve().parents[1]
LABELS = {"http11": "HTTP/1.1", "ascii_ply": "ASCII PLY",
          "ascii_pnm": "ASCII PNM"}


def label(value: str) -> str:
    return LABELS.get(value, value.upper())


def cell_text(choice: dict) -> str:
    ecosystem, fmt = choice["ecosystem"], choice["format"]
    parsers = {p["name"]: p for p in json.loads(
        (ROOT / "data" / ecosystem / fmt / "parsers.json").read_text())}
    metadata = choice["metric_metadata"]
    primary = [item for item in choice["selected"] if item["selection"] == "primary_metric"]
    secondary = [item for item in choice["selected"]
                 if item["selection"] == "supplemental_numeric_metric"]
    if set(parsers) != {item["name"] for item in choice["selected"]}:
        raise ValueError(f"selection mismatch: {ecosystem}/{fmt}")
    lines = [f"# {ecosystem.upper()} × {label(fmt)}: selected parsers", "",
             f"{len(parsers)} control-verified third-party paths selected from "
             f"{choice['original_count']} verified candidates. The ceiling is ten. "
             "A path is an API or package route, not necessarily an independent parser engine.",
             "",
             "## Primary within-cell adoption metric", "",
             (f"{metadata.get('name', metadata.get('metric', choice['metric_field']))}. "
              f"{metadata.get('limitation', '')}").rstrip(), "",
             f"| Rank | Package | Release | {primary_label(ecosystem, choice['metric_field'])} | Parsed scope | Parser family |",
             "| ---: | --- | --- | ---: | --- | --- |"]
    if not primary:
        lines.append("| — | No selected path with a positive primary metric | — | — | — | — |")
    for item in primary:
        parser = parsers[item["name"]]
        lines.append(f"| {item['rank']} | [{item['name']}]({parser['documentation']}) | "
                     f"{item['version']} | {item['metric']:,} | "
                     f"{parser['scope'].replace('|', '/')} | {item['family'].replace('|', '/')} |")
    if secondary:
        lines.extend(["", "## Supplemental numeric evidence", "",
                      "These paths lack a positive primary metric. Their figures are reported "
                      "separately and are not compared numerically with the table above.", "",
                      "| Supplemental rank | Package | Release | Signal | Value | Parsed scope | Parser family |",
                      "| ---: | --- | --- | --- | ---: | --- | --- |"])
        for item in secondary:
            parser = parsers[item["name"]]
            kind = SUPPLEMENTAL_BY_KIND[item["supplemental_kind"]]
            lines.append(f"| {item['supplemental_rank']} | "
                         f"[{item['name']}]({parser['documentation']}) | "
                         f"{item['version']} | [{kind}]({item['supplemental_url']}) | "
                         f"{item['supplemental_metric']:,} | "
                         f"{parser['scope'].replace('|', '/')} | "
                         f"{item['family'].replace('|', '/')} |")
    lines.extend(["", "The [selection plan](../../curation/plan.json) records all exclusions "
                  "and original snapshot hashes. The "
                  "[metric exception report](../../curation/metric-exceptions.json) "
                  "lists missing and zero adoption signals. Search limits and unresolved "
                  "leads remain in `cell.json` and `registry-snapshot.json`.", ""])
    return "\n".join(lines)


def main() -> None:
    plan = json.loads((ROOT / "data/curation/plan.json").read_text())
    for choice in plan["cells"]:
        path = ROOT / "data" / choice["ecosystem"] / choice["format"] / "ranking.md"
        path.write_text(cell_text(choice))
    print(f"Rendered {len(plan['cells'])} selected-cell rankings")


if __name__ == "__main__":
    main()
