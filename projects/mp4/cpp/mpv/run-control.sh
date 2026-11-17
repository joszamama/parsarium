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
llvm-cov export /work/replay -instr-profile=/coverage/variant.profdata --summary-only > /coverage/variant/coverage.json
for box in ctts stss; do
  for run in control variant; do
    llvm-profdata show --function="mov_read_$box" "/coverage/$run.profdata" > "/coverage/$run-$box.txt"
  done
done
python3 - <<'PYCODE'
import json
import re
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'container': 'mov,mp4,m4a,3gp,3g2,mj2', 'title': 'Parsarium',
            'video_codec': 'h264', 'audio_codec': 'aac'}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
variant = json.loads(Path('/coverage/observed-3s.json').read_text())
variant_expected = {**expected, 'title': ''}
if variant != variant_expected:
    raise SystemExit(f'3 s MP4 mismatch: {variant}')
def files(path):
    return json.loads(Path(path).read_text())['data'][0]['files']
control_files = files('/coverage/coverage.json')
variant_files = files('/coverage/variant/coverage.json')
def lines(entries, name):
    return sum(f['summary']['lines']['covered'] for f in entries if f['filename'] == name)
mpv_prefix, ffmpeg_prefix = '/work/source/demux/', '/work/ffmpeg/libavformat/'
parser = [f for f in control_files if f['filename'].startswith(mpv_prefix)]
covered = sum(f['summary']['lines']['covered'] for f in parser)
lavf = lines(control_files, mpv_prefix + 'demux_lavf.c')
if not parser or not covered or not lavf:
    raise SystemExit('no mpv demux_lavf source lines covered')
underlying = [f for f in control_files if f['filename'].startswith(ffmpeg_prefix)]
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
mov = lines(control_files, ffmpeg_prefix + 'mov.c')
if not underlying or not underlying_covered or not mov:
    raise SystemExit('no FFmpeg MOV/MP4 demuxer source lines covered')
call_site = lines(control_files, '/work/harness.cpp')
if not call_site:
    raise SystemExit('no C++ harness call-site lines covered')
# Sparse profiles omit functions that never ran, so a missing entry counts as 0.
def calls(run, box):
    text = Path(f'/coverage/{run}-{box}.txt').read_text()
    return sum(int(n) for n in re.findall(r'Function count: (\d+)', text))
readers = {box: {run: calls(run, box) for run in ('control', 'variant')} for box in ('ctts', 'stss')}
for box, count in readers.items():
    if count['control'] or not count['variant']:
        raise SystemExit(f'mov.c {box} reader did not separate control and 3 s MP4: {count}')
summary = {'control_pass': True, 'output': observed,
           'variant_output': variant,
           'variant_mov_box_reader_calls': readers,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'demux_lavf_lines_covered': lavf,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_covered,
           'mov_lines_covered': mov,
           'variant_mov_lines_covered': lines(variant_files, ffmpeg_prefix + 'mov.c'),
           'variant_demux_lavf_lines_covered': lines(variant_files, mpv_prefix + 'demux_lavf.c'),
           'cpp_call_site_lines_covered': call_site,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYCODE
