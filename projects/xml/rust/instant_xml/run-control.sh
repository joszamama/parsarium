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

observed = json.loads(Path('/coverage/observed.json').read_text(encoding='utf-8'))
expected = json.loads(Path('/work/manifest.json').read_text())['expected_output']
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']


def scoped(crate):
    selected = [f for f in files if f'/{crate}/' in f['filename']]
    return selected, sum(f['summary']['lines']['covered'] for f in selected), {
        f['filename'].split(f'/{crate}/', 1)[1]: f['summary']['lines']['covered'] for f in selected}


own_files, own, own_lines = scoped('instant-xml-0.7.7')
xp_files, xp, xp_lines = scoped('xmlparser-0.13.6')
if not own_files or own == 0:
    raise SystemExit('no instrumented instant-xml crate source lines covered')
if not xp_files or xp == 0:
    raise SystemExit('no instrumented xmlparser crate source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(own_files),
          'parser_source_lines_covered': own,
          'parser_file_lines_covered': own_lines,
          'underlying_source_files': len(xp_files),
          'underlying_source_lines_covered': xp,
          'underlying_file_lines_covered': xp_lines,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
