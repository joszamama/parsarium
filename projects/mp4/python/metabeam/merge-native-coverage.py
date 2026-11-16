"""Record executed MP4 box-parser source lines from metabeam."""
import json
from pathlib import Path

root = Path('/coverage')
native = json.loads((root / 'native.json').read_text())
files = [item for item in native['data'][0]['files']
         if item['filename'].startswith('/work/source/')
         and item['summary']['lines']['covered'] > 0]
if not any(item['filename'].endswith('/core/src/extractors/media.rs') for item in files):
    raise SystemExit('metabeam MP4 parser source was not covered')
(root / 'coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
summary = json.loads((root / 'summary.json').read_text())
summary['parser_source_files'] = len(files)
summary['parser_source_lines_covered'] = sum(item['summary']['lines']['covered'] for item in files)
(root / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
