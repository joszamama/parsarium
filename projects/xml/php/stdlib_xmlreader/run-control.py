"""Check PHP ext/xmlreader plus libxml2 parser coverage and the namespace-aware XML result."""
import json
from pathlib import Path

coverage_dir = Path('/coverage')
observed = json.loads((coverage_dir / 'observed.json').read_text())
expected = json.loads(Path('/work/target.json').read_text())['expected_output']
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads((coverage_dir / 'coverage.json').read_text())
files = {file['filename']: file for data in coverage['data'] for file in data['files']}.values()
php = [file for file in files if file['filename'].startswith('/work/source/php-8.5.12/ext/')]
libxml2 = [file for file in files if file['filename'].startswith('/work/source/libxml2-2.15.4/')]
lines = lambda selected: sum(file['summary']['lines']['covered'] for file in selected)
specific = lines(file for file in php if file['filename'].endswith('/xmlreader/php_xmlreader.c'))
parser = lines(file for file in libxml2 if file['filename'].endswith('/libxml2-2.15.4/parser.c'))
if not php or specific < 1 or parser < 1:
    raise SystemExit('no PHP XMLReader or libxml2 parser lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(php), 'parser_source_lines_covered': lines(php),
           'format_specific_source_lines_covered': specific,
           'underlying_source_files': len(libxml2), 'underlying_source_lines_covered': lines(libxml2),
           'underlying_parser_c_lines_covered': parser,
           'coverage': '/coverage/coverage.json'}
(coverage_dir / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
