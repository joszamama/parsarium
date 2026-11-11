"""Render verified, within-cell npm rankings from pinned evidence and metrics."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def read(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    for format_name in ("png", "zip", "mp4", "wav", "pdf", "svg", "http11", "mp3_id3v2"):
        directory = ROOT / "data" / "javascript" / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metrics = snapshot["download_metric"]["packages"]
        ranked = sorted(parsers, key=lambda parser: -metrics[parser["name"]]["downloads"])
        format_label = {"http11": "HTTP/1.1", "mp3_id3v2": "MP3 with ID3v2"}.get(format_name, format_name.upper())
        lines = [
            f"# JavaScript × {format_label}: verified parser ranking",
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

    for format_name in ("zip", "png", "wav", "http11", "mp4"):
        directory = ROOT / "data" / "go" / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metrics = snapshot["popularity_metric"]["packages"]
        ranked = sorted(parsers, key=lambda parser: -(metrics[parser["name"]]["imported_by_packages"] or 0))
        lines = [
            f"# Go × {'HTTP/1.1' if format_name == 'http11' else format_name.upper()}: verified parser ranking",
            "",
            f"{len(ranked)} verified third-party packages; working goal 20, original ceiling 30. "
            "The metric is pkg.go.dev's package-level ‘Imported by’ count captured at "
            f"{snapshot['popularity_metric']['captured_at_utc']}. It measures visible direct importers "
            "rather than downloads, and is used only within Go.",
            "",
            "Search hits and unresolved leads are separate from this ranking. See `cell.json`, "
            "`registry-snapshot.json`, and `verification.json` in this directory.",
            "",
            "| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |",
            "| ---: | --- | --- | ---: | --- | --- |",
        ]
        for rank, parser in enumerate(ranked, 1):
            value = metrics[parser["name"]]["imported_by_packages"]
            count = f"{value:,}" if value is not None else "unknown"
            lines.append(
                f"| {rank} | [{parser['name']}]({parser['documentation']}) | "
                f"{parser['module']}@{parser['version']} | {count} | "
                f"{parser['scope']} | {parser['family']} |"
            )
        (directory / "ranking.md").write_text("\n".join(lines) + "\n")
        print(f"go/{format_name}: {len(ranked)} verified packages ranked")


if __name__ == "__main__":
    main()
