"""Compile include-pnm's documented local-file macro against the supplied P3 control."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "adapters" / "rust" / "ascii_pnm" / "include_pnm_dynamic"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 scripts/run_rust_include_pnm.py CONTROL.ppm")
    control = Path(sys.argv[1]).resolve(strict=True)
    environment = os.environ.copy()
    environment["PARSARIUM_PNM_CONTROL"] = str(control)
    subprocess.run(["cargo", "run", "--locked", "--quiet"], cwd=PROJECT,
                   env=environment, check=True)


if __name__ == "__main__":
    main()
