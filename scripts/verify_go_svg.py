"""Run pinned Go SVG parsers against the valid local SVG control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "svg"
MODULE = ROOT / "adapters" / "go" / "svg"
CONTROL = ROOT / "controls" / "svg" / "red-green.svg"


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    results = []
    for parser in parsers:
        command = ["go", "run", ".", parser["name"], "../../../controls/svg/red-green.svg"]
        output = None
        error = None
        try:
            run = subprocess.run(command, cwd=MODULE, text=True, capture_output=True, timeout=120, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({"package": parser["name"], "module": parser["module"],
                        "version": parser["version"], "scope": parser["scope"],
                        "command": " ".join(command), "pass": passed,
                        "output": output, "error": error})
    version = subprocess.run(["go", "version"], cwd=MODULE, text=True, capture_output=True, check=True).stdout.strip()
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "go": version,
              "control": "controls/svg/red-green.svg",
              "control_sha256": hashlib.sha256(CONTROL.read_bytes()).hexdigest(),
              "control_meaning": "SVG with a 2x1 viewBox and two one-pixel rectangles, red then green",
              "third_party": results}
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Go SVG packages passed")
    if count != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
