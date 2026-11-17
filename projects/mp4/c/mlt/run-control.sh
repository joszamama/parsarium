#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE='/coverage/control-%m.profraw' /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay \
  -object /work/install/lib/libavformat.so.63 \
  -object /work/install/lib/mlt-7/libmltavformat.so \
  -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'streams':2,'video_codec':'h264','audio_codec':'aac','width':2,'height':2}
if observed!=expected: raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
def covered(prefix):
    found=[f for f in files if f['filename'].startswith(prefix)]
    return found,sum(f['summary']['lines']['covered'] for f in found)
plugin,plugin_lines=covered('/work/mlt/src/modules/avformat/')
ffmpeg,ffmpeg_lines=covered('/work/ffmpeg/libavformat/')
mov_lines=sum(f['summary']['lines']['covered'] for f in ffmpeg
              if f['filename']=='/work/ffmpeg/libavformat/mov.c')
if not plugin_lines or not ffmpeg_lines or not mov_lines:
    raise SystemExit(f'MLT/FFmpeg MOV parser source missing: {plugin_lines}/{ffmpeg_lines}/{mov_lines}')
summary={'control_pass':True,'output':observed,
         'parser_source_files':len(plugin),'parser_source_lines_covered':plugin_lines,
         'underlying_source_files':len(ffmpeg),'underlying_source_lines_covered':ffmpeg_lines,
         'mov_source_lines_covered':mov_lines,'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PY
