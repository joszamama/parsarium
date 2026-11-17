#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE='/coverage/control-%m.profraw' /work/replay /input/control > /coverage/observed.json
LLVM_PROFILE_FILE='/coverage/second-%m.profraw' /work/replay /work/two-page.pdf > /coverage/second-observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-profdata merge -sparse /coverage/second-*.profraw -o /coverage/second.profdata
rm -f /coverage/second-*.profraw
llvm-profdata show --all-functions --counts /coverage/control.profdata > /coverage/control-functions.txt
llvm-profdata show --all-functions --counts /coverage/second.profdata > /coverage/second-functions.txt
llvm-cov export /work/replay -object /work/libpdf_oxide.so \
  -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY'
import json
import re
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
if observed != {'pages': 1}:
    raise SystemExit(f'control mismatch: {observed}')
second = json.loads(Path('/coverage/second-observed.json').read_text())
if second != {'pages': 2}:
    raise SystemExit(f'second control mismatch: {second}')


def executed(path: str) -> set[str]:
    # Sparse profiles keep only functions with non-zero counters.
    names, current = set(), None
    for line in Path(path).read_text().splitlines():
        if re.match(r'^  \S.*:$', line):
            current = line.strip()[:-1]
        match = re.match(r'^\s+Function count: (\d+)$', line)
        if current and match and int(match.group(1)) > 0:
            names.add(current)
    return names


xref_paths = {}
for label in ('control', 'second'):
    names = executed(f'/coverage/{label}-functions.txt')
    regular = any('try_open_regular' in name for name in names)
    rebuilt = any('try_reconstruct_xref' in name for name in names)
    if not regular or rebuilt:
        raise SystemExit(f'{label}: regular xref path not taken '
                         f'(try_open_regular={regular}, try_reconstruct_xref={rebuilt})')
    xref_paths[label] = 'regular'

files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [file for file in files if file['filename'].startswith('/work/source/src/')]
covered = sum(file['summary']['lines']['covered'] for file in parser)
syntax = {}
for name in ('lexer.rs', 'parser.rs', 'object.rs', 'objstm.rs', 'xref.rs', 'xref_reconstruction.rs'):
    matching = [file for file in parser if file['filename'] == f'/work/source/src/{name}']
    syntax[name] = sum(file['summary']['lines']['covered'] for file in matching)
if not covered or not all(syntax[name] for name in ('lexer.rs', 'parser.rs', 'xref.rs')):
    raise SystemExit(f'pdf_oxide syntax decoder coverage missing: {covered} total, {syntax}')
summary = {'control_pass': True, 'output': observed,
           'second_control_output': second,
           'xref_path': xref_paths,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': covered,
           'format_specific_source_lines_covered': syntax['parser.rs'],
           'syntax_decoder_lines_covered': syntax,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
