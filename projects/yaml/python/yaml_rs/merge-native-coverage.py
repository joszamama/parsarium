"""Require executed granit-parser scanner/parser regions in the _yaml_rs extension and export Parsarium source lines.

granit-parser (git revision e10ee63, saphyr-parser lineage) is the parser; yaml-rs's own Rust
loader (src/load/: event-to-value building, alias handling, scalar resolution) is reported as
package lines; pyo3, lexical-core and the lava-sh saphyr fork are not counted."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/usr/local/cargo/git/checkouts/granit-parser-adcc536166983974/e10ee63/src/'
package = '/work/yaml-rs-source/src/'
files, own = [], []
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if not lines or not filename.startswith((prefix, package)):
        continue
    record = {'filename': filename, 'summary': {'lines': {'covered': len(lines)}}, 'executed_lines': lines}
    (files if filename.startswith(prefix) else own).append(record)
for required in ('scanner.rs', 'parser.rs'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'granit-parser {required} had no executed source regions')
for required in ('load/loads.rs', 'load/scalar.rs'):
    if not any(item['filename'] == package + required for item in own):
        raise SystemExit(f'yaml-rs {required} had no executed source regions')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files + own}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'package_source_files': len(own),
           'package_source_lines_covered': sum(len(item['executed_lines']) for item in own),
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
