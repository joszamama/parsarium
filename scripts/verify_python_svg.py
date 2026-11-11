"""Run pinned Python SVG parsers against local valid SVG controls."""

import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "python" / "svg"
ADAPTER = ROOT / "adapters" / "python" / "svg"
PYTHON = ADAPTER / ".venv" / "bin" / "python"


def native_version(package):
    try:
        return subprocess.run(["pkg-config", "--modversion", package],
                              capture_output=True, text=True, timeout=5,
                              check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None


def main():
    parsers = json.loads((CELL / "parsers.json").read_text())
    env = os.environ.copy()
    env["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join((
        "/opt/homebrew/lib", "/opt/homebrew/opt/cairo/lib",
        "/opt/homebrew/opt/imagemagick/lib",
        env.get("DYLD_FALLBACK_LIBRARY_PATH", "")))
    env["MAGICK_HOME"] = "/opt/homebrew/opt/imagemagick"
    env["QT_QPA_PLATFORM"] = "offscreen"
    third_party = []
    for parser in parsers:
        command = [str(PYTHON), str(ADAPTER / "main.py"), parser["name"],
                   str(ROOT / parser["control"])]
        try:
            process = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                                     text=True, timeout=30, check=True)
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
        "python": subprocess.run([str(PYTHON), "--version"], text=True,
                                 capture_output=True, check=True).stdout.strip(),
        "controls": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
                     for path in controls},
        "control_meaning": "A 2×1 SVG with red and green rectangles; a 4×2 SVG with a red rectangle and a blue triangular path, used for path geometry",
        "native_dependencies": {"cairo": native_version("cairo"),
                                "vips": native_version("vips"),
                                "MagickWand": native_version("MagickWand")},
        "native_dependency_note": "CairoSVG, pyvips, and Wand require local graphics libraries. A missing optional Inkscape delegate warns during the Wand run, but ImageMagick still renders the valid control.",
        "third_party": third_party,
        "runtime": [],
    }
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(row["pass"] for row in third_party)
    print(f"{passed}/{len(third_party)} Python SVG packages")
    for row in third_party:
        if not row["pass"]:
            print(row["package"], row["error"], row["output"])
    if passed != len(third_party):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
