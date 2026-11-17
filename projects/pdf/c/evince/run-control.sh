#!/bin/sh
set -eu
test -f /input/control
test -f "$EV_BACKENDS_DIR/libpdfdocument.so"
test -f "$EV_BACKENDS_DIR/pdfdocument.evince-backend"
mkdir -p /coverage
if ! ldd "$EV_BACKENDS_DIR/libpdfdocument.so" | grep -q '/work/install/lib/libpoppler-glib.so'; then
    echo 'Evince PDF backend is not loading source-built Poppler GLib' >&2
    exit 1
fi
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-cov export /work/replay \
  -object=/work/install/lib/libevdocument3.so \
  -object="$EV_BACKENDS_DIR/libpdfdocument.so" \
  -object=/work/install/lib/libpoppler-glib.so \
  -object=/work/install/lib/libpoppler.so \
  -instr-profile=/coverage/control.profdata > /coverage/coverage.json
LLVM_PROFILE_FILE=/coverage/fd-%m.profraw /work/fuzzer -runs=1 /input/control \
  > /coverage/fd.stdout 2> /coverage/fd.stderr
llvm-profdata merge -sparse /coverage/fd-*.profraw -o /coverage/fd.profdata
llvm-cov export /work/fuzzer \
  -object=/work/install/lib/libevdocument3.so \
  -object="$EV_BACKENDS_DIR/libpdfdocument.so" \
  -object=/work/install/lib/libpoppler-glib.so \
  -object=/work/install/lib/libpoppler.so \
  -instr-profile=/coverage/fd.profdata > /coverage/fd-coverage.json
python3 - <<'PY'
import json
from pathlib import Path

observed = json.loads(Path('/coverage/observed.json').read_text())
if observed != {'pages': 2}:
    raise SystemExit(f'control mismatch: {observed}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines = lambda group: sum(f['summary']['lines']['covered'] for f in group)
evince = [f for f in files if f['filename'].startswith('/work/evince-source/backend/pdf/')]
factory = [f for f in files if f['filename'].endswith('/libdocument/ev-document-factory.c')]
glib = [f for f in files if f['filename'].startswith('/work/source/glib/')]
core = [f for f in files if f['filename'].startswith('/work/source/poppler/')]
for group, suffix in ((evince, '/ev-poppler.c'), (factory, '/ev-document-factory.c'),
                      (glib, '/poppler-document.cc'), (core, '/Parser.cc'),
                      (core, '/Lexer.cc'), (core, '/XRef.cc'), (core, '/PDFDoc.cc')):
    if not lines([f for f in group if f['filename'].endswith(suffix)]):
        raise SystemExit(f'no parser source coverage in {suffix}')
gfile_backend = [f for f in evince if f['filename'].endswith('/ev-poppler.c')]
if len(gfile_backend) != 1 or not any(299 <= seg[0] <= 315 and seg[2] > 0 and seg[3]
                                      for seg in gfile_backend[0]['segments']):
    raise SystemExit('Evince PDF load_gfile source path was not covered')
fd_files = json.loads(Path('/coverage/fd-coverage.json').read_text())['data'][0]['files']
fd_backend = [f for f in fd_files if f['filename'].endswith('/backend/pdf/ev-poppler.c')]
fd_core = [f for f in fd_files if f['filename'].startswith('/work/source/poppler/')]
fd_glib = [f for f in fd_files if f['filename'].endswith('/glib/poppler-document.cc')]
if len(fd_backend) != 1 or not any(324 <= seg[0] <= 339 and seg[2] > 0 and seg[3]
                                   for seg in fd_backend[0]['segments']):
    raise SystemExit('Evince PDF load_fd source path was not covered')
for group, suffix in ((fd_backend, '/ev-poppler.c'), (fd_glib, '/poppler-document.cc'),
                      (fd_core, '/Parser.cc'), (fd_core, '/Lexer.cc'),
                      (fd_core, '/XRef.cc'), (fd_core, '/PDFDoc.cc')):
    if not lines([f for f in group if f['filename'].endswith(suffix)]):
        raise SystemExit(f'no file-descriptor parser source coverage in {suffix}')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(evince),
           'parser_source_lines_covered': lines(evince),
           'format_specific_source_lines_covered': lines(evince),
           'factory_source_lines_covered': lines(factory),
           'poppler_glib_source_lines_covered': lines(glib),
           'underlying_source_files': len(core),
           'underlying_source_lines_covered': lines(core),
           'fd_backend_source_lines_covered': lines(fd_backend),
           'fd_poppler_glib_document_lines_covered': lines(fd_glib),
           'fd_underlying_source_lines_covered': lines(fd_core),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
