#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
# No gs executable exists in this image; PDF interpretation must use linked libgs.
if command -v gs >/dev/null 2>&1; then echo 'unexpected gs executable' >&2; exit 1; fi
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/lib/libgs.so -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'pages':1,'width':612,'height':792}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
def lines(prefix='', suffix=''):
    return sum(f['summary']['lines']['covered'] for f in files
               if f['filename'].startswith(prefix) and f['filename'].endswith(suffix))
parser=[f for f in files if f['filename'].startswith('/work/source/')]
underlying=[f for f in files if f['filename'].startswith('/work/ghostscript/pdf/')]
covered=lines('/work/source/')
underlying_covered=lines('/work/ghostscript/pdf/')
pdf_coder=lines('/work/source/', '/coders/pdf.c')
delegate=lines('/work/source/', '/magick/delegate.c')
xref=lines('/work/ghostscript/pdf/', '/pdf_xref.c')
if not parser or not covered or not pdf_coder or not delegate:
    raise SystemExit('no GraphicsMagick PDF coder or Ghostscript delegate source covered')
if not underlying_covered or not xref:
    raise SystemExit('no in-process Ghostscript pdfi interpreter source covered')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,
         'pdf_coder_lines_covered':pdf_coder,'delegate_lines_covered':delegate,
         'ghostscript_source_lines_covered':lines('/work/ghostscript/'),
         'underlying_source_files':len(underlying),'underlying_source_lines_covered':underlying_covered,
         'underlying_xref_lines_covered':xref,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
