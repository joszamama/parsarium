"""Replay the valid PNG and count executed lines in the PyPNG package."""

import json
from pathlib import Path
import trace

import harness
import png


data = Path('/input/control').read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(harness.parse_png, data)
expected = {"width": 2, "height": 1,
            "rgba0": [255, 0, 0, 255], "rgba1": [0, 255, 0, 255]}
if observed != expected:
    raise SystemExit(f"control mismatch: {observed}")
source = str(Path(png.__file__).resolve())
executed = sorted({line for (filename, line), count in tracer.results().counts.items()
                   if str(Path(filename).resolve()) == source and count > 0})
if not executed:
    raise SystemExit("no PyPNG package source lines covered")
coverage = {"data": [{"files": [{"filename": source,
                                    "summary": {"lines": {"covered": len(executed)}},
                                    "executed_lines": executed}]}]}
output = Path('/coverage')
output.mkdir(exist_ok=True)
(output / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')
(output / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
summary = {"control_pass": True, "output": observed,
           "parser_source_files": 1, "parser_source_lines_covered": len(executed),
           "coverage": "/coverage/coverage.json"}
(output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
