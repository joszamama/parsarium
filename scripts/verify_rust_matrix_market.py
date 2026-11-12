"""Build pinned Rust Matrix Market adapters and run valid coordinate controls."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "rust" / "matrix_market"
ADAPTER = ROOT / "adapters" / "rust" / "matrix_market"
MAIN = ADAPTER / "target" / "debug" / "parsarium-rust-matrix-market"
HYBIT = ADAPTER / "hybit" / "target" / "debug" / "parsarium-rust-hybit-matrix-market"


def control_checksums(path: Path) -> dict[str, str]:
    files = sorted(path.rglob("*")) if path.is_dir() else [path]
    return {str(file.relative_to(ROOT)): hashlib.sha256(file.read_bytes()).hexdigest()
            for file in files if file.is_file()}


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    subprocess.run(["cargo", "build", "--locked"], cwd=ADAPTER, check=True, timeout=600)
    subprocess.run(["cargo", "build", "--locked"], cwd=ADAPTER / "hybit", check=True, timeout=600)
    controls = {}
    results = []
    for parser in parsers:
        control = parser["control"]
        controls.update(control_checksums(ROOT / control))
        binary = HYBIT if parser["name"] in {"hybit", "hybit-matrix"} else MAIN
        command = [str(binary), parser["name"], str(ROOT / control)]
        output = None
        error = None
        try:
            run = subprocess.run(command, cwd=ROOT, text=True, capture_output=True,
                                 timeout=60, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from valid Matrix Market control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({
            "package": parser["name"], "version": parser["version"],
            "scope": parser["scope"], "control": control,
            "command": f"{binary.relative_to(ROOT)} {parser['name']} {control}",
            "pass": passed, "output": output, "error": error,
        })
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "rustc": subprocess.check_output(["rustc", "--version"], text=True).strip(),
        "cargo": subprocess.check_output(["cargo", "--version"], text=True).strip(),
        "build_commands": [
            "cargo build --locked (from adapters/rust/matrix_market)",
            "cargo build --locked (from adapters/rust/matrix_market/hybit)",
        ],
        "control_sha256": controls,
        "control_meaning": "Valid 2x3 coordinate real general, 3x3 coordinate real symmetric, and gzip-compressed 10x coordinate integer general Matrix Market controls. The symmetric control contains three diagonal entries; the 10x directory also contains valid feature and barcode tables.",
        "third_party": results,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Rust Matrix Market crate paths passed")
    if passed != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
