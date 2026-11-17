"""Require executed toml++ parser regions in the pytomlpp _impl extension and export Parsarium source lines.

The vendored toml++ headers (third_party/tomlplusplus/include/toml++/) are the parser;
pytomlpp's own pybind11 sources (src/*.cpp, include/pytomlpp/) are reported only as
wrapper lines, and pybind11 and system headers are left out.
"""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/pytomlpp-source/third_party/tomlplusplus/include/toml++/'
wrappers = ('/work/pytomlpp-source/src/', '/work/pytomlpp-source/include/pytomlpp/')
files = []
wrapper_lines = 0
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if not lines:
        continue
    if filename.startswith(wrappers):
        wrapper_lines += len(lines)
    elif filename.startswith(prefix):
        files.append({'filename': filename, 'summary': {'lines': {'covered': len(lines)}},
                      'executed_lines': lines})
for required in ('impl/parser.inl', 'impl/table.inl'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'toml++ {required} had no executed source regions')
for unused in ('impl/toml_formatter.inl', 'impl/json_formatter.inl', 'impl/yaml_formatter.inl'):
    if any(item['filename'] == prefix + unused for item in files):
        raise SystemExit(f'{unused} executed during pytomlpp.loads')
if not wrapper_lines:
    raise SystemExit('pytomlpp loads wrapper was not executed')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'wrapper_source_lines_covered': wrapper_lines,
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
