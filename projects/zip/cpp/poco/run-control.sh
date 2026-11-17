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
parser = [f for f in files if f['filename'].startswith('/work/source/Zip/src/')]
archive = [f for f in parser if f['filename'].endswith('/ZipArchive.cpp')]
header = [f for f in parser if f['filename'].endswith('/ZipLocalFileHeader.cpp')]
stream = [f for f in parser if f['filename'].endswith('/ZipStream.cpp')]
zlib = [f for f in files if f['filename'].startswith('/work/source/dependencies/zlib/src/')]
inflate = [f for f in zlib if f['filename'].endswith('/inflate.c')]
if not parser or min(lines(parser), lines(archive), lines(header), lines(stream)) <= 0:
    raise SystemExit('no instrumented Poco Zip reader source lines covered')
if not zlib or lines(inflate) <= 0:
    raise SystemExit('no instrumented bundled zlib inflate source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser), 'parser_source_lines_covered': lines(parser),
           'format_specific_source_lines_covered': lines(archive),
           'local_header_source_lines_covered': lines(header),
           'stream_source_lines_covered': lines(stream),
           'underlying_source_files': len(zlib),
           'underlying_source_lines_covered': lines(zlib),
           'underlying_format_specific_source_lines_covered': lines(inflate),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
