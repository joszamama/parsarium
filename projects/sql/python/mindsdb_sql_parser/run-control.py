"""Replay the valid SQL control through mindsdb_sql_parser.parse_sql and trace the parser's own source lines.

Traced sources: the mindsdb_sql_parser package (lexer, grammar actions and AST) and the SLY
lexer/LALR library that the same distribution installs as the top-level sly package.
"""

import json
from pathlib import Path
import trace

import harness
import mindsdb_sql_parser
import sly


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
for package in (mindsdb_sql_parser, sly):
    for source in sorted(Path(package.__file__).resolve().parent.rglob("*.py")):
        executed = sorted({line for (filename, line), count in counts.items()
                           if Path(filename).resolve() == source and count > 0})
        if executed:
            files.append({"filename": str(source), "summary": {"lines": {"covered": len(executed)}},
                          "executed_lines": executed})
if not any(f["filename"].endswith("/mindsdb_sql_parser/parser.py") for f in files):
    raise SystemExit("mindsdb_sql_parser parser.py had no executed source lines")
if not any(f["filename"].endswith("/sly/yacc.py") for f in files):
    raise SystemExit("sly yacc.py had no executed source lines")
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
