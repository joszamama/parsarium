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
expected = {'title': 'Parsarium', 'codec': 'mp3', 'duration_ms': 1000}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
def lines(group, suffix):
    return sum(f['summary']['lines']['covered'] for f in group if f['filename'].endswith(suffix))
parser = [f for f in files if f['filename'].startswith('/work/source/demux/')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
lavf = lines(parser, '/demux_lavf.c')
if not parser or not covered or not lavf:
    raise SystemExit('no mpv demux_lavf source lines covered')
underlying = [f for f in files if f['filename'].startswith('/work/ffmpeg/libavformat/')]
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
id3v2 = lines(underlying, '/id3v2.c')
mp3dec = lines(underlying, '/mp3dec.c')
if not underlying or not underlying_covered or not id3v2:
    raise SystemExit('no FFmpeg ID3v2 reader source lines covered')
if not mp3dec:
    raise SystemExit('no FFmpeg MP3 demuxer source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'demux_lavf_lines_covered': lavf,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_covered,
           'ffmpeg_id3v2_lines_covered': id3v2,
           'ffmpeg_mp3dec_lines_covered': mp3dec,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
