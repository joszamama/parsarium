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
expected = {'files': 1, 'actors': 1, 'points': 3, 'cells': 1}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']

def lines(selected):
    return sum(f['summary']['lines']['covered'] for f in selected)

# F3D files: the C binding, the native plugin sources, and its generated
# reader table.
front = [f for f in files if f['filename'].startswith('/work/f3d/')]
c_api = lines(f for f in front if f['filename'].endswith('/c/scene_c_api.cxx'))
under = [f for f in files if f['filename'].startswith('/work/vtk/source/IO/PLY/vtkPLY')]
reader = lines(f for f in front if f['filename'].endswith('/plugins/native/module/vtkF3DPLYReader.cxx'))
plugin = lines(f for f in front if f['filename'].endswith('/plugins/native/reader_PLYReader.h'))
parser = lines(f for f in under if f['filename'].endswith('/vtkPLY.cxx'))
vtk_reader = lines(f for f in under if f['filename'].endswith('/vtkPLYReader.cxx'))
if min(lines(front), c_api, reader, plugin, lines(under), parser, vtk_reader) <= 0:
    raise SystemExit('no instrumented F3D C API, PLY plugin, and VTK vtkPLYReader/vtkPLY source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(front),
          'parser_source_lines_covered': lines(front),
          'format_specific_source_lines_covered': reader,
          'c_api_lines_covered': c_api,
          'plugin_reader_lines_covered': plugin,
          'underlying_source_files': len(under),
          'underlying_source_lines_covered': lines(under),
          'underlying_format_specific_source_lines_covered': parser,
          'underlying_reader_lines_covered': vtk_reader,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
