#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
/work/llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
/work/llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = json.loads("{\"sample_rate\":44100,\"channels\":1,\"frames\":11,\"samples_per_channel\":12672,\"pcm_samples\":12672,\"pcm_f32_sha256\":\"950a4b2c13148eef937e478e683959d5450f71436c95e81423456a85b63dfb8a\"}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']


def scoped(crate):
    selected = [f for f in files if f'/{crate}/' in f['filename']]
    return selected, sum(f['summary']['lines']['covered'] for f in selected), {
        f['filename'].split(f'/{crate}/', 1)[1]: f['summary']['lines']['covered'] for f in selected}


own_files, own, own_lines = scoped('rusty_mp3-1.0.6')
if not own_files or own == 0:
    raise SystemExit('no instrumented rusty_mp3-1.0.6 source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(own_files),
          'parser_source_lines_covered': own,
          'parser_file_lines_covered': own_lines,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
