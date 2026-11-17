"""Check the pecl/yaml typed tree and summarize LLVM line coverage of ext/yaml and libyaml.

target.json keys the expected tree by control SHA-256, so the same image checks both valid controls."""
from hashlib import sha256
import json
from pathlib import Path

coverage_dir = Path('/coverage')
observed = json.loads((coverage_dir / 'observed.json').read_text())
digest = sha256(Path('/input/control').read_bytes()).hexdigest()
expected = json.loads(Path('/work/target.json').read_text())['expected_output_by_control_sha256'].get(digest)
if expected is None:
    raise SystemExit(f'no expected output for control {digest}')
# Ordered comparison: map member order and scalar type tags must match the oracle tree.
if json.dumps(observed, ensure_ascii=False) != json.dumps(expected, ensure_ascii=False):
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads((coverage_dir / 'coverage.json').read_text())
files = {file['filename']: file for data in coverage['data'] for file in data['files']}.values()
extension = [file for file in files if file['filename'].startswith('/work/source/pecl-yaml-2.3.0/')]
libyaml = [file for file in files if file['filename'].startswith('/work/source/yaml-0.2.5/')]
lines = lambda selected: sum(file['summary']['lines']['covered'] for file in selected)
by_suffix = lambda selected, suffix: lines(file for file in selected if file['filename'].endswith(suffix))
parse_c = by_suffix(extension, '/pecl-yaml-2.3.0/parse.c')
parser_c = by_suffix(libyaml, '/yaml-0.2.5/src/parser.c')
scanner_c = by_suffix(libyaml, '/yaml-0.2.5/src/scanner.c')
if parse_c < 1 or parser_c < 1 or scanner_c < 1:
    raise SystemExit('no ext/yaml parse.c or libyaml parser.c/scanner.c lines covered')
summary = {'control_pass': True, 'control_sha256': digest, 'output': observed,
           'parser_source_files': len(extension), 'parser_source_lines_covered': lines(extension),
           'format_specific_source_lines_covered': parse_c,
           'extension_lines_by_file': {Path(file['filename']).name: file['summary']['lines']['covered']
                                       for file in sorted(extension, key=lambda file: file['filename'])},
           'underlying_source_files': len(libyaml), 'underlying_source_lines_covered': lines(libyaml),
           'underlying_parser_c_lines_covered': parser_c,
           'underlying_scanner_c_lines_covered': scanner_c,
           'underlying_lines_by_file': {Path(file['filename']).name: file['summary']['lines']['covered']
                                        for file in sorted(libyaml, key=lambda file: file['filename'])},
           'coverage': '/coverage/coverage.json'}
(coverage_dir / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
