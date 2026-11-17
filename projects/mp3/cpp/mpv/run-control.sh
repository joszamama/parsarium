#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage/variant
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
# A second valid file: the same MPEG audio frames as the control under an
# ID3v2.4 tag (synchsafe frame sizes, UTF-8 text) instead of ID3v2.3 (Latin-1).
# It is profiled separately.
LLVM_PROFILE_FILE=/coverage/variant/variant-%m.profraw /work/replay /work/valid-v24.mp3 > /coverage/observed-v24.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-profdata merge -sparse /coverage/variant/variant-*.profraw -o /coverage/variant.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
llvm-cov export /work/replay -instr-profile=/coverage/variant.profdata --summary-only > /coverage/variant/coverage.json
# Region segments of FFmpeg's ID3v2 reader for the source differential.
for run in control variant; do
  llvm-cov export /work/replay -instr-profile=/coverage/$run.profdata \
    /work/ffmpeg/libavformat/id3v2.c > /coverage/$run-id3v2.json
done
python3 - <<'PYCODE'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'title': 'Parsarium', 'codec': 'mp3', 'duration_ms': 1000}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
variant = json.loads(Path('/coverage/observed-v24.json').read_text())
if variant != expected:
    raise SystemExit(f'ID3v2.4 variant mismatch: {variant}')
def files(path):
    return json.loads(Path(path).read_text())['data'][0]['files']
control_files = files('/coverage/coverage.json')
variant_files = files('/coverage/variant/coverage.json')
def lines(entries, name):
    return sum(f['summary']['lines']['covered'] for f in entries if f['filename'] == name)
mpv_prefix, ffmpeg_prefix = '/work/source/demux/', '/work/ffmpeg/libavformat/'
id3v2_name = ffmpeg_prefix + 'id3v2.c'
parser = [f for f in control_files if f['filename'].startswith(mpv_prefix)]
covered = sum(f['summary']['lines']['covered'] for f in parser)
lavf = lines(control_files, mpv_prefix + 'demux_lavf.c')
if not parser or not covered or not lavf:
    raise SystemExit('no mpv demux_lavf source lines covered')
underlying = [f for f in control_files if f['filename'].startswith(ffmpeg_prefix)]
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
id3v2 = lines(control_files, id3v2_name)
mp3dec = lines(control_files, ffmpeg_prefix + 'mp3dec.c')
if not underlying or not underlying_covered or not id3v2:
    raise SystemExit('no FFmpeg ID3v2 reader source lines covered')
if not mp3dec:
    raise SystemExit('no FFmpeg MP3 demuxer source lines covered')
call_site = lines(control_files, '/work/harness.cpp')
if not call_site:
    raise SystemExit('no C++ harness call-site lines covered')
def regions(run):
    found = set()
    for source in files(f'/coverage/{run}-id3v2.json'):
        if source['filename'] == id3v2_name:
            found.update((line, column) for line, column, count, has_count, region_start, *_
                         in source['segments'] if has_count and region_start and count > 0)
    return found
control_regions, variant_regions = regions('control'), regions('variant')
variant_only = variant_regions - control_regions
if not variant_only:
    raise SystemExit('ID3v2.4 variant reached no id3v2.c regions the control did not')
summary = {'control_pass': True, 'output': observed,
           'variant_output': variant,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'demux_lavf_lines_covered': lavf,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_covered,
           'ffmpeg_id3v2_lines_covered': id3v2,
           'ffmpeg_mp3dec_lines_covered': mp3dec,
           'variant_id3v2_lines_covered': lines(variant_files, id3v2_name),
           'id3v2_regions': {'control': len(control_regions), 'variant': len(variant_regions),
                             'variant_only': len(variant_only),
                             'control_only': len(control_regions - variant_regions)},
           'cpp_call_site_lines_covered': call_site,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYCODE
