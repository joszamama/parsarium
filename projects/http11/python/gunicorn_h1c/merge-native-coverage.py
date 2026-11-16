"""Add coverage of the pinned native HTTP parser to the Python receipt."""
import json
from pathlib import Path

directory = Path('/coverage')
native = json.loads((directory / 'native.json').read_text())
coverage = json.loads((directory / 'coverage.json').read_text())
files = [item for item in native['data'][0]['files']
         if item['filename'].startswith('/work/source/src/gunicorn_h1c/')
         and item['summary']['lines']['covered'] > 0]
if not any(item['filename'].endswith('/picohttpparser.c') for item in files):
    raise SystemExit('native picohttpparser source was not covered')
coverage['data'][0]['files'].extend(files)
(directory / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
summary = json.loads((directory / 'summary.json').read_text())
summary['underlying_source_files'] = len(files)
summary['underlying_source_lines_covered'] = sum(
    item['summary']['lines']['covered'] for item in files)
(directory / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
