"""Render the C HTTP/1.1 ranking from its frozen discovery and metric snapshot."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/c/http11"


def render(parsers: list[dict], snapshot: dict) -> str:
    metric = snapshot["popularity_metric"]
    values = metric["packages"]
    assert {p["name"] for p in parsers} == set(values)
    ranked = sorted(parsers, key=lambda p: (values[p["name"]]["stars"] is None,
                                            -(values[p["name"]]["stars"] or 0), p["name"]))
    capture_date = metric["captured_at_utc"][:10]
    lines = [
        "# C × HTTP/1.1: verified parser ranking", "",
        f"{len(ranked)} verified package paths; working goal 20, original ceiling 30. "
        f"GitHub stars are project-level interest signals observed on {capture_date} "
        "and compared only within C. The exact source, method and capture time "
        "for each value are in `registry-snapshot.json`. Stars are not downloads "
        "or measured parser adoption. Packages without a comparable primary "
        "GitHub repository remain unranked.", "",
        "Search hits, unresolved leads, and C standard APIs are separate from this ranking. "
        "See `cell.json`, `leads.json`, `standard.json`, and `verification.json`.", "",
        "| Rank | Package | Pinned release | Stars | Scope | Underlying family |",
        "| ---: | --- | --- | ---: | --- | --- |",
    ]
    rank = 0
    for parser in ranked:
        stars = values[parser["name"]]["stars"]
        if stars is None:
            rank_label, stars_label = "unranked", "n/a"
        else:
            rank += 1
            rank_label, stars_label = str(rank), f"{stars:,}"
        lines.append(f"| {rank_label} | [{parser['name']}]({parser['documentation']}) | "
                     f"{parser['version']} | {stars_label} | {parser['scope']} | {parser['family']} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parsers = json.loads((DATA / "parsers.json").read_text())
    snapshot = json.loads((DATA / "registry-snapshot.json").read_text())
    (DATA / "ranking.md").write_text(render(parsers, snapshot))
    print(f"Rendered {len(parsers)} C HTTP/1.1 package paths")


if __name__ == "__main__":
    main()
