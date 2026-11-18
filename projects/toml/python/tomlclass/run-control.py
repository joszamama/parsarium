"""Replay the valid TOML control through tomlclass.loads and trace tomlclass package source."""

import json
from pathlib import Path
import trace

import harness
import tomlclass


data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(harness.parse_toml, data)
expected = json.loads(Path("/work/expected/service-config.expected.json").read_text(encoding="utf-8"))
if observed != expected:
    raise SystemExit(f"control mismatch: {json.dumps(observed, ensure_ascii=False, sort_keys=True)}")
source_root = Path(tomlclass.__file__).resolve().parent
files = []
for source in sorted(source_root.glob("*.py")):
    executed = sorted({line for (filename, line), count in tracer.results().counts.items()
                       if Path(filename).resolve() == source and count > 0})
    if executed:
        files.append({"filename": str(source), "summary": {"lines": {"covered": len(executed)}},
                      "executed_lines": executed})
if not any(f["filename"].endswith("/tomlclass/parser.py") for f in files):
    raise SystemExit("tomlclass parser.py had no executed source lines")
coverage = {"data": [{"files": files}]}
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
(output / "coverage.json").write_text(json.dumps(coverage, indent=2) + "\n")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(files),
           "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in files),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
