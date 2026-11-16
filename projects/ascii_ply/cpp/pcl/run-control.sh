#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/lib/libpcl_io.so \
  -object=/work/lib/libpcl_io_ply.so \
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
parser_files = [f for f in files if f['filename'].startswith('/work/source/io/src/')]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
specific = [f for f in parser_files if f['filename'].endswith('/ply_io.cpp')]
specific_covered = sum(f['summary']['lines']['covered'] for f in specific)
underlying = [f for f in files if f['filename'].startswith('/work/source/io/src/ply/')]
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
underlying_specific = [f for f in underlying if f['filename'].endswith('/ply_parser.cpp')]
underlying_specific_covered = sum(f['summary']['lines']['covered'] for f in underlying_specific)
if not parser_files or specific_covered == 0 or underlying_specific_covered == 0:
    raise SystemExit('no instrumented PCL PLYReader and PLY parser source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'format_specific_source_lines_covered': specific_covered,
          'underlying_source_files': len(underlying),
          'underlying_source_lines_covered': underlying_covered,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
