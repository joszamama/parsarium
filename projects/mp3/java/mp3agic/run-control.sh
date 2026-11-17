#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=com.mpatric.mp3agic.Mp3File*:com.mpatric.mp3agic.MpegFrame*:com.mpatric.mp3agic.BufferTools* \
  -cp /work/classes:/work/parser.jar GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/parser.jar --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
observed = json.loads(Path('/coverage/observed.raw').read_text().strip().splitlines()[-1])
expected = {'codec': 'MP3', 'mpeg_version': '1.0', 'layer': 'III',
            'sample_rate': 44100, 'channel_mode': 'Mono', 'bitrate_kbps': 64}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
root = ET.parse('/coverage/jacoco.xml').getroot()
files = []
for package in root.findall('package'):
    for source in package.findall('sourcefile'):
        executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                          if int(line.attrib['ci']) > 0)
        if executed:
            files.append({'filename': f"/work/parser-source/{package.attrib['name']}/{source.attrib['name']}",
                          'summary': {'lines': {'covered': len(executed)}},
                          'executed_lines': executed})
names = {Path(f['filename']).name for f in files}
if not {'Mp3File.java', 'MpegFrame.java'} <= names:
    raise SystemExit(f'file scanner and MPEG frame parser not both covered: {names}')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files),
           'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in files),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
