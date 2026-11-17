#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/install/lib/libpoppler-glib.so -object=/work/install/lib/libpoppler.so -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'pages':1}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines=lambda group: sum(f['summary']['lines']['covered'] for f in group)
parser=[f for f in files if f['filename'].startswith('/work/source/glib/')]
underlying=[f for f in files if f['filename'].startswith('/work/source/poppler/')]
covered=lines(parser)
underlying_covered=lines(underlying)
if not parser or not covered: raise SystemExit('no Poppler GLib frontend source covered')
if not underlying or not underlying_covered: raise SystemExit('no Poppler PDF core source covered')
for group,suffix in ((parser,'/poppler-document.cc'),(underlying,'/Parser.cc'),(underlying,'/Lexer.cc'),(underlying,'/XRef.cc'),(underlying,'/PDFDoc.cc')):
    if not lines([f for f in group if f['filename'].endswith(suffix)]): raise SystemExit(f'no coverage in {suffix}')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,'underlying_source_files':len(underlying),'underlying_source_lines_covered':underlying_covered,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
