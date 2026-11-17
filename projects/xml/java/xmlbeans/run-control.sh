#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=org.apache.xmlbeans.impl.store.*:org.apache.xmlbeans.impl.common.SAXHelper:com.sun.org.apache.xerces.internal.*,inclbootstrapclasses=true \
  -Dstdout.encoding=UTF-8 -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/module-classes --sourcefiles /work/parser-source/module --xml /coverage/module.xml --quiet
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/parser-classes --sourcefiles /work/parser-source/underlying --xml /coverage/underlying.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads("{\"attributes\":[\"version=1\",\"id=a1\",\"{urn:parsarium:catalog}lang=es\",\"id=b2\"],\"elements\":[\"{urn:parsarium:catalog}catalog\",\"{urn:parsarium:item}item\",\"{urn:parsarium:item}item\",\"{urn:parsarium:item}name\",\"{urn:parsarium:item}note\"],\"max_depth\":3,\"namespace_declarations\":2,\"namespaces\":[\"urn:parsarium:catalog\",\"urn:parsarium:item\"],\"root\":\"{urn:parsarium:catalog}catalog\",\"text\":[\"Caf\\u00e9 & t\\u00e9\",\"Z\\u00fcrich <HQ>\",\"x < y\"]}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
def files_for(subject):
    root = ET.parse(f'/coverage/{subject}.xml').getroot()
    files = []
    for package in root.findall('package'):
        for source in package.findall('sourcefile'):
            executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                              if int(line.attrib['ci']) > 0)
            if executed:
                filename = f"/work/parser-source/{subject}/{package.attrib['name']}/{source.attrib['name']}"
                files.append({'filename': filename,
                              'summary': {'lines': {'covered': len(executed)}},
                              'executed_lines': executed})
    return files
module = files_for('module')
underlying = files_for('underlying')
module_lines = sum(f['summary']['lines']['covered'] for f in module)
underlying_lines = sum(f['summary']['lines']['covered'] for f in underlying)
if not module_lines or not underlying_lines:
    raise SystemExit(f'missing XMLBeans tree or JDK Xerces source lines: {module_lines}/{underlying_lines}')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(module), 'parser_source_lines_covered': module_lines,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_lines,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': module + underlying}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(summary, ensure_ascii=False))
PYRUN
