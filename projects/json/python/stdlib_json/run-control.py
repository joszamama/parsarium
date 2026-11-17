"""Replay the JSON control and trace CPython's pure-Python parser files."""

import json
from pathlib import Path
import trace

import harness


data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(harness.parse_json, data)
expected = {"root_type": "object", "top_level_keys": ["items", "kind"],
            "item_count": 2, "first_id": 7, "first_label": "a\nb",
            "first_ok": True, "first_value_is_null": True, "second_label": "π"}
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
source_root = Path(json.__file__).resolve().parent
files = []
for name in ("__init__.py", "decoder.py", "scanner.py"):
    source = source_root / name
    executed = sorted({line for (filename, line), hits in tracer.results().counts.items()
                       if Path(filename).resolve() == source and hits > 0})
    if executed:
        files.append({"filename": str(source), "summary": {"lines": {"covered": len(executed)}},
                      "executed_lines": executed})
covered_names = {Path(f["filename"]).name for f in files}
if not {"decoder.py", "scanner.py"} <= covered_names:
    raise SystemExit(f"pure-Python JSON decoder/scanner not both covered: {covered_names}")
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2) + "\n")
(output / "coverage.json").write_text(json.dumps({"data": [{"files": files}]}, indent=2) + "\n")
summary = {"control_pass": True, "output": observed, "parser_source_files": len(files),
           "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in files),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
