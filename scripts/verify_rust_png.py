"""Build pinned Rust PNG adapters and run each against a valid local control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "rust" / "png"
MODULE = ROOT / "adapters" / "rust" / "png"
BINARY = MODULE / "target" / "debug" / "parsarium-rust-png"


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    subprocess.run(["cargo", "build", "--locked"], cwd=MODULE, check=True, timeout=300)
    controls = {}
    results = []
    for parser in parsers:
        control = parser["control"]
        path = ROOT / control
        controls[control] = hashlib.sha256(path.read_bytes()).hexdigest()
        command = [str(BINARY), parser["name"], str(path)]
        output = None
        error = None
        try:
            run = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                 timeout=30, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from valid PNG control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({
            "package": parser["name"], "version": parser["version"],
            "scope": parser["scope"], "control": control,
            "command": f"adapters/rust/png/target/debug/parsarium-rust-png {parser['name']} {control}",
            "pass": passed, "output": output, "error": error,
        })
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "rustc": subprocess.check_output(["rustc", "--version"], text=True).strip(),
        "cargo": subprocess.check_output(["cargo", "--version"], text=True).strip(),
        "build_command": "cargo build --locked (from adapters/rust/png)",
        "control_sha256": controls,
        "control_meaning": "Valid 2-by-1 RGBA PNG with opaque red and green pixels; tagged variant has Title tEXt chunk",
        "third_party": results,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Rust PNG crates passed")
    if passed != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
