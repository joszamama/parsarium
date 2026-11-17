#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=org.dom4j.*:com.sun.org.apache.xerces.internal.*,inclbootstrapclasses=true \
  -Dstdout.encoding=UTF-8 -cp /work/classes:/work/lib/dom4j-2.2.0.jar GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/dom4j-2.2.0.jar --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/underlying-classes --sourcefiles /work/underlying-source --xml /coverage/jacoco-underlying.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads("{\"attributes\":[\"version=1\",\"id=a1\",\"{urn:parsarium:catalog}lang=es\",\"id=b2\"],\"elements\":[\"{urn:parsarium:catalog}catalog\",\"{urn:parsarium:item}item\",\"{urn:parsarium:item}item\",\"{urn:parsarium:item}name\",\"{urn:parsarium:item}note\"],\"max_depth\":3,\"namespace_declarations\":2,\"namespaces\":[\"urn:parsarium:catalog\",\"urn:parsarium:item\"],\"root\":\"{urn:parsarium:catalog}catalog\",\"text\":[\"Caf\\u00e9 & t\\u00e9\",\"Z\\u00fcrich <HQ>\",\"x < y\"]}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')


def covered(report, prefix):
    files = []
    for package in ET.parse(report).getroot().findall('package'):
        for source in package.findall('sourcefile'):
            executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                              if int(line.attrib['ci']) > 0)
            if executed:
                files.append({'filename': f"{prefix}{package.attrib['name']}/{source.attrib['name']}",
                              'summary': {'lines': {'covered': len(executed)}},
                              'executed_lines': executed})
    return files


parser = covered('/coverage/jacoco.xml', '/work/parser-source/')
underlying = covered('/coverage/jacoco-underlying.xml', '/work/underlying-source/')
parser_lines = sum(f['summary']['lines']['covered'] for f in parser)
underlying_lines = sum(f['summary']['lines']['covered'] for f in underlying)
if parser_lines == 0:
    raise SystemExit('no dom4j source lines covered')
# The tokenizer must be the JDK Xerces fork reached through JAXP, not dom4j itself.
names = {f['filename'].removeprefix('/work/underlying-source/') for f in underlying}
for required in ('com/sun/org/apache/xerces/internal/jaxp/SAXParserImpl.java',
                 'com/sun/org/apache/xerces/internal/impl/XMLNSDocumentScannerImpl.java'):
    if required not in names:
        raise SystemExit(f'underlying JAXP Xerces path not executed: {required}')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser), 'parser_source_lines_covered': parser_lines,
           'underlying_source_files': len(underlying),
           'underlying_source_lines_covered': underlying_lines,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': parser + underlying}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
