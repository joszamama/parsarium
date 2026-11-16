"""Regenerate the 8 x 10 matrix without interpreting unsearched cells as empty."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
ECOSYSTEMS = ["c", "cpp", "go", "java", "javascript", "python", "rust", "php"]
FORMATS = ["png", "zip", "mp4", "wav", "pdf", "svg", "http11", "ascii_ply", "ascii_pnm", "mp3_id3v2"]


def main() -> None:
    cells = []
    for ecosystem in ECOSYSTEMS:
        for format_name in FORMATS:
            path = ROOT / "data" / ecosystem / format_name / "cell.json"
            if path.exists():
                cell = json.loads(path.read_text())
            else:
                cell = {
                    "ecosystem": ecosystem,
                    "format": format_name,
                    "status": "not_started",
                    "working_target": 10,
                    "ceiling": 10,
                    "verified_third_party_count": 0,
                    "verified_standard_or_runtime_count": 0,
                    "search_queries": [],
                    "search_limit_per_query": 0,
                    "search_hits_recorded": 0,
                    "uncertainty": "No search or standard/runtime inventory has been performed. Zero means no verified entry yet, not evidence of absence."
                }
            cells.append(cell)
    out = ROOT / "data" / "cells.json"
    out.write_text(json.dumps({"schema_version": 1, "cells": cells}, indent=2) + "\n")
    print(f"{len(cells)} cells: {sum(c['status'] != 'not_started' for c in cells)} started")


if __name__ == "__main__":
    main()
