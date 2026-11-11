"""Verify twenty pinned Python PDF package paths on one valid local PDF."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "pdf"
ADAPTERS = ROOT / "adapters" / "python" / "pdf"


def run(command, expected):
    try:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                timeout=120, check=True)
        output = json.loads(result.stdout.strip().splitlines()[-1])
        return output == expected, output, None if output == expected else "unexpected output"
    except subprocess.CalledProcessError as exc:
        return False, None, exc.stderr.strip()[-2000:] or str(exc)
    except Exception as exc:
        return False, None, str(exc)


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    rows = []
    for parser in parsers:
        name = parser["name"]
        env = ".venv_pdfx" if name == "pdfx" else ".venv_slate" if name == "slate3k" else ".venv"
        command = [str(ADAPTERS / env / "bin" / "python"),
                   str(ROOT / parser["adapter"]), str(ROOT / parser["control"])]
        if name not in ("pdfx", "slate3k"):
            command.insert(2, name)
        passed, output, error = run(command, parser["expected_output"])
        rows.append({"package": name, "version": parser["version"], "scope": parser["scope"],
                     "command": " ".join(command), "pass": passed,
                     "output": output, "error": error})
    control = "controls/pdf/one-page.pdf"
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": subprocess.run([str(ADAPTERS / ".venv" / "bin" / "python"), "--version"],
                                 capture_output=True, text=True, check=True).stdout.strip(),
        "external_poppler": subprocess.run(["pdftoppm", "-v"], capture_output=True,
                                           text=True, check=True).stderr.strip().splitlines()[0],
        "controls": {control: hashlib.sha256((ROOT / control).read_bytes()).hexdigest()},
        "control_meaning": "valid one-page PDF 1.4 with letter-size MediaBox, title Parsarium PDF control, and text Parsarium",
        "third_party": rows,
        "runtime": [],
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"{sum(row['pass'] for row in rows)}/{len(rows)} Python PDF packages passed; "
          "no CPython PDF API documented")
    for row in rows:
        if not row["pass"]:
            print(row["package"], row["error"], row["output"])
    if not all(row["pass"] for row in rows):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
