#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
# %m keeps one raw profile per instrumented module: harness, GdkPixbuf, librsvg, and the SVG loader.
LLVM_PROFILE_FILE='/coverage/control-%m.profraw' /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay \
 -object "$(readlink -f /work/install/lib/libgdk_pixbuf-2.0.so)" \
 -object "$(readlink -f /work/install/lib/librsvg-2.so)" \
 -object /work/install/lib/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader_svg.so \
 -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'width': 2, 'height': 1, 'first': [255, 0, 0, 255],
            'second': [0, 255, 0, 255]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
def covered(prefix):
    matched = [f for f in files if f['filename'].startswith(prefix)]
    return matched, sum(f['summary']['lines']['covered'] for f in matched)
parser, parser_covered = covered('/work/source/gdk-pixbuf/')
if not parser or not parser_covered:
    raise SystemExit('no instrumented GdkPixbuf loader API lines covered')
underlying, underlying_covered = covered('/work/librsvg/rsvg/src/')
if not underlying or not underlying_covered:
    raise SystemExit('no instrumented librsvg SVG parser lines covered')
_, xml_covered = covered('/work/librsvg/rsvg/src/xml/xml2_load.rs')
if not xml_covered:
    raise SystemExit('no librsvg SVG XML loading lines covered')
_, plugin_covered = covered('/work/librsvg/gdk-pixbuf-loader/src/')
if not plugin_covered:
    raise SystemExit('no librsvg GdkPixbuf SVG loader plugin lines covered')
summary = {'control_pass': True, 'output': observed,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_covered,
           'svg_loader_plugin_lines_covered': plugin_covered,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': parser_covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
