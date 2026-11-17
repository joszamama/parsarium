#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
python3 - <<'PY_CHECK'
import json
from pathlib import Path
observed=json.loads(Path('/coverage/observed.json').read_text())
expected={'attributes':['xmlns:c=urn:parsarium:catalog','xmlns=urn:parsarium:item','version=1','id=a1','c:lang=es','id=b2'],
          'elements':['c:catalog','item','item','name','note'],'max_depth':3,'root':'c:catalog',
          'text':['Café & té','Zürich <HQ>','x < y']}
if observed!=expected:raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser=[f for f in files if f['filename'].startswith('/work/source/src/')]
covered=sum(f['summary']['lines']['covered'] for f in parser)
if not parser or not covered:raise SystemExit('no instrumented libxmlb source lines covered')
markup=[f for f in files if f['filename']=='/work/glib/glib/gmarkup.c']
markup_covered=sum(f['summary']['lines']['covered'] for f in markup)
if len(markup)!=1 or not markup_covered:raise SystemExit('no instrumented GMarkup lines covered')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,
         'parser_file_lines_covered':{f['filename'].removeprefix('/work/source/'):f['summary']['lines']['covered'] for f in parser if f['summary']['lines']['covered']},
         'underlying_source_files':len(markup),'underlying_source_lines_covered':markup_covered,
         'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PY_CHECK
