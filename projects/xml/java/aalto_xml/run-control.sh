#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=com.fasterxml.aalto.* \
  -Dstdout.encoding=UTF-8 -cp /work/classes:/work/lib/aalto-xml-1.4.0.jar:/work/lib/stax2-api-4.3.0.jar GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/aalto-xml-1.4.0.jar --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads("{\"attributes\":[\"version=1\",\"id=a1\",\"{urn:parsarium:catalog}lang=es\",\"id=b2\"],\"elements\":[\"{urn:parsarium:catalog}catalog\",\"{urn:parsarium:item}item\",\"{urn:parsarium:item}item\",\"{urn:parsarium:item}name\",\"{urn:parsarium:item}note\"],\"max_depth\":3,\"namespace_declarations\":2,\"namespaces\":[\"urn:parsarium:catalog\",\"urn:parsarium:item\"],\"root\":\"{urn:parsarium:catalog}catalog\",\"text\":[\"Caf\\u00e9 & t\\u00e9\",\"Z\\u00fcrich <HQ>\",\"x < y\"]}")
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
