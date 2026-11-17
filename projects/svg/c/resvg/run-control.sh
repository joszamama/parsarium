#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE='/coverage/control-%m.profraw' /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object /work/libresvg.so \
  -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'width': 2, 'height': 1, 'first': [255, 0, 0], 'second': [0, 255, 0]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [file for file in files if file['filename'].startswith('/work/source/crates/usvg/src/parser/')]
covered = sum(file['summary']['lines']['covered'] for file in parser)
specific = sum(file['summary']['lines']['covered'] for file in parser
               if file['filename'].endswith('/parser/svgtree/parse.rs'))
if not covered or not specific:
    raise SystemExit(f'usvg parser coverage missing: {covered} total, {specific} XML-tree lines')
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'format_specific_source_lines_covered': specific,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
