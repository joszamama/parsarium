#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
# %m keeps one raw profile per instrumented module: the C++ harness and librsvg-2.so.
LLVM_PROFILE_FILE='/coverage/control-%m.profraw' /work/replay /input/control > /coverage/observed.json
# A valid 1 x 1 document must also render, with no second pixel.
LLVM_PROFILE_FILE=/dev/null /work/replay /work/valid-1x1.svg > /coverage/observed-1x1.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object "$(readlink -f /work/install/lib/librsvg-2.so)" \
 -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'width': 2, 'height': 1, 'first': [255, 0, 0], 'second': [0, 255, 0]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
single = json.loads(Path('/coverage/observed-1x1.json').read_text())
if single != {'width': 1, 'height': 1, 'first': [255, 0, 0], 'second': None}:
    raise SystemExit(f'1 x 1 control mismatch: {single}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
def covered(prefix):
    matched = [f for f in files if f['filename'].startswith(prefix)]
    return matched, sum(f['summary']['lines']['covered'] for f in matched)
# The gates sit in librsvg's Rust core, not only in the C API wrapper or the C++ call site.
parser, parser_covered = covered('/work/librsvg/rsvg/src/')
if not parser or not parser_covered:
    raise SystemExit('no instrumented librsvg Rust SVG engine lines covered')
_, xml_load_covered = covered('/work/librsvg/rsvg/src/xml/xml2_load.rs')
if not xml_load_covered:
    raise SystemExit('no librsvg SVG XML loading lines covered')
_, xml_tree_covered = covered('/work/librsvg/rsvg/src/xml/mod.rs')
if not xml_tree_covered:
    raise SystemExit('no librsvg SVG XML element-tree lines covered')
_, c_api_covered = covered('/work/librsvg/librsvg-c/src/')
if not c_api_covered:
    raise SystemExit('no librsvg C API lines covered')
call_site, call_site_covered = covered('/work/harness.cpp')
if len(call_site) != 1 or not call_site_covered:
    raise SystemExit('no C++ harness call-site lines covered')
summary = {'control_pass': True, 'output': observed, 'output_1x1': single,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': parser_covered,
           'xml_load_lines_covered': xml_load_covered,
           'xml_tree_lines_covered': xml_tree_covered,
           'c_api_lines_covered': c_api_covered,
           'cpp_call_site_lines_covered': call_site_covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
