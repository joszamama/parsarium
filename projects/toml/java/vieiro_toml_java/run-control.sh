#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=net.vieiro.toml.* \
  -Dstdout.encoding=UTF-8 -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/parser-classes --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text(encoding='utf-8')
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads(r'''{"database":{"limits":{"max":{"type":"integer","value":"10"},"min":{"type":"integer","value":"-2"}},"ports":[{"type":"integer","value":"8000"},{"type":"integer","value":"8001"},{"type":"integer","value":"8002"}],"ratio":{"type":"float","value":"3.25"}},"enabled":{"type":"bool","value":"true"},"owner":{"name":{"type":"string","value":"Zo\u00eb"},"since":{"type":"datetime","value":"1979-05-27T07:32:00Z"}},"products":[{"name":{"type":"string","value":"Hammer"},"sku":{"type":"integer","value":"738594937"}},{"color":{"type":"string","value":"gray"},"name":{"type":"string","value":"Nail"},"points":[{"x":{"type":"integer","value":"1"},"y":{"type":"integer","value":"2"}},{"x":{"type":"integer","value":"3"},"y":{"type":"integer","value":"4"}}]}],"retries":{"type":"integer","value":"3"},"servers":{"alpha":{"ip":{"type":"string","value":"10.0.0.1"},"tags":[{"type":"string","value":"edge"},{"type":"string","value":"eu"}]},"beta":{"enabled":{"type":"bool","value":"false"},"ip":{"type":"string","value":"10.0.0.2"}}},"title":{"type":"string","value":"Parsarium \"service\" control"}}''')
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
root = ET.parse('/coverage/jacoco.xml').getroot()
files = []
for package in root.findall('package'):
    for source in package.findall('sourcefile'):
        source_path = Path('/work/parser-source') / package.attrib['name'] / source.attrib['name']
        if not source_path.is_file():
            raise SystemExit(f'covered class without release source: {source_path}')
        executed = sorted(int(line.attrib['nr']) for line in source.findall('line')
                          if int(line.attrib['ci']) > 0)
        if executed:
            files.append({'filename': str(source_path),
                          'summary': {'lines': {'covered': len(executed)}},
                          'executed_lines': executed})
covered = sum(f['summary']['lines']['covered'] for f in files)
if covered == 0:
    raise SystemExit('no parser package source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
