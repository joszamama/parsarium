#!/bin/sh
set -eu
test -f /input/control
test -f "$EV_BACKENDS_DIR/libpdfdocument.so"
test -f "$EV_BACKENDS_DIR/pdfdocument.atril-backend"
mkdir -p /coverage
if ! ldd "$EV_BACKENDS_DIR/libpdfdocument.so" | grep -q '/work/install/lib/libpoppler-glib.so'; then
    echo 'Atril PDF backend is not loading source-built Poppler GLib' >&2
    exit 1
fi
# Valid control, then the second valid PDF baked into the image for the differential.
LLVM_PROFILE_FILE=/coverage/control-%m.profraw /work/replay /input/control > /coverage/observed.json
LLVM_PROFILE_FILE=/coverage/variant-%m.profraw /work/replay /work/valid-one-page.pdf > /coverage/variant-observed.json
llvm-profdata merge -sparse /coverage/control-*.profraw -o /coverage/control.profdata
llvm-profdata merge -sparse /coverage/variant-*.profraw -o /coverage/variant.profdata
objects="-object=/work/install/lib/libatrildocument.so -object=$EV_BACKENDS_DIR/libpdfdocument.so \
  -object=/work/install/lib/libpoppler-glib.so -object=/work/install/lib/libpoppler.so"
llvm-cov export /work/replay $objects -instr-profile=/coverage/control.profdata --summary-only > /coverage/coverage.json
llvm-cov export /work/replay $objects -instr-profile=/coverage/control.profdata > /coverage/control-segments.json
llvm-cov export /work/replay $objects -instr-profile=/coverage/variant.profdata > /coverage/variant-segments.json
python3 - <<'PY'
import json
from pathlib import Path

ATRIL_PDF = '/work/atril-source/backend/pdf/'
FACTORY = '/work/atril-source/libdocument/ev-document-factory.c'
GLIB = '/work/source/glib/'
CORE = '/work/source/poppler/'

observed = json.loads(Path('/coverage/observed.json').read_text())
if observed != {'pages': 2}:
    raise SystemExit(f'control mismatch: {observed}')
variant = json.loads(Path('/coverage/variant-observed.json').read_text())
if variant != {'pages': 1}:
    raise SystemExit(f'valid variant mismatch: {variant}')
files = json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
lines = lambda group: sum(f['summary']['lines']['covered'] for f in group)
atril = [f for f in files if f['filename'].startswith(ATRIL_PDF)]
factory = [f for f in files if f['filename'] == FACTORY]
glib = [f for f in files if f['filename'].startswith(GLIB)]
core = [f for f in files if f['filename'].startswith(CORE)]
for group, suffix in ((atril, '/ev-poppler.cc'), (factory, '/ev-document-factory.c'),
                      (glib, '/poppler-document.cc'), (core, '/Parser.cc'),
                      (core, '/Lexer.cc'), (core, '/XRef.cc'), (core, '/PDFDoc.cc')):
    if not lines([f for f in group if f['filename'].endswith(suffix)]):
        raise SystemExit(f'no parser source coverage in {suffix}')


def regions(name):
    """Executed region-entry segments in the Atril PDF backend and Poppler."""
    report = json.loads(Path(f'/coverage/{name}-segments.json').read_text())
    found = {}
    for source in report['data'][0]['files']:
        filename = source['filename']
        if not filename.startswith((ATRIL_PDF, GLIB, CORE)):
            continue
        for line, column, count, has_count, entry, *_ in source['segments']:
            if has_count and entry and count > 0:
                found[(filename, line, column)] = count
    return found


control_regions, variant_regions = regions('control'), regions('variant')
shared = control_regions.keys() & variant_regions.keys()
changed = {key for key in shared if control_regions[key] != variant_regions[key]}
variant_only = variant_regions.keys() - control_regions.keys()
control_only = control_regions.keys() - variant_regions.keys()
in_core = lambda keys: sum(1 for key in keys if key[0].startswith(CORE))
if not in_core(changed | variant_only | control_only):
    raise SystemExit('valid variant does not change Poppler core parser execution')
for name in ('control', 'variant'):
    Path(f'/coverage/{name}-segments.json').unlink()
differential = {'control_output': observed, 'variant_output': variant,
                'control_parser_regions': len(control_regions),
                'variant_parser_regions': len(variant_regions),
                'variant_only_regions': len(variant_only),
                'control_only_regions': len(control_only),
                'shared_regions_with_different_counts': len(changed),
                'poppler_core_regions_differing': in_core(changed | variant_only | control_only)}
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(atril),
           'parser_source_lines_covered': lines(atril),
           'format_specific_source_lines_covered': lines(atril),
           'factory_source_lines_covered': lines(factory),
           'poppler_glib_source_lines_covered': lines(glib),
           'underlying_source_files': len(core),
           'underlying_source_lines_covered': lines(core),
           'valid_variant_differential': differential,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY
