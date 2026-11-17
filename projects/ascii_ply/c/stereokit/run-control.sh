#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE='/coverage/control-%m.profraw' /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object /work/lib/libStereoKitC.so \
  -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'subsets':1,'vertices':3,'indices':3,'face':[0,1,2],'second_x':1.0}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'] == '/work/source/StereoKitC/libraries/micro_ply.h']
covered = sum(f['summary']['lines']['covered'] for f in parser)
loader = sum(f['summary']['lines']['covered'] for f in files
             if f['filename'] == '/work/source/StereoKitC/asset_types/model_ply.cpp')
if not covered or not loader:
    raise SystemExit(f'micro_ply/model loader source missing: {covered}/{loader}')
summary = {'control_pass':True,'output':observed,'parser_source_files':len(parser),
           'parser_source_lines_covered':covered,'model_ply_source_lines_covered':loader,
           'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PY
