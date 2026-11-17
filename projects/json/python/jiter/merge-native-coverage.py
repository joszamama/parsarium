"""Require executed Jiter Rust parser regions and export Parsarium source lines.

lexical-parse-float is Jiter's float-number dependency and is reported as underlying source."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/jiter-source/crates/jiter/src/'
lexical = '/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/lexical-parse-float-1.0.6/src/'
wrapper = '/work/jiter-source/crates/jiter-python/src/lib.rs'
files = []
underlying = []
wrapper_lines = 0
for item in raw['data'][0]['files']:
    filename = item['filename']
    lines = sorted({line for line, column, count, has_count, region_entry, *_ in item['segments']
                    if has_count and region_entry and count > 0})
    if filename == wrapper:
        wrapper_lines = len(lines)
    if not lines or not filename.startswith((prefix, lexical)):
        continue
    record = {'filename': filename, 'summary': {'lines': {'covered': len(lines)}}, 'executed_lines': lines}
    (files if filename.startswith(prefix) else underlying).append(record)
for required in ('parse.rs', 'python.rs', 'string_decoder.rs', 'number_decoder.rs'):
    if not any(item['filename'] == prefix + required for item in files):
        raise SystemExit(f'Jiter {required} had no executed source regions')
if not any(item['filename'] == lexical + 'parse.rs' for item in underlying):
    raise SystemExit('lexical-parse-float parse.rs had no executed source regions')
if not wrapper_lines:
    raise SystemExit('jiter-python from_json wrapper was not executed')
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
