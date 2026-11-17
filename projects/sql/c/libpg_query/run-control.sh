#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/tree.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 /work/summarize.py --tree /coverage/tree.json > /coverage/observed.json
python3 - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path('/work/manifest.json').read_text())
observed = json.loads(Path('/coverage/observed.json').read_text())
if observed != manifest['expected_output']:
    raise SystemExit(f'libpg_query parse-tree summary differs from the oracle: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
source = [f for f in files if f['filename'].startswith(manifest['coverage_subject_prefix'])
          and f['summary']['lines']['covered'] > 0]
grammar = [f for f in source if f['filename'].endswith(manifest['format_specific_coverage_file_suffix'])]
covered = sum(f['summary']['lines']['covered'] for f in grammar)
if covered == 0:
    raise SystemExit('no PostgreSQL grammar source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(source),
          'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in source),
          'format_specific_source_lines_covered': covered, 'coverage': '/coverage/coverage.json'}
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': source}]}) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
