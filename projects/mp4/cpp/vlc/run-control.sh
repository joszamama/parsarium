#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage/variant
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
# A second valid MP4 (3 s, 16 x 16, no title) carries stss and ctts boxes that the
# control lacks; it is profiled separately.
LLVM_PROFILE_FILE=/coverage/variant/variant-%m.profraw /work/replay /work/valid-3s.mp4 > /coverage/observed-3s.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-profdata merge -sparse /coverage/variant/variant-*.profraw -o /coverage/variant.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
for box in ctts stss; do
  for run in control variant; do
    llvm-profdata show --function="MP4_ReadBox_$box" "/coverage/$run.profdata" > "/coverage/$run-$box.txt"
  done
done
python3 - <<'PYCODE'
import json
import re
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
# The catalog records title, track counts and duration; the harness also
# reports the first video and audio track as libVLC exposes them.
expected = {'title': 'Parsarium', 'video_tracks': 1, 'audio_tracks': 1, 'duration_ms': 1000}
stream = {'video_codec': 'h264', 'audio_codec': 'mp4a', 'width': 2, 'height': 2}
if observed != {**expected, **stream}:
    raise SystemExit(f'control mismatch: {observed}')
variant = json.loads(Path('/coverage/observed-3s.json').read_text())
variant_expected = {'title': '', 'video_tracks': 1, 'audio_tracks': 1, 'duration_ms': 3000,
                    'video_codec': 'h264', 'audio_codec': 'mp4a', 'width': 16, 'height': 16}
if variant != variant_expected:
    raise SystemExit(f'3 s MP4 mismatch: {variant}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
prefix = '/work/source/modules/demux/mp4/'
def lines(name):
    return sum(f['summary']['lines']['covered'] for f in files if f['filename'] == name)
parser = [f for f in files if f['filename'].startswith(prefix)]
covered = sum(f['summary']['lines']['covered'] for f in parser)
boxes, demux = lines(prefix + 'libmp4.c'), lines(prefix + 'mp4.c')
tracks, meta = lines(prefix + 'essetup.c'), lines(prefix + 'meta.c')
if not parser or not covered or not boxes or not demux or not tracks or not meta:
    raise SystemExit('no VLC MP4 box parser, demuxer, track setup or metadata source covered')
call_site = lines('/work/harness.cpp')
if not call_site:
    raise SystemExit('no C++ harness call-site lines covered')
# The harness links only the file access and MP4 demuxer plugins.
other = [f['filename'] for f in files if f['filename'].startswith('/work/source/modules/demux/')
         and not f['filename'].startswith(prefix) and f['summary']['lines']['covered']]
if other:
    raise SystemExit(f'unexpected demuxer source covered: {other}')
# Sparse profiles omit functions that never ran, so a missing entry counts as 0.
def calls(run, box):
    text = Path(f'/coverage/{run}-{box}.txt').read_text()
    return sum(int(n) for n in re.findall(r'Function count: (\d+)', text))
readers = {box: {run: calls(run, box) for run in ('control', 'variant')} for box in ('ctts', 'stss')}
for box, count in readers.items():
    if count['control'] or not count['variant']:
        raise SystemExit(f'libmp4.c {box} reader did not separate control and 3 s MP4: {count}')
summary = {'control_pass': True, 'output': expected, 'stream': stream,
           'variant_output': variant,
           'variant_box_reader_calls': readers,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'box_parser_lines_covered': boxes, 'demuxer_lines_covered': demux,
           'track_setup_lines_covered': tracks, 'metadata_lines_covered': meta,
           'cpp_call_site_lines_covered': call_site,
           'vlc_core_lines_covered': sum(f['summary']['lines']['covered'] for f in files
                                         if f['filename'].startswith('/work/source/src/')),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYCODE
