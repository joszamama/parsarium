"""Run pinned Go MP3 and ID3v2 parsers against a valid tagged MPEG-1 control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "mp3"
MODULE = ROOT / "adapters" / "go" / "mp3"
CONTROL = ROOT / "controls" / "mp3" / "id3v2-tagged-tone-44k.mp3"


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    results = []
    for parser in parsers:
        command = ["go", "run", ".", parser["name"], "../../../controls/mp3/id3v2-tagged-tone-44k.mp3"]
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
              "control": "controls/mp3/id3v2-tagged-tone-44k.mp3",
              "control_sha256": hashlib.sha256(CONTROL.read_bytes()).hexdigest(),
              "control_meaning": "ID3v2.3 title Parsarium, artist Control, album Pilot; one second of 440 Hz mono MPEG-1 Layer III at 44100 Hz",
              "control_selection": "The earlier 8000 Hz MPEG-2.5 control is retained for JavaScript; this tagged 44100 Hz MPEG-1 control exercises decoders that do not support MPEG-2.5.",
              "third_party": results}
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Go MP3 with ID3v2 packages passed")
    if count != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
