#!/bin/sh
set -eu
export LD_LIBRARY_PATH=/opt/gegl-cov/lib
export GEGL_PATH=/opt/gegl-cov/lib/gegl-0.4
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object /opt/gegl-cov/lib/gegl-0.4/ppm-load.so \
  -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'width':2,'height':1,'first':[255,0,0],'second':[0,255,0]}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
coverage=json.loads(Path('/coverage/coverage.json').read_text())
files=[f for data in coverage['data'] for f in data['files'] if f['filename'].startswith('/work/source/operations/external/')]
covered=sum(f['summary']['lines']['covered'] for f in files)
if not files or covered < 1: raise SystemExit('no GEGL PPM plugin source coverage')
result={'control_pass':True,'output':observed,'parser_source_files':len(files),
        'parser_source_lines_covered':covered,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result)+'\n')
print(json.dumps(result))
PYCODE
