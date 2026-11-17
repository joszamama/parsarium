#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/install/lib/libpodofo.so -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'pages':1}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines=lambda group: sum(f['summary']['lines']['covered'] for f in group)
parser=[f for f in files if f['filename'].startswith('/work/source/src/podofo/')]
covered=lines(parser)
if not parser or not covered: raise SystemExit('no PoDoFo PDF parser source covered')
for suffix in ('/private/PdfParser.cpp','/private/PdfParserObject.cpp','/main/PdfTokenizer.cpp','/main/PdfMemDocument.cpp','/main/PdfPageCollection.cpp'):
    if not lines([f for f in parser if f['filename'].endswith(suffix)]): raise SystemExit(f'no coverage in {suffix}')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
