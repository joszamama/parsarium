#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'vertices': 3, 'faces': 1, 'face': [0, 1, 2]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']

def lines(selected):
    return sum(f['summary']['lines']['covered'] for f in selected)

front = [f for f in files if f['filename'].startswith('/work/source/IO/PLY/')]
under = [f for f in files if f['filename'].startswith('/work/source/IO/PLY/vtkPLY.')]
reader = lines(f for f in front if f['filename'].endswith('/vtkPLYReader.cxx'))
parser = lines(f for f in under if f['filename'].endswith('/vtkPLY.cxx'))
if min(lines(front), reader, lines(under), parser) <= 0:
    raise SystemExit('no instrumented VTK vtkPLYReader and bundled vtkPLY source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(front),
          'parser_source_lines_covered': lines(front),
          'format_specific_source_lines_covered': reader,
          'underlying_source_files': len(under),
          'underlying_source_lines_covered': lines(under),
          'underlying_format_specific_source_lines_covered': parser,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
