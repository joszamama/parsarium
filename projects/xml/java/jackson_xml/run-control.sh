#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=com.fasterxml.jackson.dataformat.xml.*:com.ctc.wstx.sr.* \
  -Dstdout.encoding=UTF-8 -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/jackson-dataformat-xml-2.23.0.jar --sourcefiles /work/parser-source/module --xml /coverage/module.xml --quiet
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/woodstox-core-7.3.0.jar --sourcefiles /work/parser-source/underlying --xml /coverage/underlying.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = {
    'events': ['START_OBJECT', 'FIELD_NAME:version', 'VALUE_STRING:1',
               'FIELD_NAME:item', 'START_OBJECT', 'FIELD_NAME:id', 'VALUE_STRING:a1',
               'FIELD_NAME:lang', 'VALUE_STRING:es', 'FIELD_NAME:',
               'VALUE_STRING:Café & té', 'END_OBJECT', 'FIELD_NAME:item',
               'START_OBJECT', 'FIELD_NAME:id', 'VALUE_STRING:b2',
               'FIELD_NAME:name', 'VALUE_STRING:Zürich <HQ>', 'FIELD_NAME:note',
               'VALUE_STRING:x < y', 'END_OBJECT', 'END_OBJECT'],
    'token_count': 22,
}
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
    raise SystemExit(f'missing XML module or Woodstox source lines: {module_lines}/{underlying_lines}')
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
