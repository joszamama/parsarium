#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE='/coverage/control-%m.profraw' /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay \
  -object /work/install/lib/libopenshot.so \
  -object /work/install/lib/libavformat.so.63 \
  -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'video':1,'audio':1,'width':2,'height':2,'video_codec':'h264','audio_codec':'aac'}
if observed!=expected: raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
def covered(prefix):
    found=[f for f in files if f['filename'].startswith(prefix)]
    return found,sum(f['summary']['lines']['covered'] for f in found)
def file_lines(found,name):
    return sum(f['summary']['lines']['covered'] for f in found if f['filename']==name)
openshot,openshot_lines=covered('/work/libopenshot/src/')
ffmpeg,ffmpeg_lines=covered('/work/ffmpeg/libavformat/')
reader_lines=file_lines(openshot,'/work/libopenshot/src/FFmpegReader.cpp')
mov_lines=file_lines(ffmpeg,'/work/ffmpeg/libavformat/mov.c')
if not openshot_lines or not reader_lines or not ffmpeg_lines or not mov_lines:
    raise SystemExit(f'libopenshot/FFmpeg MOV parser source missing: '
                     f'{openshot_lines}/{reader_lines}/{ffmpeg_lines}/{mov_lines}')
summary={'control_pass':True,'output':observed,
         'parser_source_files':len(openshot),'parser_source_lines_covered':openshot_lines,
         'ffmpeg_reader_source_lines_covered':reader_lines,
         'underlying_source_files':len(ffmpeg),'underlying_source_lines_covered':ffmpeg_lines,
         'mov_source_lines_covered':mov_lines,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PY
