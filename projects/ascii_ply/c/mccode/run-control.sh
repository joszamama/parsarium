#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'vertices': 3, 'faces': 1, 'length': 1.0, 'width': 1.0}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [file for file in files if file['filename'] == '/work/generated/interoff-lib.c']
covered = sum(file['summary']['lines']['covered'] for file in parser)
if len(parser) != 1 or covered <= 0:
    raise SystemExit('no instrumented McCode PLY parser source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': 1, 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
