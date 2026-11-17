"""Check the pg_query_parse() summary and summarize LLVM line coverage of the extension and libpg_query.

target.json keys the expected summary by control SHA-256, so the same image checks both valid controls."""
from hashlib import sha256
import json
from pathlib import Path

coverage_dir = Path('/coverage')
observed = json.loads((coverage_dir / 'observed.json').read_text())
digest = sha256(Path('/input/control').read_bytes()).hexdigest()
expected = json.loads(Path('/work/target.json').read_text())['expected_output_by_control_sha256'].get(digest)
if expected is None:
    raise SystemExit(f'no expected output for control {digest}')
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads((coverage_dir / 'coverage.json').read_text())
files = [file for data in coverage['data'] for file in data['files'] if file['summary']['lines']['covered'] > 0]
extension = [file for file in files if file['filename'].startswith('/work/source/pg-query-ext-0.48.0/ext/')]
libpg_query = [file for file in files if file['filename'].startswith('/work/source/libpg_query-18.0.0/')]
lines = lambda selected: sum(file['summary']['lines']['covered'] for file in selected)
by_suffix = lambda selected, suffix: lines(file for file in selected if file['filename'].endswith(suffix))
pg_query_c = by_suffix(extension, '/ext/pg_query.c')
gram_c = by_suffix(libpg_query, '/src/postgres/src_backend_parser_gram.c')
scan_c = by_suffix(libpg_query, '/src/postgres/src_backend_parser_scan.c')
if pg_query_c < 1 or gram_c < 1 or scan_c < 1:
    raise SystemExit('no ext/pg_query.c or libpg_query gram.c/scan.c lines covered')
relative = lambda file: file['filename'].removeprefix('/work/source/')
summary = {'control_pass': True, 'control_sha256': digest, 'output': observed,
           'parser_source_files': len(extension), 'parser_source_lines_covered': lines(extension),
           'format_specific_source_lines_covered': pg_query_c,
           'extension_lines_by_file': {relative(file): file['summary']['lines']['covered']
                                       for file in sorted(extension, key=lambda file: file['filename'])},
           'underlying_source_files': len(libpg_query), 'underlying_source_lines_covered': lines(libpg_query),
           'underlying_gram_c_lines_covered': gram_c, 'underlying_scan_c_lines_covered': scan_c,
           'underlying_lines_by_file': {relative(file): file['summary']['lines']['covered']
                                        for file in sorted(libpg_query, key=lambda file: file['filename'])},
           'coverage': '/coverage/coverage.json'}
# Only files with covered lines are kept, so run_project.py counts the same file set as this summary.
(coverage_dir / 'coverage.json').write_text(json.dumps({'data': [{'files': files}]}) + '\n')
(coverage_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
