"""Replay the valid SQL control through antlr_tsql.ast.parse and trace the parser's own source lines.

Traced sources: the antlr_tsql package (ANTLR 4 generated T-SQL lexer and parser, and its tree
transformer), the antlr-ast tree-shaping library and the antlr4 Python runtime that executes the
generated parser.
"""

import json
from pathlib import Path
import trace

import harness
import antlr4
import antlr_ast
import antlr_tsql


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
for package in (antlr_tsql, antlr_ast, antlr4):
    for source in sorted(Path(package.__file__).resolve().parent.rglob("*.py")):
        executed = sorted({line for (filename, line), count in counts.items()
                           if Path(filename).resolve() == source and count > 0})
        if executed:
            files.append({"filename": str(source), "summary": {"lines": {"covered": len(executed)}},
                          "executed_lines": executed})
if not any(f["filename"].endswith("/antlr_tsql/antlr_py/tsqlParser.py") for f in files):
    raise SystemExit("antlr-tsql tsqlParser.py had no executed source lines")
if not any(f["filename"].endswith("/antlr4/Parser.py") for f in files):
    raise SystemExit("antlr4 runtime Parser.py had no executed source lines")
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
