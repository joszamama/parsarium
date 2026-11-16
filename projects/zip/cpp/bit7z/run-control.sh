#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
# The replay binary and the DT_NEEDED SevenZip 7z.so each carry their own
# profile runtime; %m gives each module its own raw profile.
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/lib-cov/7z.so \
  -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'entries': 1, 'name': 'hello.txt', 'content': 'parsarium\n'}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines = lambda group: sum(f['summary']['lines']['covered'] for f in group)
named = lambda group, suffix: [f for f in group if f['filename'].endswith(suffix)]
# bit7z is the wrapper API; SevenZip is the ZIP reader and Deflate decoder it
# loads. The harness itself is outside both prefixes.
parser = [f for f in files if f['filename'].startswith('/work/bit7z/')]
underlying = [f for f in files if f['filename'].startswith('/work/sevenzip/')]
gates = {
    'bit7z reader': named(parser, '/src/bitarchivereader.cpp'),
    'bit7z input archive': named(parser, '/src/bitinputarchive.cpp'),
    'bit7z library loader': named(parser, '/src/bit7zlibrary.cpp'),
    'bit7z buffer extract callback': named(parser, '/src/internal/bufferextractcallback.cpp'),
    'bit7z buffer out stream': named(parser, '/src/internal/cbufferoutstream.cpp'),
    'SevenZip ZIP reader': named(underlying, '/CPP/7zip/Archive/Zip/ZipIn.cpp'),
    'SevenZip ZIP handler': named(underlying, '/CPP/7zip/Archive/Zip/ZipHandler.cpp'),
    'SevenZip ZIP item': named(underlying, '/CPP/7zip/Archive/Zip/ZipItem.cpp'),
    'SevenZip Deflate decoder': named(underlying, '/CPP/7zip/Compress/DeflateDecoder.cpp'),
    'SevenZip archive exports': named(underlying, '/CPP/7zip/Archive/ArchiveExports.cpp'),
}
missing = [name for name, group in gates.items() if lines(group) <= 0]
if missing:
    raise SystemExit(f'no instrumented source lines covered: {missing}')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser), 'parser_source_lines_covered': lines(parser),
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': lines(underlying),
           'underlying_zip_reader_source_lines_covered': lines(gates['SevenZip ZIP reader']),
           'underlying_zip_handler_source_lines_covered': lines(gates['SevenZip ZIP handler']),
           'underlying_deflate_source_lines_covered': lines(gates['SevenZip Deflate decoder']),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
