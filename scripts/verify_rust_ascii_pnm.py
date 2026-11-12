"""Build pinned Rust ASCII PNM adapters and run valid P1, P2, and P3 controls."""

import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "rust" / "ascii_pnm"
ADAPTER = ROOT / "adapters" / "rust" / "ascii_pnm"
MAIN = ADAPTER / "target" / "debug" / "parsarium-rust-ascii-pnm"
PNM = ADAPTER / "pnm_nightly" / "target" / "debug" / "parsarium-rust-pnm-nightly"
FLTK = ADAPTER / "fltk_native" / "target" / "debug" / "parsarium-rust-fltk-pnm"


def build() -> None:
    subprocess.run(["cargo", "build", "--locked"], cwd=ADAPTER, check=True, timeout=600)
    subprocess.run(["cargo", "build", "--locked"], cwd=ADAPTER / "pnm_nightly",
                   env={**os.environ, "RUSTC_BOOTSTRAP": "1"}, check=True, timeout=600)
    subprocess.run(["cargo", "build", "--locked"], cwd=ADAPTER / "fltk_native",
                   check=True, timeout=600)


def command(name: str, control: str) -> list[str]:
    if name == "include-pnm":
        return [sys.executable, str(ROOT / "scripts" / "run_rust_include_pnm.py"), control]
    if name == "pnm":
        return [str(PNM), control]
    if name == "fltk":
        return [str(FLTK), control]
    return [str(MAIN), name, control]


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    build()
    controls = {}
    results = []
    for parser in parsers:
        control = parser["control"]
        path = ROOT / control
        controls[control] = hashlib.sha256(path.read_bytes()).hexdigest()
        cmd = command(parser["name"], str(path))
        output = None
        error = None
        try:
            run = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True,
                                 timeout=60, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from valid ASCII PNM control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({
            "package": parser["name"], "version": parser["version"],
            "scope": parser["scope"], "control": control,
            "command": " ".join(command(parser["name"], control)),
            "pass": passed, "output": output, "error": error,
        })
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "rustc": subprocess.check_output(["rustc", "--version"], text=True).strip(),
        "cargo": subprocess.check_output(["cargo", "--version"], text=True).strip(),
        "build_commands": [
            "cargo build --locked (from adapters/rust/ascii_pnm)",
            "RUSTC_BOOTSTRAP=1 cargo build --locked (from adapters/rust/ascii_pnm/pnm_nightly)",
            "cargo build --locked (from adapters/rust/ascii_pnm/fltk_native)",
            "include-pnm is compiled on demand by scripts/run_rust_include_pnm.py",
        ],
        "control_sha256": controls,
        "control_meaning": "Valid ASCII Netpbm controls: red/green 2x1 P3, black/white 2x1 P2, and a generated P1 QR carrying 'Parsarium P1 control'. The compact P3 variant has ordinary single spaces and no terminal newline for rusty-ppm's narrower parser.",
        "third_party": results,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Rust ASCII PNM crates passed")
    if passed != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
