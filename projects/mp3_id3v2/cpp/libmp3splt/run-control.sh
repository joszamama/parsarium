#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/install/lib/libmp3splt.so -object=/work/install/lib/libmp3splt0/libsplt_mp3.so -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'split_status': 1, 'segment_bytes': 2304, 'frame_header': 'ffe348c0'}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser=[f for f in files if f['filename'].startswith('/work/source/plugins/')]
covered=sum(f['summary']['lines']['covered'] for f in parser)
if not parser or not covered: raise SystemExit('no libmp3splt MP3 plugin source covered')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
