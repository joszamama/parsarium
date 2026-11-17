#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=org.jzy3d.*:org.smurn.jply.* \
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/jzy3d-core-2.2.1.jar --sourcefiles /work/parser-source/module --xml /coverage/module.xml --quiet
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/underlying-lib --sourcefiles /work/parser-source/underlying --xml /coverage/underlying.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = {"vertices": 3, "second_x": 1.0, "third_y": 1.0}
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
covered = sum(f['summary']['lines']['covered'] for f in module)
underlying_lines = sum(f['summary']['lines']['covered'] for f in underlying)
if not covered or not underlying_lines:
    raise SystemExit(f'missing wrapper or underlying parser source lines: {covered}/{underlying_lines}')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(module), 'parser_source_lines_covered': covered,
           'underlying_source_files': len(underlying), 'underlying_source_lines_covered': underlying_lines,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': module + underlying}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
