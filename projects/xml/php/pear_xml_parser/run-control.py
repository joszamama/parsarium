"""Check the pear/xml_parser summary and merge Xdebug package lines with LLVM ext/xml and libxml2 lines.

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
crosscheck = json.loads((coverage_dir / 'crosscheck.json').read_text())
if crosscheck != {'file': observed, 'stream': observed}:
    raise SystemExit(f'setInputFile/setInput summary differs from setInputString: {crosscheck}')
xdebug = json.loads((coverage_dir / 'xdebug.json').read_text())
native = json.loads((coverage_dir / 'native.json').read_text())
native_files = {file['filename']: file for data in native['data'] for file in data['files']}.values()
php_ext = [file for file in native_files if file['filename'].startswith('/work/source/php-8.5.12/ext/xml/')]
libxml2 = [file for file in native_files if file['filename'].startswith('/work/source/libxml2-2.15.4/')]
lines = lambda selected: sum(file['summary']['lines']['covered'] for file in selected)
package, support = xdebug['package'], xdebug['support']
specific = lines(file for file in package if file['filename'].endswith('/XML/Parser.php'))
parser = lines(file for file in libxml2 if file['filename'].endswith('/libxml2-2.15.4/parser.c'))
compat = lines(file for file in php_ext if file['filename'].endswith('/ext/xml/compat.c'))
if specific < 1 or parser < 1 or compat < 1:
    raise SystemExit('no XML_Parser, ext/xml compat.c or libxml2 parser.c lines covered')
# Package files carry Xdebug executed lines; ext/xml and libxml2 files keep their llvm-cov export records.
coverage = {'data': [{'files': [*package, *php_ext, *libxml2]}]}
(coverage_dir / 'coverage.json').write_text(json.dumps(coverage) + '\n')
summary = {'control_pass': True, 'control_sha256': digest, 'output': observed,
           'file_and_stream_api_match': True,
           'parser_source_files': len(package), 'parser_source_lines_covered': lines(package),
           'format_specific_source_lines_covered': specific,
           'support_source_lines_covered': lines(support),
           'xdebug_eof_pseudo_lines_removed': xdebug['xdebug_eof_pseudo_lines_removed'],
           'php_deprecations': xdebug['php_deprecations'],
           'extension_source_files': len(php_ext), 'extension_source_lines_covered': lines(php_ext),
           'compat_source_lines_covered': compat,
           'underlying_source_files': len(libxml2), 'underlying_source_lines_covered': lines(libxml2),
           'underlying_parser_c_lines_covered': parser,
           'coverage': '/coverage/coverage.json'}
(coverage_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
