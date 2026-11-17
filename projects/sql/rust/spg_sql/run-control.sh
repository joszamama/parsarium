#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
/work/llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
/work/llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text(encoding='utf-8'))
expected = {"statement_count": 1, "statements": [{
    "kind": "select", "tables": ["customers", "orders"], "select_items": 3, "joins": 1,
    "where": True, "group_by": 1, "order_by": 1, "functions": ["count", "sum"],
    "literals": [["number", "10"], ["string", "paid"]]}]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
parser_files = [f for f in files if '/spg-sql-9.1.0/' in f['filename']]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
if not parser_files or covered == 0:
    raise SystemExit('no instrumented spg-sql crate source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'parser_file_lines_covered': {f['filename'].split('/spg-sql-9.1.0/', 1)[1]:
                                        f['summary']['lines']['covered'] for f in parser_files},
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
