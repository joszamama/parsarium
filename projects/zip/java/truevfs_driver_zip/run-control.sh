#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=* \
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/truevfs-comp-zip-0.14.0.jar \
  --classfiles /work/lib/truevfs-comp-zipdriver-0.14.0.jar \
  --classfiles /work/lib/truevfs-driver-zip-0.14.0.jar \
  --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text()
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads("{\"name\":\"hello.txt\",\"content_base64\":\"cGFyc2FyaXVtCg==\"}")
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
primary = [f for f in files if f['filename'].startswith(
    '/work/parser-source/net/java/truevfs/driver/zip/')]
primary_covered = sum(f['summary']['lines']['covered'] for f in primary)
if primary_covered == 0:
    raise SystemExit('no parser package source lines covered')
zip_core = [f for f in files if f['filename'].endswith(
    '/net/java/truevfs/comp/zip/AbstractZipFile.java')]
if not zip_core or zip_core[0]['summary']['lines']['covered'] == 0:
    raise SystemExit('no TrueVFS ZIP core source lines covered')
zip_core_lines = zip_core[0]['summary']['lines']['covered']
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(primary), 'parser_source_lines_covered': primary_covered,
           'underlying_source_files': sum(f['filename'].startswith(
               '/work/parser-source/net/java/truevfs/comp/zip/') for f in files),
           'underlying_source_lines_covered': sum(f['summary']['lines']['covered']
               for f in files if f['filename'].startswith(
                   '/work/parser-source/net/java/truevfs/comp/zip/')),
           'format_specific_source_lines_covered': zip_core_lines,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
