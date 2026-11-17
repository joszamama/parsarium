#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage/variant
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
# A second valid tagged MP3 carries the same audio frames under an ID3v2.4 tag with
# UTF-8 text frames and synchsafe frame sizes; the control is ID3v2.3 with ISO-8859-1
# text. It is profiled separately.
LLVM_PROFILE_FILE=/coverage/variant/variant-%m.profraw /work/replay /work/valid-v24.mp3 > /coverage/observed-v24.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-profdata merge -sparse /coverage/variant/variant-*.profraw -o /coverage/variant.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
for run in control variant; do
  llvm-cov export /work/replay -instr-profile="/coverage/$run.profdata" -format=lcov > "/coverage/$run.lcov"
  llvm-profdata show --function=copyFromUTF8 "/coverage/$run.profdata" > "/coverage/$run-utf8.txt"
done
python3 - <<'PYCODE'
import json
import os
import re
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
# The catalog records title and track counts; the harness also reports the first
# audio track's codec, rate and channels as libVLC exposes them.
expected = {'title': 'Parsarium', 'audio_tracks': 1, 'mp3_tracks': 1}
stream = {'audio_codec': 'mp3 ', 'rate': 8000, 'channels': 1}
if observed != {**expected, **stream}:
    raise SystemExit(f'control mismatch: {observed}')
variant = json.loads(Path('/coverage/observed-v24.json').read_text())
if variant != {**expected, **stream}:
    raise SystemExit(f'ID3v2.4 MP3 mismatch: {variant}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
vlc_prefix = '/work/source/modules/meta_engine/'
id3v2_prefix = '/work/taglib-1.13.1/taglib/mpeg/id3v2/'
def lines(suffix):
    return sum(f['summary']['lines']['covered'] for f in files
               if os.path.normpath(f['filename']).endswith(suffix))
vlc = [f for f in files if f['filename'].startswith(vlc_prefix)]
id3v2 = [f for f in files if f['filename'].startswith(id3v2_prefix)]
vlc_covered = sum(f['summary']['lines']['covered'] for f in vlc)
id3v2_covered = sum(f['summary']['lines']['covered'] for f in id3v2)
# VLC side: TagLib meta reader, native ID3v2 frame walker and text handling (headers
# compiled into es.c), tag-skipping stream filter, ES demuxer, MPEG audio packetizer.
vlc_parts = {name: lines(suffix) for name, suffix in (
    ('meta_reader', '/modules/meta_engine/taglib.cpp'),
    ('native_id3_tag', '/modules/meta_engine/ID3Tag.h'),
    ('native_id3_meta', '/modules/meta_engine/ID3Meta.h'),
    ('native_id3_text', '/modules/meta_engine/ID3Text.h'),
    ('skiptags', '/modules/stream_filter/skiptags.c'),
    ('es_demuxer', '/modules/demux/mpeg/es.c'),
    ('mpegaudio_packetizer', '/modules/packetizer/mpegaudio.c'))}
# TagLib side: the ID3v2 syntax engine (tag header, frame headers, frame factory,
# text frames) behind MPEG::File.
taglib_parts = {name: lines(suffix) for name, suffix in (
    ('mpeg_file', '/taglib/mpeg/mpegfile.cpp'),
    ('id3v2_tag', '/mpeg/id3v2/id3v2tag.cpp'),
    ('id3v2_header', '/mpeg/id3v2/id3v2header.cpp'),
    ('id3v2_frame', '/mpeg/id3v2/id3v2frame.cpp'),
    ('id3v2_frame_factory', '/mpeg/id3v2/id3v2framefactory.cpp'),
    ('id3v2_text_frame', '/mpeg/id3v2/frames/textidentificationframe.cpp'))}
missing = [name for parts in (vlc_parts, taglib_parts) for name, n in parts.items() if not n]
if not vlc_covered or not id3v2_covered or missing:
    raise SystemExit(f'MP3/ID3v2 parser sources not covered: {missing}')
call_site = lines('/work/harness.cpp')
if not call_site:
    raise SystemExit('no C++ harness call-site lines covered')
# The harness links only the ES demuxer and the TagLib meta reader on the parser side.
other = [f['filename'] for f in files
         if f['filename'].startswith(('/work/source/modules/demux/', '/work/source/modules/meta_engine/'))
         and not os.path.normpath(f['filename']).endswith((
             '/demux/mpeg/es.c', '/meta_engine/taglib.cpp', '/meta_engine/ID3Tag.h',
             '/meta_engine/ID3Meta.h', '/meta_engine/ID3Text.h', '/meta_engine/ID3Pictures.h'))
         and f['summary']['lines']['covered']]
if other:
    raise SystemExit(f'unexpected demuxer or meta source covered: {other}')
def covered_lines(run):
    out, name = {}, None
    for line in Path(f'/coverage/{run}.lcov').read_text().splitlines():
        if line.startswith('SF:'):
            name = os.path.normpath(line[3:])
            out.setdefault(name, set())
        elif line.startswith('DA:') and name:
            number, count = line[3:].split(',')[:2]
            if int(count):
                out[name].add(int(number))
    return out
control_lines, variant_lines = covered_lines('control'), covered_lines('variant')
def split(suffix):
    names = [name for name in set(control_lines) | set(variant_lines) if name.endswith(suffix)]
    c = set().union(*(control_lines.get(name, set()) for name in names))
    v = set().union(*(variant_lines.get(name, set()) for name in names))
    return {'control_only': len(c - v), 'variant_only': len(v - c)}
# TagLib parses v2.3 and v2.4 frame headers in separate branches of
# Frame::Header::setData; VLC's native ID3Text.h converts ISO-8859-1 and UTF-8 text in
# separate branches. Each run must reach lines the other does not.
differential = {'taglib_id3v2_frame': split('/taglib-1.13.1/taglib/mpeg/id3v2/id3v2frame.cpp'),
                'vlc_native_id3_text': split('/modules/meta_engine/ID3Text.h')}
for part, count in differential.items():
    if not count['control_only'] or not count['variant_only']:
        raise SystemExit(f'{part} did not separate ID3v2.3 control and ID3v2.4 MP3: {count}')
# Sparse profiles omit functions that never ran, so a missing entry counts as 0.
def calls(run):
    text = Path(f'/coverage/{run}-utf8.txt').read_text()
    return sum(int(n) for n in re.findall(r'Function count: (\d+)', text))
utf8 = {run: calls(run) for run in ('control', 'variant')}
if utf8['control'] or not utf8['variant']:
    raise SystemExit(f'TagLib UTF-8 text decoding did not separate control and ID3v2.4 MP3: {utf8}')
summary = {'control_pass': True, 'output': expected, 'stream': stream,
           'variant_output': variant,
           'variant_differential_lines': differential,
           'variant_taglib_utf8_decoder_calls': utf8,
           'parser_source_files': len(vlc),
           'parser_source_lines_covered': vlc_covered,
           'vlc_parser_lines_covered': vlc_parts,
           'underlying_source_files': len(id3v2),
           'underlying_source_lines_covered': id3v2_covered,
           'taglib_lines_covered': taglib_parts,
           'taglib_all_lines_covered': sum(f['summary']['lines']['covered'] for f in files
                                           if f['filename'].startswith('/work/taglib-1.13.1/taglib/')),
           'cpp_call_site_lines_covered': call_site,
           'vlc_core_lines_covered': sum(f['summary']['lines']['covered'] for f in files
                                         if f['filename'].startswith('/work/source/src/')),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYCODE
