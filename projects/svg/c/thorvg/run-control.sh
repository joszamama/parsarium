#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
LLVM_PROFILE_FILE=/tmp/one-pixel.profraw /work/replay /work/one-pixel.svg > /tmp/one-pixel.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'width': 2, 'height': 1}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
one_pixel = json.loads(Path('/tmp/one-pixel.json').read_text())
if one_pixel != {'width': 1, 'height': 1}:
    raise SystemExit(f'one-pixel mismatch: {one_pixel}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'].startswith('/work/source/src/')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
if not parser or not covered:
    raise SystemExit('no instrumented ThorVG source lines covered')
summary = {'control_pass': True, 'output': observed, 'one_pixel_output': one_pixel,
           'parser_source_files': len(parser), 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
