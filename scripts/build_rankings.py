"""Render verified, within-cell npm rankings from pinned evidence and metrics."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]


def read(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    for format_name in ("png", "zip", "mp4", "wav", "pdf", "svg", "http11", "mp3_id3v2", "ascii_pnm", "ascii_ply", "matrix_market"):
        directory = ROOT / "data" / "javascript" / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metrics = snapshot["download_metric"]["packages"]
        ranked = sorted(parsers, key=lambda parser: -metrics[parser["name"]]["downloads"])
        format_label = {"http11": "HTTP/1.1", "mp3_id3v2": "MP3 with ID3v2", "ascii_pnm": "ASCII PNM", "ascii_ply": "ASCII PLY", "matrix_market": "Matrix Market"}.get(format_name, format_name.upper())
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

    for format_name in ("zip", "png", "wav", "http11", "mp4", "mp3_id3v2", "pdf", "svg", "ascii_pnm", "ascii_ply", "matrix_market"):
        directory = ROOT / "data" / "go" / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metrics = snapshot["popularity_metric"]["packages"]
        ranked = sorted((p for p in parsers if metrics[p["name"]]["imported_by_packages"] is not None),
                        key=lambda parser: (-metrics[parser["name"]]["imported_by_packages"], parser["name"]))
        unknown = sorted((p for p in parsers if metrics[p["name"]]["imported_by_packages"] is None),
                         key=lambda parser: parser["name"])
        label = {"http11": "HTTP/1.1", "mp3_id3v2": "MP3 with ID3v2", "ascii_pnm": "ASCII PNM", "ascii_ply": "ASCII PLY", "matrix_market": "Matrix Market"}.get(format_name, format_name.upper())
        lines = [
            f"# Go × {label}: verified parser ranking",
            "",
            f"{len(parsers)} verified third-party packages; working goal 20, original ceiling 30. "
            "The metric is pkg.go.dev's package-level ‘Imported by’ count captured at "
            f"{snapshot['popularity_metric']['captured_at_utc']}. It measures visible direct importers "
            f"rather than downloads, and is used only within Go. {len(unknown)} package(s) lack "
            "a metric and remain unranked; equal counts share a rank.",
            "",
            "Search hits and unresolved leads are separate from this ranking. See `cell.json`, "
            "`registry-snapshot.json`, and `verification.json` in this directory.",
            "",
            "| Rank | Package | Pinned module release | Imported by packages | Scope | Underlying family |",
            "| ---: | --- | --- | ---: | --- | --- |",
        ]
        previous_count = None
        displayed_rank = 0
        for position, parser in enumerate(ranked, 1):
            value = metrics[parser["name"]]["imported_by_packages"]
            if value != previous_count:
                displayed_rank = position
                previous_count = value
            count = f"{value:,}" if value is not None else "unknown"
            lines.append(
                f"| {displayed_rank} | [{parser['name']}]({parser['documentation']}) | "
                f"{parser['module']}@{parser['version']} | {count} | "
                f"{parser['scope']} | {parser['family']} |"
            )
        for parser in unknown:
            lines.append(
                f"| unranked | [{parser['name']}]({parser['documentation']}) | "
                f"{parser['module']}@{parser['version']} | unknown | "
                f"{parser['scope']} | {parser['family']} |"
            )
        (directory / "ranking.md").write_text("\n".join(lines) + "\n")
        print(f"go/{format_name}: {len(ranked)} verified packages ranked, {len(unknown)} unranked")

    for format_name, label in (("png", "PNG"), ("ascii_ply", "ASCII PLY"),
                               ("ascii_pnm", "ASCII PNM"),
                               ("zip", "ZIP"), ("wav", "WAV"), ("pdf", "PDF"),
                               ("mp3_id3v2", "MP3 with ID3v2"), ("mp4", "MP4"),
                               ("http11", "HTTP/1.1"), ("svg", "SVG"),
                               ("matrix_market", "Matrix Market")):
        directory = ROOT / "data" / "python" / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metrics = snapshot["download_metric"]["packages"]
        known = sorted((parser for parser in parsers if metrics[parser["name"]]["downloads"] is not None),
                       key=lambda parser: -metrics[parser["name"]]["downloads"])
        unknown = [parser for parser in parsers if metrics[parser["name"]]["downloads"] is None]
        lines = [
            f"# Python × {label}: verified parser ranking", "",
            f"{len(parsers)} verified third-party packages; working goal 20, original ceiling 30. "
            "The metric is PyPI Stats `last_month` downloads excluding known mirrors, captured at "
            f"{snapshot['download_metric']['captured_at_utc']}. It is compared only within Python. "
            f"{len(unknown)} package(s) lack a metric and remain unranked; no value is inferred.", "",
            "The PyPI Simple Index leads are alphabetically ordered names, not a popularity search. "
            "Search hits, unresolved leads, and standard-library findings are separate from this ranking.", "",
            "| Rank | Package | Pinned release | Last-month downloads | Scope | Underlying family |",
            "| ---: | --- | --- | ---: | --- | --- |",
        ]
        for rank, parser in enumerate(known, 1):
            lines.append(f"| {rank} | [{parser['name']}]({parser['documentation']}) | "
                         f"{parser['version']} | {metrics[parser['name']]['downloads']:,} | "
                         f"{parser['scope']} | {parser['family']} |")
        for parser in unknown:
            lines.append(f"| unranked | [{parser['name']}]({parser['documentation']}) | "
                         f"{parser['version']} | unknown | {parser['scope']} | {parser['family']} |")
        (directory / "ranking.md").write_text("\n".join(lines) + "\n")
        print(f"python/{format_name}: {len(parsers)} verified packages, {len(unknown)} unranked")

    for format_name, label in (("png", "PNG"), ("zip", "ZIP"), ("mp4", "MP4"), ("wav", "WAV"), ("pdf", "PDF"), ("svg", "SVG"), ("http11", "HTTP/1.1"), ("ascii_ply", "ASCII PLY"),
                               ("mp3_id3v2", "MP3 with ID3v2")):
        directory = ROOT / "data" / "rust" / format_name
        parsers = read(directory / "parsers.json")
        snapshot = read(directory / "registry-snapshot.json")
        metrics = snapshot["popularity_metric"]["packages"]
        known = sorted((parser for parser in parsers if metrics[parser["name"]]["recent_downloads"] is not None),
                       key=lambda parser: (-metrics[parser["name"]]["recent_downloads"], parser["name"]))
        unknown = sorted((parser for parser in parsers if metrics[parser["name"]]["recent_downloads"] is None),
                         key=lambda parser: parser["name"])
        lines = [
            f"# Rust × {label}: verified parser ranking", "",
            f"{len(parsers)} verified third-party crate paths; working goal 20, original ceiling 30. "
            "The metric is crates.io crate-level recent downloads over 90 days, captured at "
            f"{snapshot['popularity_metric']['captured_at_utc']}. It includes all releases of each "
            f"crate name and is compared only within Rust. {len(unknown)} crate(s) lack a metric "
            "and remain unranked; equal counts share a rank.", "",
            "Search hits, unresolved leads, and the standard-library inventory are separate from this ranking. "
            "See `cell.json`, `leads.json`, and `verification.json` in this directory.", "",
            "| Rank | Crate | Pinned release | 90-day downloads | Scope | Underlying family |",
            "| ---: | --- | --- | ---: | --- | --- |",
        ]
        previous_count = None
        displayed_rank = 0
        for position, parser in enumerate(known, 1):
            value = metrics[parser["name"]]["recent_downloads"]
            if value != previous_count:
                displayed_rank = position
                previous_count = value
            lines.append(f"| {displayed_rank} | [{parser['name']}]({parser['documentation']}) | "
                         f"{parser['version']} | {value:,} | {parser['scope']} | {parser['family']} |")
        for parser in unknown:
            lines.append(f"| unranked | [{parser['name']}]({parser['documentation']}) | "
                         f"{parser['version']} | unknown | {parser['scope']} | {parser['family']} |")
        (directory / "ranking.md").write_text("\n".join(lines) + "\n")
        print(f"rust/{format_name}: {len(known)} verified packages ranked, {len(unknown)} unranked")


if __name__ == "__main__":
    main()
