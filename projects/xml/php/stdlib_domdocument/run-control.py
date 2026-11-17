"""Check PHP ext/dom plus libxml2 parser coverage and the namespace-aware XML result.

target.json keys the expected summary by control SHA-256, so the same image checks both valid controls."""
from hashlib import sha256
import json
from pathlib import Path

coverage_dir = Path('/coverage')
observed = json.loads((coverage_dir / 'observed.json').read_text())
digest = sha256(Path('/input/control').read_bytes()).hexdigest()
expected = json.loads(Path('/work/target.json').read_text())['expected_by_control_sha256'].get(digest)
if expected is None:
    raise SystemExit(f'no expected output for control {digest}')
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads((coverage_dir / 'coverage.json').read_text())
files = {file['filename']: file for data in coverage['data'] for file in data['files']}.values()
php = [file for file in files if file['filename'].startswith('/work/source/php-8.5.12/ext/')]
libxml2 = [file for file in files if file['filename'].startswith('/work/source/libxml2-2.15.4/')]
lines = lambda selected: sum(file['summary']['lines']['covered'] for file in selected)
specific = lines(file for file in php if file['filename'].endswith('/dom/document.c'))
parser = lines(file for file in libxml2 if file['filename'].endswith('/libxml2-2.15.4/parser.c'))
sax2 = lines(file for file in libxml2 if file['filename'].endswith('/libxml2-2.15.4/SAX2.c'))
if not php or specific < 1 or parser < 1 or sax2 < 1:
    raise SystemExit('no PHP ext/dom document.c or libxml2 parser.c/SAX2.c lines covered')
summary = {'control_pass': True, 'control_sha256': digest, 'output': observed,
           'parser_source_files': len(php), 'parser_source_lines_covered': lines(php),
           'format_specific_source_lines_covered': specific,
           'underlying_source_files': len(libxml2), 'underlying_source_lines_covered': lines(libxml2),
           'underlying_parser_c_lines_covered': parser,
           'underlying_sax2_c_lines_covered': sax2,
           'coverage': '/coverage/coverage.json'}
(coverage_dir / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
