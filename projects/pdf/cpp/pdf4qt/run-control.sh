#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
if ! ldd /work/replay | grep -q '/work/install/lib/libPdf4QtLibCore.so'; then
    echo 'replay is not loading the source-built PDF4QT core' >&2
    exit 1
fi
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -object=/work/install/lib/libPdf4QtLibCore.so \
  -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
if observed != {'pages': 1}: raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser = [f for f in files if f['filename'].startswith('/work/source/Pdf4QtLibCore/sources/')]
lines = lambda suffix: sum(f['summary']['lines']['covered'] for f in parser
                           if f['filename'].endswith(suffix))
if lines('/pdfdocumentreader.cpp') <= 0 or lines('/pdfparser.cpp') <= 0:
    raise SystemExit('PDF4QT native PDF reader/parser source was not covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser),
           'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in parser),
           'reader_source_lines_covered': lines('/pdfdocumentreader.cpp'),
           'syntax_source_lines_covered': lines('/pdfparser.cpp'),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
