"""Check native PHP parser coverage and the valid PNG result."""
import json
from pathlib import Path

coverage_dir = Path('/coverage')
observed = json.loads((coverage_dir / 'observed.json').read_text())
expected = json.loads(Path('/work/target.json').read_text())['expected_output']
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads((coverage_dir / 'coverage.json').read_text())
files = [file for data in coverage['data'] for file in data['files']
         if file['filename'].startswith('/work/source/php-8.5.12/sapi/cli/')]
covered = sum(file['summary']['lines']['covered'] for file in files)
specific = sum(file['summary']['lines']['covered'] for file in files
               if file['filename'].endswith('/php_http_parser.c'))
if not files or covered < 1 or specific < 1:
    raise SystemExit('no native php_http_parser.c parser lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
(coverage_dir / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
