#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=javazoom.spi.*:javazoom.jl.decoder.* \
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/mp3spi-1.9.5.4.jar --sourcefiles /work/parser-source --xml /coverage/mp3spi.xml --quiet
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/jlayer-1.0.1.4.jar --sourcefiles /work/underlying-source --xml /coverage/jlayer.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
observed = json.loads(Path('/coverage/observed.raw').read_text().strip().splitlines()[-1])
expected = {'codec': 'MP3', 'sample_rate': 44100, 'channels': 1,
            'frames': 11, 'decoded_samples': 12672}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
files = []
counts = {}
for group, source_root, report in (
    ('parser', '/work/parser-source', '/coverage/mp3spi.xml'),
    ('underlying', '/work/underlying-source', '/coverage/jlayer.xml'),
):
    group_files = []
    for package in ET.parse(report).getroot().findall('package'):
        for source in package.findall('sourcefile'):
            executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                              if int(line.attrib['ci']) > 0)
            if executed:
                group_files.append({
                    'filename': f"{source_root}/{package.attrib['name']}/{source.attrib['name']}",
                    'summary': {'lines': {'covered': len(executed)}},
                    'executed_lines': executed,
                })
    counts[group] = (len(group_files), sum(f['summary']['lines']['covered'] for f in group_files))
    files.extend(group_files)
if not any(f['filename'].endswith('/DecodedMpegAudioInputStream.java')
           for f in files if f['filename'].startswith('/work/parser-source/')):
    raise SystemExit('no MP3SPI decoder stream source lines covered')
if not any(f['filename'].endswith('/LayerIIIDecoder.java')
           for f in files if f['filename'].startswith('/work/underlying-source/')):
    raise SystemExit('no soundlibs Layer III decoder source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': counts['parser'][0],
           'parser_source_lines_covered': counts['parser'][1],
           'underlying_source_files': counts['underlying'][0],
           'underlying_source_lines_covered': counts['underlying'][1],
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
