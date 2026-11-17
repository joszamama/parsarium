#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
# The catalog records title, track counts and duration; the harness also
# reports the first video and audio track as libVLC exposes them.
expected = {'title': 'Parsarium', 'video_tracks': 1, 'audio_tracks': 1, 'duration_ms': 1000}
stream = {'video_codec': 'h264', 'audio_codec': 'mp4a', 'width': 2, 'height': 2}
if observed != {**expected, **stream}:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
prefix = '/work/source/modules/demux/mp4/'
def lines(name):
    return sum(f['summary']['lines']['covered'] for f in files if f['filename'] == prefix + name)
parser = [f for f in files if f['filename'].startswith(prefix)]
covered = sum(f['summary']['lines']['covered'] for f in parser)
boxes, demux, tracks, meta = lines('libmp4.c'), lines('mp4.c'), lines('essetup.c'), lines('meta.c')
if not parser or not covered or not boxes or not demux or not tracks or not meta:
    raise SystemExit('no VLC MP4 box parser, demuxer, track setup or metadata source covered')
# The harness links only the file access and MP4 demuxer plugins.
other = [f['filename'] for f in files if f['filename'].startswith('/work/source/modules/demux/')
         and not f['filename'].startswith(prefix) and f['summary']['lines']['covered']]
if other:
    raise SystemExit(f'unexpected demuxer source covered: {other}')
summary = {'control_pass': True, 'output': expected, 'stream': stream,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'box_parser_lines_covered': boxes, 'demuxer_lines_covered': demux,
           'track_setup_lines_covered': tracks, 'metadata_lines_covered': meta,
           'vlc_core_lines_covered': sum(f['summary']['lines']['covered'] for f in files
                                         if f['filename'].startswith('/work/source/src/')),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYCODE
