"""Require executed libfyaml scanner/parser regions in the _libfyaml extension; export Parsarium source lines.

Counted scope: the bundled libfyaml 1.0.0-rc2 core under src/lib/ (input, scanner/parser in
fy-parse.c, tokens, atoms, composer). The generic value builder under src/generic/ is reported as
underlying source; allocators, hashing and the binding's own _libfyaml.c are not counted."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/libfyaml-src/src/lib/'
generic = '/work/libfyaml-src/src/generic/'
files, underlying = [], []
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if not lines or not filename.startswith((prefix, generic)):
        continue
    record = {'filename': filename, 'summary': {'lines': {'covered': len(lines)}}, 'executed_lines': lines}
    (files if filename.startswith(prefix) else underlying).append(record)
for required in ('fy-parse.c', 'fy-input.c'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'{required} had no executed source regions')
if not underlying:
    raise SystemExit('libfyaml generic value builder had no executed source regions')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files + underlying}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': sum(len(item['executed_lines']) for item in underlying),
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
