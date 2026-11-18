"""Require executed polyglot-sql parser regions and the pyo3 binding; export Parsarium source lines."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/polyglot-source/crates/polyglot-sql/src/'
binding_prefix = '/work/polyglot-source/crates/polyglot-sql-python/src/'


def executed(item) -> list[int]:
    return sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                   if has_count and region_entry and count > 0})


files = []
binding_lines = 0
for item in raw['data'][0]['files']:
    filename = item['filename']
    if filename.startswith(binding_prefix):
        binding_lines += len(executed(item))
    if not filename.startswith(prefix):
        continue
    lines = executed(item)
    if lines:
        files.append({'filename': filename, 'summary': {'lines': {'covered': len(lines)}},
                      'executed_lines': lines})
for required in ('parser.rs', 'tokens.rs'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'{required} had no executed source regions')
if not binding_lines:
    raise SystemExit('polyglot-sql-python binding had no executed source regions')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'binding_source_lines_covered': binding_lines,
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
