#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/lib/libgs.so -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'pages':1}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser=[f for f in files if f['filename'].startswith('/work/source/')]
underlying=[f for f in files if f['filename'].startswith('/work/source/pdf/')]
xref=[f for f in underlying if f['filename'].endswith('/pdf/pdf_xref.c')]
covered=sum(f['summary']['lines']['covered'] for f in parser)
underlying_covered=sum(f['summary']['lines']['covered'] for f in underlying)
xref_covered=sum(f['summary']['lines']['covered'] for f in xref)
if not parser or not covered or not underlying_covered: raise SystemExit('no Ghostscript PDF interpreter source covered')
if not xref_covered: raise SystemExit('no pdf_xref.c lines covered')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,'underlying_source_files':len(underlying),'underlying_source_lines_covered':underlying_covered,'format_specific_source_lines_covered':xref_covered,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
