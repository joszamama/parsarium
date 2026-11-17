"""Run pinned Go ASCII PNM readers against a valid local P3 control."""

import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data" / "go" / "ascii_pnm"
MODULE = ROOT / "adapters" / "go" / "ascii_pnm"
CONTROL = ROOT / "controls" / "ascii_pnm" / "red-green.ppm"
NATIVE = {
    "github.com/kirklin/vipsx/vips": "native_kirklin",
    "gitee.com/shiqiyue/go-vips": "native_shiqiyue",
    "github.com/bu/govips/pkg/vips": "native_bu",
    "github.com/robxyy/govips/pkg/vips": "native_robxyy",
    "github.com/perelin/govips/pkg/vips": "native_perelin",
    "github.com/gographics/gmagick": "native_gmagick",
    "github.com/cshum/vipsgen/vips": "native_vipsgen",
}


def tool_version(*command: str) -> str | None:
    run = subprocess.run(command, cwd=MODULE, text=True, capture_output=True)
    return run.stdout.strip() if run.returncode == 0 else None


def main() -> None:
    parsers = json.loads((CELL / "parsers.json").read_text())
    results = []
    for parser in parsers:
        name = parser["name"]
        command = ["go", "run", f"./{NATIVE[name]}", "../../../controls/ascii_pnm/red-green.ppm"] if name in NATIVE else ["go", "run", ".", name, "../../../controls/ascii_pnm/red-green.ppm"]
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
        results.append({"package": name, "module": parser["module"],
                        "version": parser["version"], "scope": parser["scope"],
                        "command": " ".join(command), "pass": passed,
                        "output": output, "error": error})
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "platform": platform.platform(), "go": tool_version("go", "version"),
              "libvips": tool_version("pkg-config", "--modversion", "vips"),
              "magickwand": tool_version("pkg-config", "--modversion", "MagickWand"),
              "graphicsmagickwand": tool_version("pkg-config", "--modversion", "GraphicsMagickWand"),
              "control": "controls/ascii_pnm/red-green.ppm",
              "control_sha256": hashlib.sha256(CONTROL.read_bytes()).hexdigest(),
              "control_meaning": "ASCII P3 PPM, 2x1, maximum 255, red then green",
              "third_party": results}
    (CELL / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    count = sum(row["pass"] for row in results)
    print(f"{count}/{len(results)} Go ASCII PNM packages passed")
    if count != len(results):
        for row in results:
            if not row["pass"]:
                print(row["package"], row["error"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
