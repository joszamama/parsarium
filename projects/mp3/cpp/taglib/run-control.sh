#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY_CHECK'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'version':1,'layer':3,'sample_rate':44100,'channels':1,'bitrate_kbps':64,'length_ms':287}
if observed!=expected:raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser=[f for f in files if f['filename'].startswith('/work/taglib-2.3.2/taglib/')]
covered=sum(f['summary']['lines']['covered'] for f in parser)
if not parser or not covered:raise SystemExit('no instrumented TagLib parser lines covered')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,
         'parser_file_lines_covered':{f['filename'].removeprefix('/work/taglib-2.3.2/taglib/'):f['summary']['lines']['covered'] for f in parser if f['summary']['lines']['covered']},
         'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PY_CHECK
