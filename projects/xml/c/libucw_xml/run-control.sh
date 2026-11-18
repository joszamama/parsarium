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
expected={'attributes':['version=1','id=a1','{urn:parsarium:catalog}lang=es','id=b2'],
          'elements':['{urn:parsarium:catalog}catalog','{urn:parsarium:item}item','{urn:parsarium:item}item','{urn:parsarium:item}name','{urn:parsarium:item}note'],
          'max_depth':3,'namespace_declarations':2,'namespaces':['urn:parsarium:catalog','urn:parsarium:item'],
          'root':'{urn:parsarium:catalog}catalog','text':['Café & té','Zürich <HQ>','x < y']}
if observed!=expected:raise SystemExit(f'control mismatch: {observed}')
files=json.loads(Path('/coverage/coverage.json').read_text())['data'][0]['files']
parser=[f for f in files if f['filename'].startswith('/work/source/ucw-xml/')]
covered=sum(f['summary']['lines']['covered'] for f in parser)
if not parser or not covered:raise SystemExit('no instrumented ucw-xml lines covered')
summary={'control_pass':True,'output':observed,'parser_source_files':len(parser),'parser_source_lines_covered':covered,
         'parser_file_lines_covered':{f['filename'].removeprefix('/work/source/ucw-xml/'):f['summary']['lines']['covered'] for f in parser if f['summary']['lines']['covered']},
         'coverage':'/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
PY_CHECK
