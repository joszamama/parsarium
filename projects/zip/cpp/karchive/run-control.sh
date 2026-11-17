#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
expected = {'entries': 1, 'name': 'hello.txt', 'content': 'parsarium\n'}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines = lambda group: sum(f['summary']['lines']['covered'] for f in group)
named = lambda group, name: [f for f in group if f['filename'].endswith('/' + name)]
# Only KArchive is instrumented; Qt6Core and zlib are uninstrumented system
# libraries and do not appear in this report.
parser = [f for f in files if f['filename'].startswith('/work/source/src/')]
kzip = named(parser, 'kzip.cpp')
archive = named(parser, 'karchive.cpp')
device = named(parser, 'kcompressiondevice.cpp')
gzip = named(parser, 'kgzipfilter.cpp')
limited = named(parser, 'klimitediodevice.cpp')
if not parser or min(lines(kzip), lines(archive), lines(device), lines(gzip), lines(limited)) <= 0:
    raise SystemExit('no instrumented KArchive KZip reader source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser), 'parser_source_lines_covered': lines(parser),
           'format_specific_source_lines_covered': lines(kzip),
           'archive_source_lines_covered': lines(archive),
           'compression_device_source_lines_covered': lines(device),
           'deflate_filter_source_lines_covered': lines(gzip),
           'limited_device_source_lines_covered': lines(limited),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
