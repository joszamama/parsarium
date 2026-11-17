"""Check the flow-php/postgresql summary and merge Xdebug package lines with LLVM extension and libpg_query lines.

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
xdebug = json.loads((coverage_dir / 'xdebug.json').read_text())
native = json.loads((coverage_dir / 'native.json').read_text())
native_files = [file for data in native['data'] for file in data['files'] if file['summary']['lines']['covered'] > 0]
extension = [file for file in native_files if file['filename'].startswith('/work/source/pg-query-ext-0.48.0/ext/')]
libpg_query = [file for file in native_files if file['filename'].startswith('/work/source/libpg_query-18.0.0/')]
lines = lambda selected: sum(file['summary']['lines']['covered'] for file in selected)
package, support = xdebug['package'], xdebug['support']
relative = lambda file, prefix: file['filename'].removeprefix(prefix)
parser_php = lines(file for file in package if file['filename'].endswith('/src/Flow/PostgreSql/Parser.php'))
gram_c = lines(file for file in libpg_query if file['filename'].endswith('/src/postgres/src_backend_parser_gram.c'))
pg_query_c = lines(file for file in extension if file['filename'].endswith('/ext/pg_query.c'))
if parser_php < 1 or gram_c < 1 or pg_query_c < 1:
    raise SystemExit('no Parser.php, ext/pg_query.c or libpg_query gram.c lines covered')
# Package files carry Xdebug executed lines; extension and libpg_query files keep their llvm-cov export records.
native_sources = [*extension, *libpg_query]
coverage = {'data': [{'files': [*package, *native_sources]}]}
(coverage_dir / 'coverage.json').write_text(json.dumps(coverage) + '\n')
summary = {'control_pass': True, 'control_sha256': digest, 'output': observed,
           'parser_source_files': len(package), 'parser_source_lines_covered': lines(package),
           'format_specific_source_lines_covered': parser_php,
           'package_lines_by_file': {relative(file, '/work/vendor/flow-php/postgresql/'): file['summary']['lines']['covered']
                                     for file in package},
           'support_source_files': len(support), 'support_source_lines_covered': lines(support),
           'xdebug_eof_pseudo_lines_removed': xdebug['xdebug_eof_pseudo_lines_removed'],
           'extension_source_lines_covered': lines(extension),
           'underlying_source_files': len(native_sources), 'underlying_source_lines_covered': lines(native_sources),
           'underlying_libpg_query_lines_covered': lines(libpg_query),
           'underlying_gram_c_lines_covered': gram_c,
           'coverage': '/coverage/coverage.json'}
(coverage_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
