#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
LLVM_PROFILE_FILE=/tmp/one-pixel.profraw /work/replay /work/one-pixel.svg > /coverage/one-pixel.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
# Bundled codec, shaping, and bidi libraries are not on the SVG path; leave
# them out of the export to keep it a parser report.
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata \
  -ignore-filename-regex='/(harfbuzz|sheenbidi|image_formats|zip)/' > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'width': 2, 'height': 1}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
one_pixel = json.loads(Path('/coverage/one-pixel.json').read_text())
if one_pixel != {'width': 1, 'height': 1}:
    raise SystemExit(f'1x1 SVG mismatch: {one_pixel}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines = lambda group: sum(f['summary']['lines']['covered'] for f in group)
parser = [f for f in files if f['filename'].startswith('/work/source/modules/juce_graphics/drawables/')]
covered = lines(parser)
if not parser or not covered:
    raise SystemExit('no instrumented JUCE SVG parser source lines covered')
for suffix in ('/juce_SVGParser.cpp', '/lunasvg/source/svgparser.cpp', '/lunasvg/source/lunasvg.cpp', '/juce_DrawableComposite.cpp'):
    if not lines([f for f in parser if f['filename'].endswith(suffix)]):
        raise SystemExit(f'no coverage in {suffix}')
summary = {'control_pass': True, 'output': observed, 'one_pixel_output': one_pixel,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
