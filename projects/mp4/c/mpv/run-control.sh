#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'container': 'mov,mp4,m4a,3gp,3g2,mj2', 'title': 'Parsarium',
            'video_codec': 'h264', 'audio_codec': 'aac'}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'].startswith('/work/source/demux/')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
lavf = sum(f['summary']['lines']['covered'] for f in parser if f['filename'].endswith('/demux_lavf.c'))
if not parser or not covered or not lavf:
    raise SystemExit('no mpv demux_lavf source lines covered')
underlying = [f for f in files if f['filename'].startswith('/work/ffmpeg/libavformat/')]
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
mov = sum(f['summary']['lines']['covered'] for f in underlying if f['filename'].endswith('/mov.c'))
if not underlying or not underlying_covered or not mov:
    raise SystemExit('no FFmpeg MOV/MP4 demuxer source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
