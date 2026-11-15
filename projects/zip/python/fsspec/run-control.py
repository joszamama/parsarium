"""Replay the valid ZIP and count fsspec plus delegated zipfile lines."""

import json
from pathlib import Path
import trace

import fsspec
import zipfile

from harness import parse_zip


data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(parse_zip, data)
expected = {"names": ["hello.txt"], "hello": "parsarium\n"}
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
source_root = str(Path(fsspec.__file__).resolve().parent) + "/"
zip_root = str(Path(zipfile.__file__).resolve().parent) + "/"
executed_by_file = {}
underlying_by_file = {}
for (filename, line), count in tracer.results().counts.items():
    source = str(Path(filename).resolve())
    if source.startswith(source_root) and count > 0:
        executed_by_file.setdefault(source, set()).add(line)
    if source.startswith(zip_root) and count > 0:
        underlying_by_file.setdefault(source, set()).add(line)
if not executed_by_file:
    raise SystemExit("no fsspec package source lines covered")
if not underlying_by_file:
    raise SystemExit("no CPython zipfile source lines covered")
files = [{"filename": source,
          "summary": {"lines": {"covered": len(lines)}},
          "executed_lines": sorted(lines)}
         for source, lines in sorted({**executed_by_file, **underlying_by_file}.items())]
coverage = {"data": [{"files": files}]}
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2) + "\n")
(output / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(executed_by_file),
           "parser_source_lines_covered": sum(len(lines) for lines in executed_by_file.values()),
           "underlying_source_files": len(underlying_by_file),
           "underlying_source_lines_covered": sum(len(lines) for lines in underlying_by_file.values()),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
