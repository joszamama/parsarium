#!/bin/sh
set -eu

test -f /input/control
mkdir -p /coverage
LLVM_PROFILE_FILE=/coverage/control.profraw /work/replay /input/control > /coverage/observed.json
/work/llvm-profdata merge -sparse /coverage/control.profraw -o /coverage/control.profdata
/work/llvm-cov export /work/replay -instr-profile=/coverage/control.profdata > /coverage/coverage.json
CRATE_DIR="${CRATE_DIR:-/packet-dissector-dns-0.6.3/}" python3 - <<'PY'
import json
import os
from pathlib import Path

crate = os.environ["CRATE_DIR"]
observed = json.loads(Path('/coverage/observed.json').read_text(encoding='utf-8'))
expected = json.loads('{"id": 43981, "qr": 1, "opcode": 0, "aa": 0, "tc": 0, "rd": 1, "ra": 1, "z": 0, "rcode": 0, "qdcount": 1, "ancount": 4, "nscount": 0, "arcount": 0, "questions": [{"name": "www.example.test.", "type": 1, "class": 1}], "answers": [{"name": "www.example.test.", "type": 5, "class": 1, "ttl": 3600, "rdata": "example.test."}, {"name": "example.test.", "type": 1, "class": 1, "ttl": 300, "rdata": "192.0.2.10"}, {"name": "example.test.", "type": 28, "class": 1, "ttl": 600, "rdata": "2001:db8::10"}, {"name": "example.test.", "type": 15, "class": 1, "ttl": 7200, "rdata": "10 mail.example.test."}], "authority": [], "additional": []}')
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
coverage = json.loads(Path('/coverage/coverage.json').read_text())
files = coverage['data'][0]['files']
parser_files = [f for f in files if crate in f['filename']]
covered = sum(f['summary']['lines']['covered'] for f in parser_files)
if not parser_files or covered == 0:
    raise SystemExit('no instrumented parser crate source lines covered')
result = {'control_pass': True, 'output': observed,
          'parser_source_files': len(parser_files),
          'parser_source_lines_covered': covered,
          'parser_file_lines_covered': {f['filename'].split(crate, 1)[1]:
                                        f['summary']['lines']['covered'] for f in parser_files},
          'coverage': '/coverage/coverage.json'}
Path('/coverage/summary.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
PY
