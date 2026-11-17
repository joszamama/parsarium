#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
if ! ldd /work/replay-bin | grep -q '/work/lib/libgtk-4.so.1'; then
    echo 'replay is not using the source-built GTK 4 library' >&2
    exit 1
fi
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay-bin -object=/work/lib/libgtk-4.so.1 \
  -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'width': 2, 'height': 1}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'].startswith('/work/source/gtk/svg/')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
specific = sum(f['summary']['lines']['covered'] for f in parser
               if f['filename'].endswith('/gtksvgparser.c'))
if not parser or covered <= 0 or specific <= 0:
    raise SystemExit('GTK 4 native GtkSvg parser source was not covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'format_specific_source_lines_covered': specific,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
