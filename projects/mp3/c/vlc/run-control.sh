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
# The catalog records title and track counts; the harness also reports the
# first audio track's codec, rate and channels as libVLC exposes them.
expected = {'title': 'Parsarium', 'audio_tracks': 1, 'mp3_tracks': 1}
stream = {'audio_codec': 'mp3 ', 'rate': 8000, 'channels': 1}
if observed != {**expected, **stream}:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
def covered(selected):
    return sum(f['summary']['lines']['covered'] for f in selected)
def lines(name):
    return covered(f for f in files if f['filename'] == name)
vlc = '/work/source/modules/'
taglib = '/work/taglib-1.13.1/taglib/'
parser = [f for f in files if f['filename'].startswith(vlc)]
underlying = [f for f in files if f['filename'].startswith(taglib)]
# Each stage of VLC's tagged-MP3 path must execute: the tag-skipping stream
# filter, VLC's own ID3v2 reader called by the es demuxer, the MPEG audio frame
# parser, and TagLib's ID3v2 tag, frame factory and text frame parsers.
stages = {
    'skiptags_lines_covered': lines(vlc + 'stream_filter/skiptags.c'),
    'vlc_id3v2_tag_lines_covered': lines(vlc + 'meta_engine/ID3Tag.h'),
    'vlc_id3v2_frame_lines_covered': lines(vlc + 'meta_engine/ID3Meta.h') + lines(vlc + 'meta_engine/ID3Text.h'),
    'es_demuxer_lines_covered': lines(vlc + 'demux/mpeg/es.c'),
    'mpegaudio_packetizer_lines_covered': lines(vlc + 'packetizer/mpegaudio.c'),
    'taglib_id3v2_tag_lines_covered': lines(taglib + 'mpeg/id3v2/id3v2tag.cpp'),
    'taglib_id3v2_frame_lines_covered': lines(taglib + 'mpeg/id3v2/id3v2framefactory.cpp')
        + lines(taglib + 'mpeg/id3v2/frames/textidentificationframe.cpp'),
}
missing = [name for name, value in stages.items() if not value]
if not parser or not underlying or missing:
    raise SystemExit(f'VLC MP3/ID3v2 parser stage not covered: {missing}')
# The harness links only these plugins; nothing else may claim the input.
allowed = {vlc + 'demux/mpeg/es.c', vlc + 'stream_filter/skiptags.c'}
other = [f['filename'] for f in parser if f['summary']['lines']['covered']
         and f['filename'].startswith((vlc + 'demux/', vlc + 'stream_filter/'))
         and f['filename'] not in allowed]
if other:
    raise SystemExit(f'unexpected demuxer or stream filter source covered: {other}')
summary = {'control_pass': True, 'output': expected, 'stream': stream,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered(parser),
           **stages,
           # Wrapper and access lines are inside the parser prefix; listed so
           # they can be separated from the parsing stages above.
           'taglib_plugin_wrapper_lines_covered': lines(vlc + 'meta_engine/taglib.cpp'),
           'file_access_lines_covered': covered(f for f in parser
                                                if f['filename'].startswith(vlc + 'access/')),
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': covered(underlying),
           'vlc_core_lines_covered': covered(f for f in files
                                             if f['filename'].startswith('/work/source/src/')),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYCODE
