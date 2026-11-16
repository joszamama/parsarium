#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PYCODE'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'method': 'GET', 'path': '/parsarium?x=1', 'version': '1.1', 'host': 'example.test'}
if observed != expected: raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'].startswith('/work/boost_1_92_0/boost/beast/http/')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
state_machine = sum(f['summary']['lines']['covered'] for f in parser
                    if f['filename'].endswith('/impl/basic_parser.ipp'))
if not parser or not covered or not state_machine:
    raise SystemExit('no instrumented Boost.Beast HTTP parser lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser), 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYCODE
