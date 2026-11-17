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

observed = json.loads(Path('/coverage/observed.json').read_text(encoding='utf-8'))
expected = {"statement_count": 1, "statements": [{
    "kind": "select", "tables": ["customers", "orders"], "select_items": 3, "joins": 1,
    "where": True, "group_by": 1, "order_by": 1, "functions": ["count", "sum"],
    "literals": [["number", "10"], ["string", "paid"]]}]}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
crate = '/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/typedpg_pg_query-0.7.3/'
# The build script compiles the libpg_query files it patches (patches.rs) from OUT_DIR/patched
# copies; map those to the copies kept beside the crate source (patched-libpg_query/).
out_dir = Path('/work/typedpg-out-dir.txt').read_text().strip() + '/patched/'
coverage = json.loads(Path('/coverage/coverage.json').read_text())
for entry in coverage['data'][0]['files']:
    if entry['filename'].startswith(out_dir):
        entry['filename'] = crate + 'patched-libpg_query/' + entry['filename'][len(out_dir):]
Path('/coverage/coverage.json').write_text(json.dumps(coverage))
files = coverage['data'][0]['files']

def covered(prefix, suffix=''):
    selected = [f for f in files if f['filename'].startswith(prefix) and f['filename'].endswith(suffix)]
    return selected, sum(f['summary']['lines']['covered'] for f in selected)

rust_files, rust_lines = covered(crate + 'src/')
csrc_files, csrc_lines = covered(crate + 'csrc/')
c_files, c_lines = covered(crate + 'libpg_query/')
patched_files, patched_lines = covered(crate + 'patched-libpg_query/')
_, gram_lines = covered(crate + 'libpg_query/src/postgres/src_backend_parser_gram.c')
_, scan_lines = covered(crate + 'libpg_query/src/postgres/src_backend_parser_scan.c')
if not rust_files or rust_lines == 0:
    raise SystemExit('no instrumented typedpg_pg_query binding lines covered')
if not c_files or c_lines == 0 or gram_lines == 0 or scan_lines == 0:
    raise SystemExit('libpg_query C grammar or scanner was not instrumented or not reached')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(rust_files),
          'parser_source_lines_covered': rust_lines,
          'underlying_source_files': len(c_files),
          'underlying_source_lines_covered': c_lines,
          'catalog_c_lines_covered': csrc_lines,
          'patched_libpg_query_files': len(patched_files),
          'patched_libpg_query_lines_covered': patched_lines,
          'native_gram_lines_covered': gram_lines,
          'native_scan_lines_covered': scan_lines,
          'parser_file_lines_covered': {f['filename'][len(crate):]: f['summary']['lines']['covered']
                                        for f in rust_files},
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
