#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/tree.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
tree = json.loads(Path('/coverage/tree.json').read_text())
reference = json.loads(Path('/input/control').read_text())
if tree != reference:
    raise SystemExit('parsed yyjson tree differs from valid control')
arrays = objects = booleans = nulls = max_depth = 0
numbers, strings = [], []
def walk(value, depth):
    global arrays, objects, booleans, nulls, max_depth
    if isinstance(value, dict):
        objects += 1
        max_depth = max(max_depth, depth)
        for child in value.values(): walk(child, depth + 1)
    elif isinstance(value, list):
        arrays += 1
        max_depth = max(max_depth, depth)
        for child in value: walk(child, depth + 1)
    elif value is None: nulls += 1
    elif isinstance(value, bool): booleans += 1
    elif isinstance(value, (int, float)): numbers.append(value)
    elif isinstance(value, str): strings.append(value)
walk(tree, 1)
observed = {'arrays': arrays, 'booleans': booleans, 'max_depth': max_depth,
            'nulls': nulls, 'numbers': sorted(numbers), 'objects': objects,
            'root': 'object' if isinstance(tree, dict) else 'array',
            'strings': sorted(strings)}
if isinstance(tree, dict): observed['top_level_keys'] = sorted(tree)
else: observed['top_level_items'] = len(tree)
expected = {'arrays': 3, 'booleans': 2, 'max_depth': 4, 'nulls': 1,
            'numbers': [-2.5, 1, 1, 2, 2], 'objects': 5, 'root': 'object',
            'strings': ['café "quoted"', 'go', 'json', 'parsarium', 'rfc8259'],
            'top_level_keys': ['enabled', 'missing', 'name', 'nested', 'ratio', 'tags', 'version']}
if observed != expected:
    raise SystemExit(f'format-aware JSON summary differs: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
source = [f for f in coverage['data'][0]['files'] if f['filename'].startswith('/work/yyjson-src/')]
lines = sum(f['summary']['lines']['covered'] for f in source)
if lines == 0:
    raise SystemExit('no yyjson parser source lines covered')
result = {'control_pass': True, 'output': observed, 'exact_nested_structure_match': True,
          'parser_source_files': len(source), 'parser_source_lines_covered': lines,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
