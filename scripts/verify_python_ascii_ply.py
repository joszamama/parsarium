"""Run every pinned Python ASCII PLY adapter on the valid local triangle."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data/python/ascii_ply"
PYTHON = ROOT / "adapters/python/ascii_ply/.venv/bin/python"
ADAPTER = ROOT / "adapters/python/ascii_ply/main.py"


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    results = []
    for parser in parsers:
        command = [str(PYTHON), str(ADAPTER), parser["name"],
                   str(ROOT / parser["control"])]
        observed, error = None, None
        try:
            run = subprocess.run(command, cwd=ROOT, capture_output=True,
                                 text=True, timeout=120, check=True)
            observed = json.loads(run.stdout.strip().splitlines()[-1])
            passed = observed == parser["expected_output"]
            if not passed:
                error = "output differs from the ASCII PLY triangle control"
        except subprocess.CalledProcessError as exc:
            passed = False
            error = exc.stderr.strip()[-2000:] or str(exc)
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({"package": parser["name"], "version": parser["version"],
                        "scope": parser["scope"], "command": " ".join(command),
                        "pass": passed, "output": observed, "error": error})
    python_version = subprocess.run([str(PYTHON), "--version"], check=True,
                                    capture_output=True, text=True).stdout.strip()
    brew = subprocess.run(["brew", "list", "--versions", "assimp"],
                          capture_output=True, text=True, check=False)
    control = ROOT / "controls/ascii_ply/triangle.ply"
    lock = ROOT / "adapters/python/ascii_ply/requirements.lock"
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "python": python_version,
        "system_assimp": brew.stdout.strip() or None,
        "controls": {str(control.relative_to(ROOT)): hashlib.sha256(control.read_bytes()).hexdigest()},
        "requirements_lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
        "third_party": results, "runtime": [],
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Python ASCII PLY packages passed")
    if count != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
