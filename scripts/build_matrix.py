"""Regenerate the active matrix and separately label incomplete pilot cells."""

from pathlib import Path
import json
from format_registry import ACTIVE_FORMATS, ECOSYSTEMS, PILOT_FORMATS


ROOT = Path(__file__).resolve().parents[1]
FORMATS = ACTIVE_FORMATS  # Compatibility for active-only catalog tooling.


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
    pilot_cells = []
    for ecosystem in ECOSYSTEMS:
        for format_name in PILOT_FORMATS:
            path = ROOT / "data" / ecosystem / format_name / "cell.json"
            if path.is_file():
                cell = json.loads(path.read_text())
                if ((cell.get("ecosystem"), cell.get("format")) != (ecosystem, format_name)
                        or not str(cell.get("status", "")).startswith("pilot_")
                        or cell.get("status") == "pilot_complete"):
                    raise ValueError(f"pilot cell must declare a pilot status: {path}")
                cell = {**cell, "phase": "pilot", "complete": False}
            else:
                cell = {
                    "ecosystem": ecosystem, "format": format_name,
                    "phase": "pilot", "status": "pilot_not_started", "complete": False,
                    "working_target": 10, "ceiling": 10,
                    "verified_third_party_count": 0,
                    "verified_standard_or_runtime_count": 0,
                    "search_queries": [], "search_limit_per_query": 0,
                    "search_hits_recorded": 0,
                    "uncertainty": "No search or standard/runtime inventory has been performed. This pilot cell is incomplete; zero is not evidence of absence."
                }
            pilot_cells.append(cell)
    pilot_out = ROOT / "data" / "pilot-cells.json"
    pilot_out.write_text(json.dumps({"schema_version": 1, "phase": "pilot",
                                     "complete": False, "cells": pilot_cells}, indent=2) + "\n")
    print(f"{len(cells)} active cells: {sum(c['status'] != 'not_started' for c in cells)} started; "
          f"{len(pilot_cells)} incomplete pilot cells")


if __name__ == "__main__":
    main()
