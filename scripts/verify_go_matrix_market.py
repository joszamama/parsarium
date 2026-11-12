"""Run pinned Go Matrix Market adapters against valid local controls."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "matrix_market"
MODULE = ROOT / "adapters" / "go" / "matrix_market"


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    results = []
    controls = {}
    for parser in parsers:
        control = parser["control"]
        path = ROOT / control
        controls[control] = hashlib.sha256(path.read_bytes()).hexdigest()
        for companion in parser.get("control_companions", []):
            controls[companion] = hashlib.sha256((ROOT / companion).read_bytes()).hexdigest()
        command = ["go", "run", ".", parser["name"], str(path)]
        output = None
        error = None
        try:
            run = subprocess.run(command, cwd=MODULE, text=True, capture_output=True,
                                 timeout=180, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({
            "package": parser["name"], "module": parser["module"],
            "version": parser["version"], "scope": parser["scope"],
            "control": control, "command": " ".join(command),
            "pass": passed, "output": output, "error": error,
        })
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "go": subprocess.check_output(["go", "version"], cwd=MODULE, text=True).strip(),
        "control_sha256": controls,
        "control_meaning": "Valid Matrix Market coordinate real general matrices and a pattern symmetric graph control; the graph controls have three vertices and two edges",
        "third_party": results,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in results)
    print(f"{passed}/{len(results)} Go Matrix Market packages passed")
    if passed != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
