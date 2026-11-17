"""Verify pinned Python MP3/ID3v2 readers on a valid tagged local control."""

import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "mp3"
PYTHON = ROOT / "adapters" / "python" / "mp3" / ".venv" / "bin" / "python"
ADAPTER = ROOT / "adapters" / "python" / "mp3" / "main.py"


def check(command, expected):
    try:
        result = subprocess.run(command, cwd=ROOT, env=os.environ.copy(),
                                capture_output=True, text=True, timeout=120, check=True)
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
    control = "controls/mp3/id3v2-tagged-tone.mp3"
    ffprobe = subprocess.run(["ffprobe", "-version"], capture_output=True,
                             text=True, check=True).stdout.splitlines()[0]
    libsndfile = subprocess.run([str(PYTHON), "-c",
                                 "import soundfile; print(soundfile.__libsndfile_version__)"],
                                capture_output=True, text=True, check=True).stdout.strip()
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                 text=True, check=True).stdout.strip(),
        "external_ffprobe": ffprobe,
        "libsndfile_version": libsndfile,
        "controls": {control: hashlib.sha256((ROOT / control).read_bytes()).hexdigest()},
        "control_meaning": "valid one-second 8 kHz mono MP3 with ID3v2.3 title Parsarium, artist Control, album Pilot",
        "third_party": rows,
        "runtime": [],
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{sum(row['pass'] for row in rows)}/{len(rows)} Python MP3/ID3v2 package paths passed; "
          "no CPython MP3/ID3v2 API documented")
    for row in rows:
        if not row["pass"]:
            print(row["package"], row["error"], row["output"])
    if not all(row["pass"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
