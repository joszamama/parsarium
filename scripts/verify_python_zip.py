"""Verify pinned Python ZIP APIs and CPython runtime APIs on valid controls."""

import hashlib
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "zip"
ADAPTER = ROOT / "adapters" / "python" / "zip" / "main.py"
STANDARD = ADAPTER.with_name("standard.py")
PYTHON = ADAPTER.parent / ".venv" / "bin" / "python"


def check(command, expected):
    try:
        run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                             timeout=120, check=True)
        output = json.loads(run.stdout.strip().splitlines()[-1])
        return output == expected, output, None if output == expected else "unexpected output"
    except subprocess.CalledProcessError as exc:
        return False, None, exc.stderr.strip()[-2000:] or str(exc)
    except Exception as exc:
        return False, None, str(exc)


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    standard = json.loads((CELL / "standard.json").read_text())["verified_apis"]
    rows = []
    runtime = []
    for parser in parsers:
        command = [str(PYTHON), str(ADAPTER), parser["name"],
                   str(ROOT / parser["control"])]
        passed, output, error = check(command, parser["expected_output"])
        rows.append({"package": parser["name"], "version": parser["version"],
                     "scope": parser["scope"], "command": " ".join(command),
                     "pass": passed, "output": output, "error": error})
    for entry in standard:
        command = [str(PYTHON), str(STANDARD), entry["api"],
                   str(ROOT / entry["control"])]
        passed, output, error = check(command, entry["expected"])
        runtime.append({"api": entry["api"], "command": " ".join(command),
                        "pass": passed, "output": output, "error": error})
    controls = {parser["control"] for parser in parsers} | {entry["control"] for entry in standard}
    python_version = subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                    text=True, check=True).stdout.strip()
    unzip_path = shutil.which("unzip")
    unzip_version = None
    if unzip_path:
        run = subprocess.run([unzip_path, "-v"], capture_output=True, text=True)
        if run.returncode == 0:
            unzip_version = run.stdout.splitlines()[0]
    libarchive_version = subprocess.run(
        [str(PYTHON), "-c", "import libarchive.ffi; print(libarchive.ffi.version_number())"],
        capture_output=True, text=True, check=True).stdout.strip()
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "python": python_version,
        "unzip_utility": unzip_path, "unzip_version": unzip_version,
        "libarchive_version_number": libarchive_version,
        "controls": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                     for name in sorted(controls)},
        "control_meaning": "valid one-entry ZIP controls: DEFLATE text, Zstandard text, and Python source for zipimport",
        "third_party": rows, "runtime": runtime,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{sum(x['pass'] for x in rows)}/{len(rows)} Python ZIP packages and "
          f"{sum(x['pass'] for x in runtime)}/{len(runtime)} standard APIs passed")
    for row in rows + runtime:
        if not row["pass"]:
            print(row.get("package", row.get("api")), row["error"])
    if not all(row["pass"] for row in rows + runtime):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
