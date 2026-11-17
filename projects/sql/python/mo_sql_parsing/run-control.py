"""Replay the valid SQL control through mo_sql_parsing.parse and trace the mo-sql-parsing grammar and mo-parsing engine source lines."""

import json
from pathlib import Path
import trace

import harness
import mo_parsing
import mo_sql_parsing


EXPECTED = {
    "statement_count": 1,
    "statements": [{
        "kind": "select", "tables": ["customers", "orders"], "select_items": 3,
        "joins": 1, "where": True, "group_by": 1, "order_by": 1,
        "functions": ["count", "sum"], "literals": [["number", "10"], ["string", "paid"]],
    }],
}

data = Path("/input/control").read_bytes()
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(harness.parse_sql, data)
if observed != EXPECTED:
    raise SystemExit(f"control mismatch: {observed}")
counts = tracer.results().counts
files = []
for package in (mo_sql_parsing, mo_parsing):
    for source in sorted(Path(package.__file__).resolve().parent.rglob("*.py")):
        executed = sorted({line for (filename, line), count in counts.items()
                           if Path(filename).resolve() == source and count > 0})
        if executed:
            files.append({"filename": str(source), "summary": {"lines": {"covered": len(executed)}},
                          "executed_lines": executed})
if not any(f["filename"].endswith("/mo_sql_parsing/sql_parser.py") for f in files):
    raise SystemExit("mo_sql_parsing sql_parser.py had no executed source lines")
output = Path("/coverage")
output.mkdir(exist_ok=True)
(output / "observed.json").write_text(json.dumps(observed, indent=2) + "\n")
(output / "coverage.json").write_text(json.dumps({"data": [{"files": files}]}, indent=2) + "\n")
summary = {"control_pass": True, "output": observed,
           "parser_source_files": len(files),
           "parser_source_lines_covered": sum(f["summary"]["lines"]["covered"] for f in files),
           "coverage": "/coverage/coverage.json"}
(output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary))
