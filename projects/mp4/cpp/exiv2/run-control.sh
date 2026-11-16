#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'brand':'MP4 Base Media','width':2,'height':2}
if observed!=expected:raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser=[f for f in files if f['filename'].startswith('/work/exiv2-0.28.9/src/')]
covered=sum(f['summary']['lines']['covered'] for f in parser)
if not parser or not covered:raise SystemExit('no Exiv2 parser source lines covered')
qtime=[f for f in parser if f['filename'].endswith('/quicktimevideo.cpp')]
qtime_covered=sum(f['summary']['lines']['covered'] for f in qtime)
if not qtime_covered:raise SystemExit('no Exiv2 QuickTime parser lines covered')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),
         'parser_source_lines_covered':covered,'quicktime_source_lines_covered':qtime_covered,
         'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
