#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/libexec/gcv/libgcv-ply.so \
  -object=/work/lib/libgcv.so -instr-profile=/coverage/control.profdata \
  --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'vertices': 3, 'faces': 1, 'second_x': 1000.0, 'face': [0, 1, 2]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
reader = [f for f in files if f['filename'].endswith('/src/libgcv/plugins/ply/ply_read.c')]
rply = [f for f in files if f['filename'].endswith('/src/libgcv/plugins/ply/rply.c')]
reader_covered = sum(f['summary']['lines']['covered'] for f in reader)
rply_covered = sum(f['summary']['lines']['covered'] for f in rply)
if len(reader) != 1 or len(rply) != 1 or reader_covered == 0 or rply_covered == 0:
    raise SystemExit('no instrumented BRL-CAD importer and bundled RPly source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(reader),
          'parser_source_lines_covered': reader_covered,
          'format_specific_source_lines_covered': reader_covered,
          'underlying_source_files': len(rply),
          'underlying_source_lines_covered': rply_covered,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
