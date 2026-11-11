"""Verify pinned Python MP4 readers against one valid local audiovisual control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "mp4"
PYTHON = ROOT / "adapters" / "python" / "mp4" / ".venv" / "bin" / "python"
ADAPTER = ROOT / "adapters" / "python" / "mp4" / "main.py"


def check(command, expected):
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                timeout=120, check=True)
        output = json.loads(result.stdout.strip().splitlines()[-1])
        return output == expected, output, None if output == expected else "unexpected output"
    except subprocess.CalledProcessError as exc:
        return False, None, exc.stderr.strip()[-2000:] or str(exc)
    except Exception as exc:
        return False, None, str(exc)


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    rows = []
    for parser in parsers:
        command = [str(PYTHON), str(ADAPTER), parser["name"],
                   str(ROOT / parser["control"])]
        passed, output, error = check(command, parser["expected_output"])
        rows.append({"package": parser["name"], "version": parser["version"],
                     "scope": parser["scope"], "command": " ".join(command),
                     "pass": passed, "output": output, "error": error})
    control = "controls/mp4/red-av.mp4"
    ffprobe = subprocess.run(["ffprobe", "-version"], capture_output=True,
                             text=True, check=True).stdout.splitlines()[0]
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                 text=True, check=True).stdout.strip(),
        "external_ffprobe": ffprobe,
        "controls": {control: hashlib.sha256((ROOT / control).read_bytes()).hexdigest()},
        "control_meaning": "valid one-second MP4 with one 2x2 red H.264 frame, 8 kHz AAC audio, title Parsarium, and creation timestamp",
        "third_party": rows,
        "runtime": [],
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{sum(row['pass'] for row in rows)}/{len(rows)} Python MP4 package paths passed; "
          "no CPython MP4 API documented")
    for row in rows:
        if not row["pass"]:
            print(row["package"], row["error"], row["output"])
    if not all(row["pass"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
