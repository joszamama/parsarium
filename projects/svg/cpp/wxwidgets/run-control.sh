#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay-bin -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'width': 2, 'height': 1, 'left_rgb': [255, 0, 0], 'right_rgb': [0, 255, 0]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
svg = [f for f in files if f['filename'] == '/work/source/src/generic/bmpsvg.cpp']
nano = [f for f in files if f['filename'].startswith('/work/source/3rdparty/nanosvg/src/')]
svg_lines = sum(f['summary']['lines']['covered'] for f in svg)
nano_lines = sum(f['summary']['lines']['covered'] for f in nano)
parser = sum(f['summary']['lines']['covered'] for f in nano
             if f['filename'].endswith('/nanosvg.h'))
if len(svg) != 1 or svg_lines <= 0:
    raise SystemExit('wxWidgets bmpsvg.cpp source was not covered')
if parser <= 0:
    raise SystemExit('bundled NanoSVG nanosvg.h parser source was not covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(svg),
          'parser_source_lines_covered': svg_lines,
          'format_specific_source_lines_covered': svg_lines,
          'underlying_source_files': len(nano),
          'underlying_source_lines_covered': nano_lines,
          'underlying_parser_source_lines_covered': parser,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
