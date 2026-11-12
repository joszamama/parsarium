"""Render the PHP SVG ranking from pinned verified rows and saved metrics."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/php/svg"


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    cell = json.loads((DATA / "cell.json").read_text())
    metrics = snapshot["download_metric"]["packages"]
    verified = json.loads((DATA / "verification.json").read_text())["third_party"]
    assert len(parsers) == len(verified) == cell["verified_third_party_count"]
    assert {p["name"] for p in parsers} == {r["package"] for r in verified if r["pass"]}
    rows = sorted(parsers, key=lambda p: (-metrics[p["name"]]["downloads"], p["name"]))
    lines = [
        "# PHP × SVG: verified parser ranking", "",
        f"{len(rows)} pinned third-party package paths passed valid local SVG controls; working goal 20, original ceiling 30. Packagist lifetime downloads were captured with the bounded search snapshot at {snapshot['captured_at_utc']}. This metric covers all package uses and is comparable only within PHP. {cell['unresolved_documentation_leads']} named leads remain unresolved, so the list is not a definitive most-used top twenty.",
        "",
        "| Rank | Package | Pinned release | Lifetime downloads | Observable scope | Underlying family |",
        "| ---: | --- | --- | ---: | --- | --- |",
    ]
    for rank, parser in enumerate(rows, 1):
        name = parser["name"]
        lines.append(
            f"| {rank} | [{name}]({snapshot['releases'][name]['url']}) | {parser['version']} | "
            f"{metrics[name]['downloads']:,} | {parser['scope']} | {parser['family']} |"
        )
    lines += [
        "",
        "The two verified [PHP 8.5 runtime APIs](standard.json) are separate from this ranking. Several package paths share the same enshrined sanitizer, PHP-SVG lineage, dompdf parser, or librsvg engine. The two exact-source Packagist aliases in [leads.json](leads.json) are excluded.",
        "",
    ]
    (DATA / "ranking.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
