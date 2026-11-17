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
expected = {'width': 2, 'height': 1, 'first': [255, 0, 0, 255],
            'second': [0, 255, 0, 255]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'].startswith('/work/source/modules/imgcodecs/src/')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
png = sum(f['summary']['lines']['covered'] for f in parser if f['filename'].endswith('/grfmt_png.cpp'))
if not parser or not covered or not png:
    raise SystemExit('no OpenCV imgcodecs PNG decoder source lines covered')
underlying = [f for f in files if f['filename'].startswith('/work/source/3rdparty/libpng/')]
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
chunks = sum(f['summary']['lines']['covered'] for f in underlying if f['filename'].endswith('/pngrutil.c'))
if not underlying or not underlying_covered or not chunks:
    raise SystemExit('no bundled libpng chunk-reader source lines covered')
summary = {'control_pass': True, 'output': observed,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_covered,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
