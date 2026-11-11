"""Run pinned Python and CPython HTTP/1.1 parsers on valid local controls."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "http11"
ADAPTER = ROOT / "adapters" / "python" / "http11"
PYTHON = ADAPTER / ".venv" / "bin" / "python"
PYTHON_310 = ADAPTER / ".venv310" / "bin" / "python"


def check(command, expected):
    try:
        process = subprocess.run(command, cwd=ROOT, capture_output=True,
                                 text=True, timeout=30, check=True)
        output = json.loads(process.stdout.strip().splitlines()[-1])
        return output == expected, output, None if output == expected else "unexpected output"
    except subprocess.CalledProcessError as error:
        return False, None, error.stderr.strip()[-1500:] or str(error)
    except Exception as error:
        return False, None, str(error)


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    standard = json.loads((CELL / "standard.json").read_text())
    third_party = []
    for parser in parsers:
        python = PYTHON_310 if parser["name"] == "http-parser" else PYTHON
        command = [str(python), str(ADAPTER / "main.py"), parser["name"],
                   str(ROOT / parser["control"])]
        passed, output, error = check(command, parser["expected_output"])
        third_party.append({"package": parser["name"], "version": parser["version"],
                            "scope": parser["scope"], "command": " ".join(command),
                            "pass": passed, "output": output, "error": error})

    runtime = []
    for api in standard["verified_apis"]:
        command = [str(PYTHON), str(ADAPTER / "standard.py"), api["name"],
                   str(ROOT / api["control"])]
        passed, output, error = check(command, api["expected"])
        runtime.append({"api": api["name"], "command": " ".join(command),
                        "pass": passed, "output": output, "error": error})

    controls = sorted({row["control"] for row in parsers}
                      | {row["control"] for row in standard["verified_apis"]})
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                 text=True, check=True).stdout.strip(),
        "python_legacy": subprocess.run([str(PYTHON_310), "--version"], capture_output=True,
                                        text=True, check=True).stdout.strip(),
        "controls": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                     for path in controls},
        "control_meaning": "Valid HTTP/1.1 GET request with Host, custom field and CRLF framing; valid 200 response with Content-Length 9 and a nine-byte text body",
        "third_party": third_party,
        "runtime": runtime,
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{sum(row['pass'] for row in third_party)}/{len(third_party)} Python HTTP/1.1 packages; "
          f"{sum(row['pass'] for row in runtime)}/{len(runtime)} CPython APIs")
    for row in third_party + runtime:
        if not row["pass"]:
            print(row.get("package", row.get("api")), row["error"], row["output"])
    if not all(row["pass"] for row in third_party + runtime):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
