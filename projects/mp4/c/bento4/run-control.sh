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
expected={'brand':'isom','tracks':2,'video_tracks':1,'audio_tracks':1,'duration_ms':1000}
if observed!=expected:raise SystemExit(f'control mismatch: {observed}')
root='/work/Bento4-1.6.0-641/Source/C++/'
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines=lambda group:sum(f['summary']['lines']['covered'] for f in group)
binding=[f for f in files if f['filename'].startswith(root+'CApi/')]
core=[f for f in files if f['filename'].startswith(root+'Core/')]
system=[f for f in files if f['filename'].startswith(root+'System/')]
if not binding or not lines(binding):raise SystemExit('no Bento4 C binding source covered')
if not core or not lines(core):raise SystemExit('no Bento4 AP4 core source covered')
for group,suffix in ((binding,'/Bento4C.cpp'),(core,'/Ap4File.cpp'),(core,'/Ap4AtomFactory.cpp'),
                     (core,'/Ap4ContainerAtom.cpp'),(core,'/Ap4FtypAtom.cpp'),(core,'/Ap4MoovAtom.cpp'),
                     (core,'/Ap4MvhdAtom.cpp'),(core,'/Ap4TrakAtom.cpp'),(core,'/Ap4HdlrAtom.cpp'),
                     (core,'/Ap4Movie.cpp'),(core,'/Ap4Track.cpp'),(core,'/Ap4ByteStream.cpp'),
                     (system,'/Ap4StdCFileByteStream.cpp')):
    if not lines([f for f in group if f['filename'].endswith(suffix)]):raise SystemExit(f'no coverage in {suffix}')
summary={'control_pass':True,'output':observed,'parser_source_files':len(binding),
         'parser_source_lines_covered':lines(binding),'underlying_source_files':len(core),
         'underlying_source_lines_covered':lines(core),'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PYCODE
