#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=com.github.mkroli.dns4s.* \
  -Dstdout.encoding=UTF-8 -cp '/work/classes:/work/lib/*' Dns4sHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/parser-classes --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads('{"id": 43981, "qr": 1, "opcode": 0, "aa": 0, "tc": 0, "rd": 1, "ra": 1, "z": 0, "rcode": 0, "qdcount": 1, "ancount": 4, "nscount": 0, "arcount": 0, "questions": [{"name": "www.example.test.", "type": 1, "class": 1}], "answers": [{"name": "www.example.test.", "type": 5, "class": 1, "ttl": 3600, "rdata": "example.test."}, {"name": "example.test.", "type": 1, "class": 1, "ttl": 300, "rdata": "192.0.2.10"}, {"name": "example.test.", "type": 28, "class": 1, "ttl": 600, "rdata": "2001:db8::10"}, {"name": "example.test.", "type": 15, "class": 1, "ttl": 7200, "rdata": "10 mail.example.test."}], "authority": [], "additional": []}')
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
root = ET.parse('/coverage/jacoco.xml').getroot()
files = []
for package in root.findall('package'):
    for source in package.findall('sourcefile'):
        executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                          if int(line.attrib['ci']) > 0)
        if executed:
            filename = f"/work/parser-source/{package.attrib['name']}/{source.attrib['name']}"
            files.append({'filename': filename,
                          'summary': {'lines': {'covered': len(executed)}},
                          'executed_lines': executed})
covered = sum(f['summary']['lines']['covered'] for f in files)
if covered == 0:
    raise SystemExit('no parser package source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
