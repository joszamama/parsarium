"""Build pinned Rust MP3/ID3v2 adapters and run the valid local control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "rust" / "mp3_id3v2"
ADAPTER = ROOT / "adapters" / "rust" / "mp3_id3v2"
BINARY = ADAPTER / "target" / "debug" / "parsarium-rust-mp3-id3v2"


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    subprocess.run(["cargo", "build", "--locked"], cwd=ADAPTER, check=True, timeout=600)
    controls = {}
    results = []
    for parser in parsers:
        control = parser["control"]
        path = ROOT / control
        controls[control] = hashlib.sha256(path.read_bytes()).hexdigest()
        output = None
        error = None
        try:
            run = subprocess.run([str(BINARY), parser["name"], str(path)], cwd=ROOT,
                                 text=True, capture_output=True, timeout=30, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from valid MP3 with ID3v2 control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({
            "package": parser["name"], "version": parser["version"],
            "scope": parser["scope"], "control": control,
            "command": f"adapters/rust/mp3_id3v2/target/debug/parsarium-rust-mp3-id3v2 {parser['name']} {control}",
            "pass": passed, "output": output, "error": error,
        })
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "rustc": subprocess.check_output(["rustc", "--version"], text=True).strip(),
        "cargo": subprocess.check_output(["cargo", "--version"], text=True).strip(),
        "build_command": "cargo build --locked (from adapters/rust/mp3_id3v2)",
        "control_sha256": controls,
        "control_meaning": "Valid ID3v2.3 tagged mono MPEG Layer III audio with title Parsarium, artist Control, album Pilot, and 8 kHz sample rate",
        "third_party": results,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Rust MP3 with ID3v2 crates passed")
    if passed != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
