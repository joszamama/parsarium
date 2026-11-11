"""Run pinned Python Matrix Market readers on valid local controls."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "matrix_market"
ADAPTER = ROOT / "adapters" / "python" / "matrix_market"
PYTHON = ADAPTER / ".venv" / "bin" / "python"
PYTHON_310 = ADAPTER / ".venv310" / "bin" / "python"


def control_digest(path):
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    return {child.name: hashlib.sha256(child.read_bytes()).hexdigest()
            for child in sorted(path.iterdir()) if child.is_file()}


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    third_party = []
    for parser in parsers:
        python = PYTHON_310 if parser["name"] in {"scprep", "mtl5"} else PYTHON
        command = [str(python), str(ADAPTER / "main.py"), parser["name"],
                   str(ROOT / parser["control"])]
        try:
            process = subprocess.run(command, cwd=ROOT, capture_output=True,
                                     text=True, timeout=45, check=True)
            output = json.loads(process.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            error = None if passed else "unexpected format-aware result"
        except subprocess.CalledProcessError as failure:
            output, passed = None, False
            error = failure.stderr.strip()[-1200:] or str(failure)
        except Exception as failure:
            output, passed, error = None, False, str(failure)
        third_party.append({"package": parser["name"], "version": parser["version"],
                            "scope": parser["scope"], "command": " ".join(command),
                            "pass": passed, "output": output, "error": error})

    controls = sorted({parser["control"] for parser in parsers})
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                 text=True, check=True).stdout.strip(),
        "python_legacy": subprocess.run([str(PYTHON_310), "--version"], capture_output=True,
                                        text=True, check=True).stdout.strip(),
        "controls": {path: control_digest(ROOT / path)
                     for path in controls},
        "control_meaning": "Valid NIST Matrix Market coordinate controls: a 2×3 real matrix, a 3×3 graph adjacency matrix, a 3×3 real symmetric diagonal matrix, and a 10x directory with a compressed 2×3 integer matrix plus feature and barcode annotations",
        "third_party": third_party,
        "runtime": [],
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in third_party)
    print(f"{passed}/{len(third_party)} Python Matrix Market packages")
    for row in third_party:
        if not row["pass"]:
            print(row["package"], row["error"], row["output"])
    if passed != len(third_party):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
