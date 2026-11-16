"""Record OpenMesh PLYReader source coverage from valid-control replay."""
import json
from pathlib import Path

directory = Path('/coverage')
native = json.loads((directory / 'native.json').read_text())
files = [item for item in native['data'][0]['files']
         if item['filename'].startswith('/work/source/OpenMesh/src/OpenMesh/Core/IO/reader/')
         and item['summary']['lines']['covered'] > 0]
if not any(item['filename'].endswith('/PLYReader.cc') for item in files):
    raise SystemExit('OpenMesh native PLYReader.cc was not covered')
(directory / 'coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
observed = json.loads((directory / 'observed.json').read_text())
summary = {
    'control_pass': True,
    'output': observed,
    'parser_source_files': len(files),
    'parser_source_lines_covered': sum(item['summary']['lines']['covered'] for item in files),
    'coverage': '/coverage/coverage.json',
}
(directory / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
