"""Run pinned Go ZIP package adapters and Go archive/zip on one valid control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "zip"
MODULE = ROOT / "adapters" / "go" / "zip"
CONTROL = ROOT / "controls" / "zip" / "hello.zip"
EXPECTED = {"name": "hello.txt", "text": "parsarium\n"}


def run(command: list[str], cwd: Path) -> tuple[bool, dict | None, str | None]:
    try:
        completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=30, check=True)
        output = json.loads(completed.stdout.strip().splitlines()[-1])
        return output == EXPECTED, output, None if output == EXPECTED else "output differs from ZIP control"
    except Exception as error:
        return False, None, str(error)


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    third_party = []
    for parser in parsers:
        command = ["go", "run", ".", parser["name"], "../../../controls/zip/hello.zip"]
        pass_, output, error = run(command, MODULE)
        third_party.append({
            "package": parser["name"], "module": parser["module"], "version": parser["version"],
            "scope": parser["scope"], "command": " ".join(command), "pass": pass_, "output": output, "error": error,
        })
    standard_command = ["go", "run", "adapters/go/zip_std.go", "controls/zip/hello.zip"]
    pass_, output, error = run(standard_command, ROOT)
    runtime = {"command": " ".join(standard_command), "pass": pass_, "output": output, "error": error}
    version = subprocess.run(["go", "version"], text=True, capture_output=True, check=True).stdout.strip()
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(), "platform": platform.platform(), "go": version,
        "control": "controls/zip/hello.zip", "control_sha256": hashlib.sha256(CONTROL.read_bytes()).hexdigest(),
        "expected": EXPECTED, "third_party": third_party, "runtime": runtime,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in third_party)
    print(f"{count}/{len(third_party)} Go ZIP packages passed; standard archive/zip {'passed' if pass_ else 'failed'}")
    if count != len(third_party) or not pass_:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
