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

manifest = json.loads(Path('/work/manifest.json').read_text())
observed = json.loads(Path('/coverage/observed.json').read_text(encoding='utf-8'))
if observed != manifest['expected_output']:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']


def scoped(prefix):
    selected = [f for f in files if f['filename'].startswith(prefix)]
    return selected, sum(f['summary']['lines']['covered'] for f in selected), {
        f['filename'][len(prefix):]: f['summary']['lines']['covered'] for f in selected}


own_files, own, own_lines = scoped(manifest['coverage_subject_prefix'])
under_files, under, under_lines = scoped(manifest['underlying_coverage_subject_prefix'])
if not own_files or own == 0:
    raise SystemExit(f"no instrumented {manifest['package']} crate source lines covered")
if not under_files or under == 0:
    raise SystemExit('no instrumented toml_parser crate source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(own_files),
          'parser_source_lines_covered': own,
          'parser_file_lines_covered': own_lines,
          'underlying_source_files': len(under_files),
          'underlying_source_lines_covered': under,
          'underlying_file_lines_covered': under_lines,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
