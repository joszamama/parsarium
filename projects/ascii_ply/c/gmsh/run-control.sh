#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/lib/libgmsh.so \
  -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'vertices': 3, 'triangles': 1, 'triangle_nodes': 3, 'x_sum': 1.0}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
parser_files = [f for f in files if f['filename'].startswith('/work/source/src/geo/')]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
specific = [f for f in parser_files if f['filename'].endswith('/GModelIO_PLY.cpp')]
specific_covered = sum(f['summary']['lines']['covered'] for f in specific)
if not parser_files or covered == 0 or specific_covered == 0:
    raise SystemExit('no instrumented Gmsh native PLY reader source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'format_specific_source_lines_covered': specific_covered,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
