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

def typed(text, keep_order):
    # Kind-aware view: 1 and 1.0 do not match; array order always counts.
    # picojson::object is std::map, so the parsed tree cannot keep source key
    # order: control objects are compared with sorted keys, and the printed
    # tree must already list keys in sorted order.
    def canon(value):
        if isinstance(value, tuple):
            pairs = [(k, canon(v)) for k, v in value[1]]
            return ('object', pairs if keep_order else sorted(pairs))
        if isinstance(value, list): return ('array', [canon(v) for v in value])
        return (type(value).__name__, value)
    return canon(json.loads(text, object_pairs_hook=lambda pairs: ('object', pairs)))

tree_text = Path('/coverage/tree.json').read_text(encoding='utf-8')
control_text = Path('/input/control').read_text(encoding='utf-8')
if typed(tree_text, True) != typed(control_text, False):
    raise SystemExit('parsed picojson value differs from valid control')
tree = json.loads(tree_text)
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
expected = json.loads(Path('/work/manifest.json').read_text())['expected_output']
if observed != expected:
    raise SystemExit(f'format-aware JSON summary differs: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
source = [f for f in files if f['filename'].startswith('/work/source/')]
parser = [f for f in source if f['filename'].endswith('/source/picojson.h')]
covered = sum(f['summary']['lines']['covered'] for f in parser)
if covered == 0:
    raise SystemExit('no picojson.h lines covered')
result = {'control_pass': True, 'output': observed, 'exact_nested_structure_match': True,
          'parser_source_files': len(source),
          'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in source),
          'format_specific_source_lines_covered': covered, 'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
