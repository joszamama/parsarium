"""Build pinned Rust ZIP adapters and run each against a valid local control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "rust" / "zip"
ADAPTER = ROOT / "adapters" / "rust" / "zip"
BINARY = ADAPTER / "target" / "debug" / "parsarium-rust-zip"


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
                error = "output differs from valid ZIP control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({
            "package": parser["name"], "version": parser["version"],
            "scope": parser["scope"], "control": control,
            "command": f"adapters/rust/zip/target/debug/parsarium-rust-zip {parser['name']} {control}",
            "pass": passed, "output": output, "error": error,
        })
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "rustc": subprocess.check_output(["rustc", "--version"], text=True).strip(),
        "cargo": subprocess.check_output(["cargo", "--version"], text=True).strip(),
        "build_command": "cargo build --locked (from adapters/rust/zip)",
        "control_sha256": controls,
        "control_meaning": "Valid one-entry DEFLATE ZIP: hello.txt contains parsarium followed by newline",
        "third_party": results,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Rust ZIP crates passed")
    if passed != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
