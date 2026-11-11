"""Verify pinned Python ASCII PNM APIs with valid local P1/P2/P3 controls."""

import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "ascii_pnm"
ADAPTER = ROOT / "adapters" / "python" / "ascii_pnm" / "main.py"
STANDARD_ADAPTER = ADAPTER.with_name("standard.py")
PYTHON = ADAPTER.parent / ".venv" / "bin" / "python"


def pkg_config(variable: str, package: str) -> str | None:
    try:
        run = subprocess.run(["pkg-config", variable, package], text=True, capture_output=True)
        return run.stdout.strip() if run.returncode == 0 else None
    except FileNotFoundError:
        return None


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    prefix = pkg_config("--variable=prefix", "MagickWand")
    results = []
    for parser in parsers:
        command = [str(PYTHON), str(ADAPTER), parser["name"],
                   str(ROOT / parser["control"])]
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
        except subprocess.CalledProcessError as exc:
            passed = False
            error = exc.stderr.strip()[-2000:] or str(exc)
        except Exception as exc:
            passed = False
            error = str(exc)
        results.append({"package": parser["name"], "version": parser["version"],
                        "scope": parser["scope"], "command": " ".join(command),
                        "pass": passed, "output": output, "error": error})
    python_version = subprocess.run([str(PYTHON), "--version"], capture_output=True,
                                    text=True, check=True).stdout.strip()
    controls = {parser["control"] for parser in parsers}
    standard_controls = [ROOT / "controls/ascii_pnm" / name for name in
                         ("red-green.ppm", "black-white.pgm", "black-white.pbm")]
    standard_command = [str(PYTHON), str(STANDARD_ADAPTER),
                        *(str(path) for path in standard_controls)]
    standard_run = subprocess.run(standard_command, cwd=ROOT, capture_output=True,
                                  text=True, timeout=30, check=True)
    standard_output = json.loads(standard_run.stdout.strip().splitlines()[-1])
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(), "python": python_version,
        "libvips": pkg_config("--modversion", "vips"),
        "magickwand": pkg_config("--modversion", "MagickWand"),
        "controls": {control: hashlib.sha256((ROOT / control).read_bytes()).hexdigest()
                     for control in sorted(controls)},
        "control_meaning": "valid ASCII P3 red/green 2x1 PPM and P2 black/white 2x1 PGM",
        "third_party": results,
        "runtime_candidate": {"api": "tkinter.PhotoImage(file=local path)",
                              "command": " ".join(standard_command),
                              "output": standard_output,
                              "verified_ascii_pnm": any(item["parsed"] for item in standard_output["controls"])},
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Python ASCII PNM packages passed")
    for row in results:
        if not row["pass"]:
            print(row["package"], row["error"])
    if count != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
