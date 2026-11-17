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
expected = json.loads(Path('/work/manifest.json').read_text())['expected_output']
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'].endswith('/source/include/jsoncons/json_parser.hpp')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
if covered < 100:
    raise SystemExit(f'jsoncons parser source line coverage insufficient: {covered}')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len([f for f in files if f['filename'].startswith('/work/source/')]),
          'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in files if f['filename'].startswith('/work/source/')),
          'format_specific_source_lines_covered': covered, 'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
