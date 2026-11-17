"""Require executed RapidJSON reader and wrapper regions; export Parsarium source lines."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/rapidjson-source/'
rapidjson_prefix = prefix + 'rapidjson/include/rapidjson/'
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
for required in ('rapidjson.cpp', 'rapidjson/include/rapidjson/reader.h'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'{required} had no executed source regions')
for unused in ('writer.h', 'prettywriter.h', 'schema.h', 'document.h'):
    if any(item['filename'] == rapidjson_prefix + unused for item in files):
        raise SystemExit(f'{unused} executed during a load-only control')
underlying = [item for item in files if item['filename'].startswith(rapidjson_prefix)]
wrapper = [item for item in files if not item['filename'].startswith(rapidjson_prefix)]
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': sum(len(item['executed_lines']) for item in underlying),
           'wrapper_source_files': len(wrapper),
           'wrapper_source_lines_covered': sum(len(item['executed_lines']) for item in wrapper),
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
