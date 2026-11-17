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
parser_files = [f for f in files if '/sqlite3-parser-0.17.0/' in f['filename']]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
if not parser_files or covered == 0:
    raise SystemExit('no instrumented sqlite3-parser crate source lines covered')
out_dir = Path('/work/generated/out-dir.txt').read_text().strip() + '/'
generated = [f for f in files if f['filename'].startswith(out_dir)]
generated_lines = sum(f['summary']['lines']['covered'] for f in generated)
if generated_lines == 0:
    raise SystemExit('generated Lemon parser (OUT_DIR parse.rs) was not reached')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'parser_file_lines_covered': {f['filename'].split('/sqlite3-parser-0.17.0/', 1)[1]:
                                        f['summary']['lines']['covered'] for f in parser_files},
          'generated_parser_lines_covered': {f['filename'][len(out_dir):]:
                                             f['summary']['lines']['covered'] for f in generated},
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
