#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'sequence_tracks':1,'video_tracks':1,'width':2,'height':2}
if observed!=expected:raise SystemExit(f'control mismatch: {observed}')
root='/work/libheif-1.23.7/libheif/'
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines=lambda group:sum(f['summary']['lines']['covered'] for f in group)
parser=[f for f in files if f['filename'].startswith(root)]
if not parser or not lines(parser):raise SystemExit('no libheif parser source covered')
for suffix in ('/file.cc','/file_layout.cc','/box.cc','/bitstream.cc','/context.cc',
               '/sequences/seq_boxes.cc','/sequences/track.cc','/sequences/track_visual.cc',
               '/sequences/chunk.cc','/codecs/avc_boxes.cc'):
    if not lines([f for f in parser if f['filename'].endswith(suffix)]):raise SystemExit(f'no coverage in {suffix}')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),
         'parser_source_lines_covered':lines(parser),'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
