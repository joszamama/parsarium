"""Run pinned Go PNG package adapters and Go image/png on a valid control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "png"
MODULE = ROOT / "adapters" / "go" / "png"
CONTROL = ROOT / "controls" / "png" / "red-green.png"
PIXELS = {"width": 2, "height": 1, "rgba": [255, 0, 0, 255, 0, 255, 0, 255]}
CHUNKS = {"width": 2, "height": 1, "chunks": ["IHDR", "IDAT", "IEND"]}
IOSPNG = {"width": 2, "height": 1, "output_bytes": 71}
DIMENSIONS = {"width": 2, "height": 1}
STANDARD = {
    "decode": PIXELS,
    "config": DIMENSIONS,
    "generic": {"format": "png", **DIMENSIONS},
}


def expected(parser: dict) -> dict:
    if parser["scope"] == "chunks+dimensions":
        return CHUNKS
    if parser["scope"] == "dimensions+converted_bytes":
        return IOSPNG
    if parser["scope"] == "dimensions":
        return DIMENSIONS
    return PIXELS


def run(command: list[str], cwd: Path, expected_output: dict) -> tuple[bool, dict | None, str | None]:
    try:
        completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=60, check=True)
        output = json.loads(completed.stdout.strip().splitlines()[-1])
        passed = output == expected_output
        return passed, output, None if passed else "output differs from PNG control"
    except Exception as error:
        return False, None, str(error)


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    third_party = []
    for parser in parsers:
        command = ["go", "run", ".", parser["name"], "../../../controls/png/red-green.png"]
        passed, output, error = run(command, MODULE, expected(parser))
        third_party.append({
            "package": parser["name"], "module": parser["module"], "version": parser["version"],
            "scope": parser["scope"], "command": " ".join(command), "pass": passed,
            "output": output, "error": error,
        })
    standard_command = ["go", "run", "adapters/go/png_std.go", "controls/png/red-green.png"]
    passed, output, error = run(standard_command, ROOT, STANDARD)
    runtime = {"command": " ".join(standard_command), "pass": passed, "output": output, "error": error}
    version = subprocess.run(["go", "version"], text=True, capture_output=True, check=True).stdout.strip()
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(), "platform": platform.platform(), "go": version,
        "control": "controls/png/red-green.png", "control_sha256": hashlib.sha256(CONTROL.read_bytes()).hexdigest(),
        "expected_by_scope": {"pixels": PIXELS, "chunks+dimensions": CHUNKS,
                              "dimensions+converted_bytes": IOSPNG, "dimensions": DIMENSIONS},
        "third_party": third_party, "runtime": runtime,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in third_party)
    print(f"{count}/{len(third_party)} Go PNG packages passed; standard image/png {'passed' if passed else 'failed'}")
    if count != len(third_party) or not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
