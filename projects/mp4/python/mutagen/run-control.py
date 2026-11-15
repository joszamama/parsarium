"""Replay the valid MP4 and count executed Mutagen package lines."""

import json
from pathlib import Path
import trace

import mutagen

from harness import parse_mp4


data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(parse_mp4, data)
expected = {"title": "Parsarium"}
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
source_root = str(Path(mutagen.__file__).resolve().parent) + "/"
executed_by_file = {}
for (filename, line), count in tracer.results().counts.items():
    source = str(Path(filename).resolve())
    if source.startswith(source_root) and count > 0:
        executed_by_file.setdefault(source, set()).add(line)
if not executed_by_file:
    raise SystemExit("no Mutagen package source lines covered")
files = [{"filename": source,
          "summary": {"lines": {"covered": len(lines)}},
          "executed_lines": sorted(lines)}
         for source, lines in sorted(executed_by_file.items())]
coverage = {"data": [{"files": files}]}
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2) + "\n")
(output / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(files),
           "parser_source_lines_covered": sum(len(lines) for lines in executed_by_file.values()),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
