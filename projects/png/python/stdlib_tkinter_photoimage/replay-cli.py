"""Run the PhotoImage replay under Xvfb for arbitrary local PNG files."""

import subprocess
import sys


if len(sys.argv) != 2:
    raise SystemExit("usage: replay-cli.py LOCAL_PNG_FILE")
subprocess.run(
    ["xvfb-run", "-a", "/opt/python/bin/python3.13", "/work/replay.py", sys.argv[1]],
    check=True,
)
