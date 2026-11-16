"""Record covered lines of the pinned pytaglib C++ extension."""
import json
from pathlib import Path

directory = Path('/coverage')
native = json.loads((directory / 'native.json').read_text())
files = [item for item in native['data'][0]['files']
         if item['filename'].startswith('/work/source/')
         and item['summary']['lines']['covered'] > 0]
if not any(item['filename'].endswith('/src/taglib.cpp') for item in files):
    raise SystemExit('pytaglib C++ extension source was not covered')
coverage = {'data': [{'files': files}]}
(directory / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
summary = json.loads((directory / 'summary.json').read_text())
summary['parser_source_files'] = len(files)
summary['parser_source_lines_covered'] = sum(
    item['summary']['lines']['covered'] for item in files)
(directory / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
