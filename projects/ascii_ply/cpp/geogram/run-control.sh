#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/lib/libgeogram.so \
  -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'vertices': 3, 'faces': 1, 'face': [0, 1, 2]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
front = [f for f in files if f['filename'].startswith(
    '/work/source/src/lib/geogram/mesh/')]
under = [f for f in files if f['filename'].startswith(
    '/work/source/src/lib/geogram/third_party/rply/')]
front_covered = sum(f['summary']['lines']['covered'] for f in front)
under_covered = sum(f['summary']['lines']['covered'] for f in under)
front_specific = sum(f['summary']['lines']['covered'] for f in front
                     if f['filename'].endswith('/mesh_io.cpp'))
under_specific = sum(f['summary']['lines']['covered'] for f in under
                     if f['filename'].endswith('/rply.c'))
if min(front_covered, under_covered, front_specific, under_specific) <= 0:
    raise SystemExit('no instrumented Geogram and RPly PLY source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(front),
          'parser_source_lines_covered': front_covered,
          'format_specific_source_lines_covered': front_specific,
          'underlying_source_files': len(under),
          'underlying_source_lines_covered': under_covered,
          'underlying_format_specific_source_lines_covered': under_specific,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
