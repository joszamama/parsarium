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
expected = json.loads("{\"sample_rate\":44100,\"channels\":1,\"layer\":3,\"bitrate_kbps\":64,\"frames\":11,\"frame_bytes\":2298,\"frame_samples_per_channel\":12672,\"samples_per_channel\":12672,\"pcm_samples\":12672,\"pcm_sha256\":\"1106d468c6a515a4c554991af6ab95e9c811e8e34005478ee81dd1e3a8063edb\",\"minimp3_compat_pcm_sha256\":\"d8bde33ad59477f815f1194dd04517bf8b5949807f5bf01fb19a9ab4e3a99364\"}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']


def scoped(crate):
    selected = [f for f in files if f'/{crate}/' in f['filename']]
    return selected, sum(f['summary']['lines']['covered'] for f in selected), {
        f['filename'].split(f'/{crate}/', 1)[1]: f['summary']['lines']['covered'] for f in selected}


own_files, own, own_lines = scoped('nanomp3-0.2.0')
if not own_files or own == 0:
    raise SystemExit('no instrumented nanomp3-0.2.0 source lines covered')
under_files, under, under_lines = scoped('nanomp3-core-0.2.0')
if not under_files or under == 0:
    raise SystemExit('no instrumented nanomp3-core-0.2.0 source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(own_files),
          'parser_source_lines_covered': own,
          'parser_file_lines_covered': own_lines,
          'underlying_source_files': len(under_files),
          'underlying_source_lines_covered': under,
          'underlying_file_lines_covered': under_lines,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
