#!/bin/sh
set -eu
test -f /input/control
test -f "$PPS_BACKENDS_DIR/libpdfdocument.so"
test -f "$PPS_BACKENDS_DIR/org.gnome.Papers.PdfDocument.papers-backend"
mkdir -p /coverage
if ! ldd "$PPS_BACKENDS_DIR/libpdfdocument.so" | grep -q '/work/install/lib/libpoppler-glib.so'; then
    echo 'Papers PDF backend is not loading source-built Poppler GLib' >&2
    exit 1
fi
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay \
  -object=/work/install/lib/libppsdocument-4.0.so \
  -object="$PPS_BACKENDS_DIR/libpdfdocument.so" \
  -object=/work/install/lib/libpoppler-glib.so \
  -object=/work/install/lib/libpoppler.so \
  -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
python3 - <<'PY'
import json
from pathlib import Path
observed = json.loads(Path('/coverage/observed.json').read_text())
if observed != {'pages': 2}:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines = lambda group: sum(f['summary']['lines']['covered'] for f in group)
backend = [f for f in files if f['filename'].startswith('/work/papers-source/libdocument/backend/pdf/')]
factory = [f for f in files if f['filename'].endswith('/libdocument/pps-document-factory.c')]
glib = [f for f in files if f['filename'].startswith('/work/poppler-source/glib/')]
core = [f for f in files if f['filename'].startswith('/work/poppler-source/poppler/')]
for group, suffix in ((backend, '/pps-poppler.c'), (factory, '/pps-document-factory.c'),
                      (glib, '/poppler-document.cc'), (core, '/Parser.cc'),
                      (core, '/Lexer.cc'), (core, '/XRef.cc'), (core, '/PDFDoc.cc')):
    if not lines([f for f in group if f['filename'].endswith(suffix)]):
        raise SystemExit(f'no parser source coverage in {suffix}')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(backend),
           'parser_source_lines_covered': lines(backend),
           'format_specific_source_lines_covered': lines(backend),
           'factory_source_lines_covered': lines(factory),
           'poppler_glib_source_lines_covered': lines(glib),
           'underlying_source_files': len(core),
           'underlying_source_lines_covered': lines(core),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
