"""Render verified, within-cell npm rankings from pinned evidence and metrics."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def read(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    for format_name in ("png", "zip", "wav", "pdf", "http11"):
        directory = ROOT / "data" / "javascript" / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metrics = snapshot["download_metric"]["packages"]
        ranked = sorted(parsers, key=lambda parser: -metrics[parser["name"]]["downloads"])
        lines = [
            f"# JavaScript × {format_name.upper() if format_name != 'http11' else 'HTTP/1.1'}: verified parser ranking",
            "",
            f"{len(ranked)} verified third-party packages; working goal 20, original ceiling 30. "
            f"npm downloads cover {snapshot['download_metric']['window'].replace(':', ' through ')} inclusive, "
            "counting all versions of each package name. This ranks adoption signals only within this cell.",
            "",
            "Search hits and unresolved leads are separate from this ranking. See `cell.json`, "
            "`registry-snapshot.json`, and `verification.json` in this directory.",
            "",
            "| Rank | Package | Pinned release | Downloads | Scope | Underlying family |",
            "| ---: | --- | --- | ---: | --- | --- |",
        ]
        for rank, parser in enumerate(ranked, 1):
            lines.append(
                f"| {rank} | [{parser['name']}]({parser['documentation']}) | "
                f"{parser['version']} | {metrics[parser['name']]['downloads']:,} | "
                f"{parser['scope']} | {parser['family']} |"
            )
        (directory / "ranking.md").write_text("\n".join(lines) + "\n")
        print(f"{format_name}: {len(ranked)} verified packages ranked")


if __name__ == "__main__":
    main()
