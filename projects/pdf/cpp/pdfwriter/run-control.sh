#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
# A zero-page document is a valid parse, not a rejection. Its profile stays
# out of the control coverage.
python3 - <<'PYCODE'
from pathlib import Path
objects=[b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [] /Count 0 >>"]
data=bytearray(b"%PDF-1.4\n"); offsets=[]
for index, obj in enumerate(objects, 1):
    offsets.append(len(data)); data += f"{index} 0 obj\n".encode() + obj + b"\nendobj\n"
xref=len(data)
data += f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode()
data += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets)
data += f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
Path('/tmp/zero-page.pdf').write_bytes(data)
PYCODE
LLVM_PROFILE_FILE=/tmp/zero-page.profraw /work/replay /tmp/zero-page.pdf > /tmp/zero-page.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'pages':1}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
zero=json.loads(Path('/tmp/zero-page.json').read_text())
if zero != {'pages':0}: raise SystemExit(f'zero-page mismatch: {zero}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines=lambda group: sum(f['summary']['lines']['covered'] for f in group)
parser=[f for f in files if f['filename'].startswith('/work/source/PDFWriter/')]
covered=lines(parser)
if not parser or not covered: raise SystemExit('no PDF-Writer parser source covered')
for suffix in ('/PDFParser.cpp','/PDFParserTokenizer.cpp','/PDFObjectParser.cpp','/InputFile.cpp'):
    if not lines([f for f in parser if f['filename'].endswith(suffix)]): raise SystemExit(f'no coverage in {suffix}')
summary={'control_pass':True,'output':observed,'zero_page_output':zero,'parser_source_files':len(parser),'parser_source_lines_covered':covered,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
