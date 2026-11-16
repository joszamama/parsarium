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
expected = {'entries': 1, 'name': 'hello.txt', 'content': 'parsarium\n'}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
primary = [f for f in files if f['filename'] == '/work/source/library/Zippy/ZipArchive.hpp']
underlying = [f for f in files if f['filename'].startswith('/work/source/library/Zippy/miniz/')]
covered = sum(f['summary']['lines']['covered'] for f in primary)
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
if not covered or not underlying_covered:
    raise SystemExit('Zippy or bundled miniz parser source not covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(primary), 'parser_source_lines_covered': covered,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
