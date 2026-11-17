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
expected = json.loads("{\"width\":2,\"height\":1,\"rgb\":[255,0,0,0,255,0]}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
registry = '/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/'
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']

def covered(prefix, suffix=''):
    selected = [f for f in files
                if f['filename'].startswith(prefix) and f['filename'].endswith(suffix)]
    return selected, sum(f['summary']['lines']['covered'] for f in selected)

rust_files, rust_lines = covered(registry + 'fltk-1.5.23/')
fltk_files, fltk_lines = covered(registry + 'fltk-sys-1.5.23/cfltk/fltk/src/')
_, pnm_lines = covered(registry + 'fltk-sys-1.5.23/cfltk/fltk/src/Fl_PNM_Image.cxx')
_, shim_lines = covered(registry + 'fltk-sys-1.5.23/cfltk/src/cfl_image.cpp')
if not rust_files or rust_lines == 0:
    raise SystemExit('no instrumented fltk Rust crate source lines covered')
if not fltk_files or fltk_lines == 0 or pnm_lines == 0:
    raise SystemExit('FLTK C++ Fl_PNM_Image.cxx source was not instrumented or not reached')
if shim_lines == 0:
    raise SystemExit('cfltk cfl_image.cpp shim was not instrumented or not reached')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(rust_files),
          'parser_source_lines_covered': rust_lines,
          'underlying_source_files': len(fltk_files),
          'underlying_source_lines_covered': fltk_lines,
          'native_pnm_loader_lines_covered': pnm_lines,
          'cfltk_shim_lines_covered': shim_lines,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
