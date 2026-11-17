"""Require executed unsafe-libyaml scanner/parser regions in the _ryaml extension and export Parsarium source lines.

unsafe-libyaml 0.2.11 is the parser; serde_yaml 0.9.34 (event loader, alias expansion, scalar
resolution) is reported as underlying source; the ryaml PyO3 module is reported as wrapper lines."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
registry = '/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/'
prefix = registry + 'unsafe-libyaml-0.2.11/src/'
loader = registry + 'serde_yaml-0.9.34+deprecated/src/'
wrapper = '/work/ryaml-source/src/lib.rs'
files, underlying = [], []
wrapper_lines = 0
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if filename == wrapper:
        wrapper_lines = len(lines)
    if not lines or not filename.startswith((prefix, loader)):
        continue
    record = {'filename': filename, 'summary': {'lines': {'covered': len(lines)}}, 'executed_lines': lines}
    (files if filename.startswith(prefix) else underlying).append(record)
for required in ('scanner.rs', 'parser.rs', 'reader.rs'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'unsafe-libyaml {required} had no executed source regions')
if not any(item['filename'] == loader + 'de.rs' for item in underlying):
    raise SystemExit('serde_yaml de.rs had no executed source regions')
if not wrapper_lines:
    raise SystemExit('ryaml loads wrapper was not executed')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files + underlying}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': sum(len(item['executed_lines']) for item in underlying),
           'wrapper_source_lines_covered': wrapper_lines,
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
