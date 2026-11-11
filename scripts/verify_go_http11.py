"""Run pinned Go HTTP/1.1 readers against valid local wire controls."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "http11"
MODULE = ROOT / "adapters" / "go" / "http11"
REQUEST = ROOT / "controls" / "http11" / "request.http"
RESPONSE = ROOT / "controls" / "http11" / "response.http"
STANDARD_EXPECTED = {
    "request": {"method": "GET", "target": "/parsarium?x=1", "host": "example.test", "proto": "HTTP/1.1"},
    "response": {"status": 200, "body": "parsarium", "proto": "HTTP/1.1"},
}


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    results = []
    for parser in parsers:
        command = ["go", "run", ".", parser["name"], "../../../controls/http11/request.http"]
        output = None
        error = None
        try:
            run = subprocess.run(command, cwd=MODULE, text=True, capture_output=True, timeout=120, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({"package": parser["name"], "module": parser["module"],
                        "version": parser["version"], "scope": parser["scope"],
                        "command": " ".join(command), "pass": passed,
                        "output": output, "error": error})
    standard_command = ["go", "run", "adapters/go/http11_std.go",
                        "controls/http11/request.http", "controls/http11/response.http"]
    standard_output = None
    standard_error = None
    try:
        run = subprocess.run(standard_command, cwd=ROOT, text=True, capture_output=True, timeout=60, check=True)
        standard_output = json.loads(run.stdout.strip().splitlines()[-1])
        standard_pass = standard_output == STANDARD_EXPECTED
        if not standard_pass:
            standard_error = "output differs from control expectation"
    except Exception as exc:
        standard_pass = False
        standard_error = str(exc)
    version = subprocess.run(["go", "version"], text=True, capture_output=True, check=True).stdout.strip()
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "go": version,
              "controls": {"request": "controls/http11/request.http", "response": "controls/http11/response.http"},
              "control_sha256": {"request": hashlib.sha256(REQUEST.read_bytes()).hexdigest(),
                                 "response": hashlib.sha256(RESPONSE.read_bytes()).hexdigest()},
              "control_meaning": "GET /parsarium?x=1 with Host example.test; HTTP/1.1 200 OK with parsarium body",
              "third_party": results,
              "runtime": {"apis": ["net/http.ReadRequest", "net/http.ReadResponse"],
                          "command": " ".join(standard_command), "pass": standard_pass,
                          "output": standard_output, "error": standard_error}}
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Go HTTP/1.1 packages and {int(standard_pass)}/1 standard adapter passed")
    if count != len(results) or not standard_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
