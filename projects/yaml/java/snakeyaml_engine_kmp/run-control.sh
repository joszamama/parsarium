#!/bin/sh
set -eu
mkdir -p /coverage
java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=it.krzeminski.snakeyaml.engine.kmp.* \
  -Dstdout.encoding=UTF-8 -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/parser-classes --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
raw = Path('/coverage/observed.raw').read_text(encoding='utf-8')
observed = json.loads(raw.strip().splitlines()[-1])
expected = json.loads("{\"tree\":[\"map\",[[\"kind\",[\"str\",\"catalog\"]],[\"version\",[\"int\",\"2\"]],[\"ratio\",[\"float\",\"0.25\"]],[\"offset\",[\"int\",\"-17\"]],[\"enabled\",[\"bool\",true]],[\"retired\",[\"bool\",false]],[\"missing\",[\"null\"]],[\"title\",[\"str\",\"Caf\\u00e9 \\\"quoted\\\"\\tend\"]],[\"single\",[\"str\",\"it's here\"]],[\"tags\",[\"seq\",[[\"str\",\"alpha\"],[\"str\",\"beta\"],[\"str\",\"gamma delta\"]]]],[\"point\",[\"map\",[[\"lat\",[\"int\",\"1\"]],[\"lon\",[\"float\",\"-2.5\"]]]]],[\"items\",[\"seq\",[[\"map\",[[\"id\",[\"int\",\"7\"]],[\"name\",[\"str\",\"first item\"]],[\"note\",[\"str\",\"line one\\nline two\\n\"]]]],[\"map\",[[\"id\",[\"int\",\"8\"]],[\"name\",[\"str\",\"Z\\u00fcrich\"]],[\"note\",[\"str\",\"folded text\\n\"]]]]]]],[\"defaults\",[\"map\",[[\"retries\",[\"int\",\"3\"]],[\"label\",[\"str\",\"base\"]]]]],[\"service\",[\"map\",[[\"settings\",[\"map\",[[\"retries\",[\"int\",\"3\"]],[\"label\",[\"str\",\"base\"]]]]],[\"label\",[\"str\",\"edge\"]]]]]]]}")
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
covered = sum(f['summary']['lines']['covered'] for f in files)
if covered == 0:
    raise SystemExit('no parser package source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': covered,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps(summary))
PYRUN
