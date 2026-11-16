"""Verify a valid PNG control and instrument Tk's native PNG reader."""

import json
import os
from pathlib import Path
import subprocess


os.environ["LLVM_PROFILE_FILE"] = "/coverage/tk-control.profraw"
run = subprocess.run(
    ["xvfb-run", "-a", "/opt/python/bin/python3.13", "/work/replay.py", "/input/control"],
    text=True, capture_output=True, check=True,
)
observed = json.loads(run.stdout)
expected = {"width": 2, "height": 1, "rgb0": [255, 0, 0], "rgb1": [0, 255, 0]}
if observed != expected:
    raise RuntimeError(f"control mismatch: {observed}")
subprocess.run(
    ["llvm-profdata", "merge", "-sparse", "/coverage/tk-control.profraw",
     "-o", "/coverage/tk-control.profdata"], check=True,
)
with Path("/coverage/coverage.json").open("w") as coverage_file:
    subprocess.run(
        ["llvm-cov", "export", "/opt/tk/lib/libtk8.6.so",
         "-instr-profile=/coverage/tk-control.profdata", "--summary-only"],
        stdout=coverage_file, check=True,
    )
files = json.loads(Path("/coverage/coverage.json").read_text())["data"][0]["files"]
png_sources = [file for file in files if file["filename"].endswith("/tkImgPNG.c")]
covered = sum(file["summary"]["lines"]["covered"] for file in png_sources)
if not png_sources or covered <= 0:
    raise RuntimeError("Tk PNG decoder source lines were not covered")
summary = {
    "control_pass": True,
    "output": observed,
    "parser_source_files": len(png_sources),
    "parser_source_lines_covered": covered,
    "coverage": "/coverage/coverage.json",
    "afl_parser_feedback_available": False,
}
Path("/coverage/observed.json").write_text(json.dumps(observed, indent=2) + "\n")
Path("/coverage/summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
