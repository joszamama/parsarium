#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
LLVM_PROFILE_FILE=/tmp/tree.profraw /work/replay /input/control --tree > /coverage/tree.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {
    'arrays': 3, 'booleans': 2, 'max_depth': 4, 'nulls': 1,
    'numbers': [-2.5, 1, 1, 2, 2], 'objects': 5, 'root': 'object',
    'strings': ['café "quoted"', 'go', 'json', 'parsarium', 'rfc8259'],
    'top_level_keys': ['enabled', 'missing', 'name', 'nested', 'ratio', 'tags', 'version'],
}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
# The full tree printed from jansson's json_t values must equal the control's
# exact nested structure, including key order and integer/real distinction.
tree = json.loads(Path('/coverage/tree.json').read_text(), object_pairs_hook=list)
reference = json.loads(Path('/input/control').read_text(), object_pairs_hook=list)
def typed(value):
    if isinstance(value, list):
        return [typed(item) for item in value]
    if isinstance(value, tuple):
        return (value[0], typed(value[1]))
    return (type(value).__name__, value)
if typed(tree) != typed(reference):
    raise SystemExit('control nested structure mismatch')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
parser_files = [f for f in files if f['filename'].startswith('/work/jansson-src/')]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
if not parser_files or covered == 0:
    raise SystemExit('no instrumented jansson source lines covered')
load = [f for f in parser_files if f['filename'].endswith('/src/load.c')]
result = {'control_pass': True, 'output': observed,
          'exact_nested_structure_match': True,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'load_c_lines_covered': sum(f['summary']['lines']['covered'] for f in load),
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
