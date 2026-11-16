#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=* \
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/jvm-2.5.jar --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/core-2.5.jar --sourcefiles /work/underlying-source --xml /coverage/jacoco-core.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads("{\"sample_rate\":8000,\"channels\":1,\"bits\":16,\"frames\":256}")
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = []
counts = {}
for kind, xml, source_root in (
    ('parser', '/coverage/jacoco.xml', '/work/parser-source'),
    ('underlying', '/coverage/jacoco-core.xml', '/work/underlying-source'),
):
    covered_files = []
    for package in ET.parse(xml).getroot().findall('package'):
        for source in package.findall('sourcefile'):
            executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                              if int(line.attrib['ci']) > 0)
            if executed:
                filename = f"{source_root}/{package.attrib['name']}/{source.attrib['name']}"
                covered_files.append({'filename': filename,
                                      'summary': {'lines': {'covered': len(executed)}},
                                      'executed_lines': executed})
    counts[kind] = (len(covered_files), sum(f['summary']['lines']['covered'] for f in covered_files))
    files.extend(covered_files)
if counts['parser'][1] == 0 or counts['underlying'][1] == 0:
    raise SystemExit('no TarsosDSP JVM or core source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': counts['parser'][0], 'parser_source_lines_covered': counts['parser'][1],
           'underlying_source_files': counts['underlying'][0],
           'underlying_source_lines_covered': counts['underlying'][1],
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
