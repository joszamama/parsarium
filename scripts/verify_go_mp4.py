"""Run pinned Go MP4 parsers against the valid local MP4 control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "mp4"
MODULE = ROOT / "adapters" / "go" / "mp4"
CONTROL = ROOT / "controls" / "mp4" / "red-av.mp4"


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    results = []
    for parser in parsers:
        command = ["go", "run", ".", parser["name"], "../../../controls/mp4/red-av.mp4"]
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
              "control": "controls/mp4/red-av.mp4",
              "control_sha256": hashlib.sha256(CONTROL.read_bytes()).hexdigest(),
              "control_meaning": "Progressive MP4: isom major brand, 2x2 H.264 frame, one-second AAC track, title Parsarium, two tracks",
              "third_party": results}
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Go MP4 packages passed")
    if count != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
