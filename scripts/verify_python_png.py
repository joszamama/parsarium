"""Verify pinned Python PNG package APIs against valid local PNG controls."""

import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "png"
ADAPTER = ROOT / "adapters" / "python" / "png" / "main.py"
STANDARD_ADAPTER = ADAPTER.with_name("standard.py")
PYTHON = ADAPTER.parent / ".venv" / "bin" / "python"


def pkg_config(variable: str, package: str) -> str | None:
    run = subprocess.run(["pkg-config", variable, package], text=True, capture_output=True)
    return run.stdout.strip() if run.returncode == 0 else None


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    prefix = pkg_config("--variable=prefix", "MagickWand")
    results = []
    for parser in parsers:
        path = ROOT / parser["control"]
        command = [str(PYTHON), str(ADAPTER), parser["name"], str(path)]
        env = os.environ.copy()
        if parser["name"] == "Wand" and prefix:
            env["MAGICK_HOME"] = prefix
        output = None
        error = None
        try:
            run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                                 text=True, timeout=120, check=True)
            output = json.loads(run.stdout.strip().splitlines()[-1])
            passed = output == parser["expected_output"]
            if not passed:
                error = "output differs from control expectation"
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({"package": parser["name"], "version": parser["version"],
                        "scope": parser["scope"], "command": " ".join(command),
                        "pass": passed, "output": output, "error": error})
    python_version = subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                    text=True, check=True).stdout.strip()
    controls = {parser["control"] for parser in parsers}
    standard = json.loads((CELL / "standard.json").read_text())["verified_apis"][0]
    standard_command = [str(PYTHON), str(STANDARD_ADAPTER),
                        str(ROOT / standard["control"])]
    standard_output = None
    standard_error = None
    try:
        standard_run = subprocess.run(standard_command, cwd=ROOT, capture_output=True,
                                      text=True, timeout=30, check=True)
        standard_output = json.loads(standard_run.stdout.strip().splitlines()[-1])
        standard_passed = standard_output == standard["expected"]
        if not standard_passed:
            standard_error = "output differs from control expectation"
    except Exception as exc:
        standard_passed = False
        standard_error = str(exc)
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "python": python_version,
        "libvips": pkg_config("--modversion", "vips"),
        "magickwand": pkg_config("--modversion", "MagickWand"),
        "controls": {control: hashlib.sha256((ROOT / control).read_bytes()).hexdigest()
                     for control in sorted(controls)},
        "control_meaning": "2x1 RGBA PNG, opaque red then green; the metadata variant adds a Title=Parsarium tEXt chunk",
        "third_party": results,
        "runtime": {"api": standard["api"], "command": " ".join(standard_command),
                    "pass": standard_passed, "output": standard_output,
                    "error": standard_error},
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Python PNG packages and {int(standard_passed)}/1 bundled API passed")
    if count != len(results) or not standard_passed:
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
