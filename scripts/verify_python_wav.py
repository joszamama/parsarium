"""Verify pinned Python WAV readers and CPython wave on a valid PCM control."""

import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "wav"
ADAPTER = ROOT / "adapters" / "python" / "wav" / "main.py"
STANDARD = ADAPTER.with_name("standard.py")
PYTHON = ADAPTER.parent / ".venv" / "bin" / "python"


def check(command, expected, env=None):
    try:
        run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                             text=True, timeout=120, check=True)
        output = json.loads(run.stdout.strip().splitlines()[-1])
        return output == expected, output, None if output == expected else "unexpected output"
    except subprocess.CalledProcessError as exc:
        return False, None, exc.stderr.strip()[-2000:] or str(exc)
    except Exception as exc:
        return False, None, str(exc)


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    standard = json.loads((CELL / "standard.json").read_text())["verified_apis"][0]
    rows = []
    for parser in parsers:
        command = [str(PYTHON), str(ADAPTER), parser["name"],
                   str(ROOT / parser["control"])]
        env = os.environ.copy()
        if parser["name"] == "pygame":
            env["SDL_AUDIODRIVER"] = "dummy"
        passed, output, error = check(command, parser["expected_output"], env)
        rows.append({"package": parser["name"], "version": parser["version"],
                     "scope": parser["scope"], "command": " ".join(command),
                     "pass": passed, "output": output, "error": error})
    standard_command = [str(PYTHON), str(STANDARD), str(ROOT / standard["control"])]
    standard_passed, standard_output, standard_error = check(standard_command,
                                                             standard["expected"])
    python_version = subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                    text=True, check=True).stdout.strip()
    native_version = subprocess.run([str(PYTHON), "-c",
                                     "import soundfile; print(soundfile.__libsndfile_version__)"],
                                    capture_output=True, text=True, check=True).stdout.strip()
    control = standard["control"]
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "python": python_version,
        "libsndfile_version": native_version,
        "controls": {control: hashlib.sha256((ROOT / control).read_bytes()).hexdigest()},
        "control_meaning": "valid 8 kHz mono 16-bit PCM RIFF/WAVE with samples 0, +1000, -1000, 0",
        "third_party": rows,
        "runtime": {"api": standard["api"], "command": " ".join(standard_command),
                    "pass": standard_passed, "output": standard_output,
                    "error": standard_error},
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{sum(x['pass'] for x in rows)}/{len(rows)} Python WAV packages and "
          f"{int(standard_passed)}/1 standard API passed")
    for row in rows:
        if not row["pass"]:
            print(row["package"], row["error"])
    if not all(x["pass"] for x in rows) or not standard_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
