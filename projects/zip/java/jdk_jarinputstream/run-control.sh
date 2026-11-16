#!/bin/sh
set -eu
test -f /input/control
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=java.util.zip.*:java.util.jar.*,inclbootstrapclasses=true \
  -cp /work/classes GenericHarness /input/control > /coverage/observed.json
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/parser-classes --sourcefiles /work/parser-sources --xml /coverage/jacoco.xml --quiet
python3 - <<'PY_CHECK'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
observed = json.loads(Path('/coverage/observed.json').read_text())
expected = json.loads("{\"name\":\"hello.txt\",\"content_base64\":\"cGFyc2FyaXVtCg==\"}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
root = ET.parse('/coverage/jacoco.xml').getroot()
files = []
for package in root.findall('package'):
    for source in package.findall('sourcefile'):
        executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                          if int(line.attrib['ci']) > 0)
        if not executed: continue
        filename = f"/work/parser-classes/{package.attrib['name']}/{source.attrib['name']}"
        files.append({'filename': filename,
                      'summary': {'lines': {'covered': len(executed)}},
                      'executed_lines': executed})
prefixes = ['/work/parser-classes/java/util/zip/', '/work/parser-classes/java/util/jar/']
parser_files = [item for item in files if any(item['filename'].startswith(p) for p in prefixes)]
covered = sum(item['summary']['lines']['covered'] for item in parser_files)
if not parser_files or covered == 0:
    raise SystemExit('no instrumented JDK format reader source lines covered')
coverage = {'data': [{'files': parser_files}]}
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(parser_files),
           'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/coverage.json').write_text(json.dumps(coverage, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PY_CHECK
