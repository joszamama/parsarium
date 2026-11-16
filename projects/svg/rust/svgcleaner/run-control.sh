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
expected = json.loads("{\"rects\":2,\"has_svg\":true}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
parser_files = [f for f in files if '/svgcleaner-0.9.5/' in f['filename']]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
if not parser_files or covered == 0:
    raise SystemExit('no instrumented svgcleaner crate source lines covered')
underlying = [f for f in files if f['filename'].startswith(
    '/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/svgdom-0.10.5/')]
underlying_covered = sum(f['summary']['lines']['covered'] for f in underlying)
if not any(f['filename'].endswith('/src/parser/parser.rs') and
           f['summary']['lines']['covered'] > 0 for f in underlying):
    raise SystemExit('svgdom SVG parser source was not covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'underlying_source_files': len(underlying),
          'underlying_source_lines_covered': underlying_covered,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
