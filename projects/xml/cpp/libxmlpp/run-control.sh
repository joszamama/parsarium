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
expected = {'attributes': ['version=1', 'id=a1', '{urn:parsarium:catalog}lang=es', 'id=b2'],
            'elements': ['{urn:parsarium:catalog}catalog', '{urn:parsarium:item}item',
                         '{urn:parsarium:item}item', '{urn:parsarium:item}name',
                         '{urn:parsarium:item}note'],
            'max_depth': 3, 'namespace_declarations': 2,
            'namespaces': ['urn:parsarium:catalog', 'urn:parsarium:item'],
            'root': '{urn:parsarium:catalog}catalog',
            'text': ['Café & té', 'Zürich <HQ>', 'x < y']}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
wrapper = [f for f in files if f['filename'].startswith('/work/source/')]
underlying = [f for f in files if f['filename'].startswith('/work/libxml2-source/')]
covered = lambda rows: sum(f['summary']['lines']['covered'] for f in rows)
if covered(wrapper) <= 0 or covered(underlying) <= 0:
    raise SystemExit('no covered libxml++ or libxml2 source lines')
if sum(f['summary']['lines']['covered'] for f in underlying
       if f['filename'].endswith('/parser.c')) <= 0:
    raise SystemExit('no covered native libxml2 parser.c lines')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(wrapper), 'parser_source_lines_covered': covered(wrapper),
          'underlying_source_files': len(underlying),
          'underlying_source_lines_covered': covered(underlying),
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
