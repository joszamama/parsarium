"""Require executed msgspec JSON decoder regions in _core.c; export Parsarium source lines."""
import json
from pathlib import Path

root = Path('/coverage')
raw = json.loads((root / 'native.json').read_text())
prefix = '/work/msgspec-source/src/msgspec/'
core = prefix + '_core.c'
# _core.c section banners at the pinned SHA-256: "JSON Decoder" up to "to_builtins",
# and the shared "Number Parser" that json_maybe_decode_number calls.
json_decoder = range(17076, 20141)
number_parser = range(12242, 12692)
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
core_lines, = [item['executed_lines'] for item in files if item['filename'] == core]
decoder_lines = [line for line in core_lines if line in json_decoder]
number_lines = [line for line in core_lines if line in number_parser]
if not decoder_lines or not number_lines:
    raise SystemExit('msgspec JSON decoder or number parser had no executed source regions')
observed = json.loads((root / 'observed.json').read_text())
coverage = {'data': [{'files': files}]}
summary = {'control_pass': True, 'output': observed, 'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(item['executed_lines']) for item in files),
           'json_decoder_section_lines_covered': len(decoder_lines),
           'number_parser_section_lines_covered': len(number_lines),
           'coverage': '/coverage/coverage.json'}
(root / 'coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
(root / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
