"""Require executed toml11 parser regions in the pytoml11 _value extension and export Parsarium source lines.

The vendored single-header toml11 4.2.0 (src/toml.hpp) is the parser; pytoml11's own
pybind11 source (src/pytoml11.cpp) is reported only as wrapper lines, and pybind11,
libstdc++ and system headers are left out.
"""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
parser_file = '/work/pytoml11-source/src/toml.hpp'
wrapper_file = '/work/pytoml11-source/src/pytoml11.cpp'
files = []
wrapper_lines = 0
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if not lines:
        continue
    if filename == wrapper_file:
        wrapper_lines += len(lines)
    elif filename == parser_file:
        files.append({'filename': filename, 'summary': {'lines': {'covered': len(lines)}},
                      'executed_lines': lines})
if not files:
    raise SystemExit('toml11 src/toml.hpp had no executed source regions')
if not wrapper_lines:
    raise SystemExit('pytoml11 loads wrapper was not executed')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'wrapper_source_lines_covered': wrapper_lines,
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
