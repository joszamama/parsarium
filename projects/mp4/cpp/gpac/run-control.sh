#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
import os
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'tracks':2,'video_tracks':1,'audio_tracks':1,'width':2,'height':2,'duration_ms':1000}
if observed!=expected:raise SystemExit(f'control mismatch: {observed}')
root='/work/gpac-26.07.0/src/'
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines=lambda group:sum(f['summary']['lines']['covered'] for f in group)
isomedia=[f for f in files if f['filename'].startswith(root+'isomedia/')]
utils=[f for f in files if f['filename'].startswith(root+'utils/')]
adapter=[f for f in files if os.path.normpath(f['filename'])=='/work/adapter/c/mp4/gpac.c']
if not isomedia or not lines(isomedia):raise SystemExit('no GPAC ISO media source covered')
if not lines(adapter):raise SystemExit('selected C++ call site was not executed')
for group,suffix in ((isomedia,'/isom_read.c'),(isomedia,'/isom_intern.c'),(isomedia,'/box_funcs.c'),
                     (isomedia,'/box_code_base.c'),(isomedia,'/data_map.c'),(isomedia,'/stbl_read.c'),
                     (isomedia,'/sample_descs.c'),(isomedia,'/track.c'),(utils,'/bitstream.c')):
    if not lines([f for f in group if f['filename'].endswith(suffix)]):raise SystemExit(f'no coverage in {suffix}')
summary={'control_pass':True,'output':observed,'parser_source_files':len(isomedia),
         'parser_source_lines_covered':lines(isomedia),'call_site_lines_covered':lines(adapter),
         'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
