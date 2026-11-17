#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
SUBJECT="${SUBJECT:-/work/libtins-src/}" python3 - <<'PY'
import json
import os
from pathlib import Path
subject = os.environ['SUBJECT']
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = json.loads('{"id": 43981, "qr": 1, "opcode": 0, "aa": 0, "tc": 0, "rd": 1, "ra": 1, "z": 0, "rcode": 0, "qdcount": 1, "ancount": 4, "nscount": 0, "arcount": 0, "questions": [{"name": "www.example.test.", "type": 1, "class": 1}], "answers": [{"name": "www.example.test.", "type": 5, "class": 1, "ttl": 3600, "rdata": "example.test."}, {"name": "example.test.", "type": 1, "class": 1, "ttl": 300, "rdata": "192.0.2.10"}, {"name": "example.test.", "type": 28, "class": 1, "ttl": 600, "rdata": "2001:db8::10"}, {"name": "example.test.", "type": 15, "class": 1, "ttl": 7200, "rdata": "10 mail.example.test."}], "authority": [], "additional": []}')
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
source = [f for f in coverage['data'][0]['files'] if f['filename'].startswith(subject)]
lines = sum(f['summary']['lines']['covered'] for f in source)
if lines == 0:
    raise SystemExit('no parser source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(source), 'parser_source_lines_covered': lines,
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
