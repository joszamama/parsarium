"""Require executed ujson decoder and double-conversion regions; export Parsarium source lines."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/ujson-source/src/ujson/'
dconv_prefix = prefix + 'deps/double-conversion/'
files = []
for item in raw['data'][0]['files']:
    filename = item['filename']
    if not filename.startswith(prefix):
        continue
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if lines:
        files.append({'filename': filename, 'summary': {'lines': {'covered': len(lines)}},
                      'executed_lines': lines})
for required in ('decode.c', 'dconv_wrapper.cc',
                 'deps/double-conversion/double-conversion/string-to-double.cc'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'{required} had no executed source regions')
if any(item['filename'] == prefix + 'encode.c' for item in files):
    raise SystemExit('encode.c executed during a loads-only control')
dconv = [item for item in files if item['filename'].startswith(dconv_prefix)]
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'underlying_source_files': len(dconv),
           'underlying_source_lines_covered': sum(len(item['executed_lines']) for item in dconv),
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
