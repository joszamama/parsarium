#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/tree.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
from hashlib import sha256
import json
from pathlib import Path

manifest = json.loads(Path('/work/manifest.json').read_text())
tree = json.loads(Path('/coverage/tree.json').read_text(encoding='utf-8'))
counts = {}
def visit(node, depth):
    counts[node[0]] = counts.get(node[0], 0) + 1
    if node[0] == 'map':
        return max([depth] + [visit(value, depth + 1) for _, value in node[1]])
    if node[0] == 'seq':
        return max([depth] + [visit(value, depth + 1) for value in node[1]])
    return depth - 1
depth = visit(tree, 1)
observed = {'max_depth': depth, 'nodes': dict(sorted(counts.items())), 'root': tree[0], 'tree': tree,
            'tree_sha256': sha256(json.dumps(tree, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()}
if observed != manifest['expected_output']:
    raise SystemExit(f"typed YAML tree differs from the expected control tree: {observed['tree']}")
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
source = [f for f in files if f['filename'].startswith(manifest['coverage_subject_prefix'])]
parser = [f for f in source if f['filename'].endswith(manifest['format_specific_coverage_file_suffix'])]
covered = sum(f['summary']['lines']['covered'] for f in parser)
if covered == 0:
    raise SystemExit(f"no {manifest['package']} parser source lines covered")
result = {'control_pass': True, 'output': observed, 'exact_typed_tree_match': True,
          'parser_source_files': len(source),
          'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in source),
          'format_specific_source_lines_covered': covered, 'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(result, ensure_ascii=False))
PY
