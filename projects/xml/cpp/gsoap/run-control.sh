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
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
# gSOAP's XML engine (stdsoap2.cpp/.h) and DOM parser (dom.cpp); soapcpp2-generated code in /work/gen is excluded.
parser_files = [f for f in files if f['filename'].startswith('/work/source/gsoap/')]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
names = {f['filename'] for f in parser_files}
if not {'/work/source/gsoap/stdsoap2.cpp', '/work/source/gsoap/dom.cpp'} <= names or covered == 0:
    raise SystemExit('no instrumented gSOAP source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'format_specific_source_lines_covered': sum(
              f['summary']['lines']['covered'] for f in parser_files
              if f['filename'].endswith('/gsoap/dom.cpp')),
          'parser_file_lines_covered': {f['filename'].removeprefix('/work/source/'): f['summary']['lines']['covered']
                                        for f in parser_files},
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
