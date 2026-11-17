"""Require executed toml_parser lexer/parser regions in the _rtoml extension and export Parsarium source lines.

toml_parser 1.1.5 is the parser (lexer, event parser, scalar and string decoding);
the toml 1.1.8 crate that assembles its DeTable/DeValue from those events is
reported as underlying source and toml_datetime 1.1.2 as a separate line count; rtoml's own PyO3 glue
(src/*.rs) is reported only as wrapper lines.
"""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
registry = '/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/'
prefix = registry + 'toml_parser-1.1.5+spec-1.1.0/src/'
underlying_prefix = registry + 'toml-1.1.8+spec-1.1.0/src/'
datetime_prefix = registry + 'toml_datetime-1.1.2+spec-1.1.0/src/'
wrapper = '/work/rtoml-source/src/'
files, underlying = [], []
wrapper_lines = 0
datetime_lines = 0
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if not lines:
        continue
    if filename.startswith(wrapper):
        wrapper_lines += len(lines)
        continue
    if filename.startswith(datetime_prefix):
        datetime_lines += len(lines)
        continue
    record = {'filename': filename, 'summary': {'lines': {'covered': len(lines)}}, 'executed_lines': lines}
    if filename.startswith(prefix):
        files.append(record)
    elif filename.startswith(underlying_prefix):
        underlying.append(record)
for required in ('lexer/mod.rs', 'parser/document.rs', 'decoder/string.rs'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'toml_parser {required} had no executed source regions')
if not any(item['filename'].startswith(underlying_prefix + 'de/') for item in underlying):
    raise SystemExit('toml de module had no executed source regions')
if not wrapper_lines:
    raise SystemExit('rtoml deserialize wrapper was not executed')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files + underlying}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': sum(len(item['executed_lines']) for item in underlying),
           'wrapper_source_lines_covered': wrapper_lines,
           'toml_datetime_source_lines_covered': datetime_lines,
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
