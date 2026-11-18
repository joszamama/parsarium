#!/bin/sh
set -eu
mkdir -p /coverage
profiles=$(mktemp -d /tmp/parsarium-llvm.XXXXXX)
# The unmodified pdal_2.13 classes and pdal-native JNI library (sbt-jni NativeLoader extracts it
# from pdal-native-2.10.0.jar) over PDAL 2.10.2 built from its release source with LLVM coverage.
LLVM_PROFILE_FILE="$profiles/native-%p-%m.profraw" \
  java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=io.pdal.* \
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/pdal_2.13-2.10.0.jar --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
llvm-profdata merge "$profiles"/*.profraw -o "$profiles/native.profdata"
llvm-cov export /work/native/libpdalcpp.so.20 -instr-profile="$profiles/native.profdata" \
  /work/source/io/PlyReader.cpp > /coverage/native-llvm.json
rm -rf "$profiles"
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
expected = {"points": 3, "second_x": 1.0, "last_y": 1.0}
observed = json.loads(Path('/coverage/observed.raw').read_text().strip().splitlines()[-1])
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
wrapper_lines = sum(f['summary']['lines']['covered'] for f in files)
if wrapper_lines == 0:
    raise SystemExit('no pdal_2.13 wrapper source lines covered')
native = [f for f in json.loads(Path('/coverage/native-llvm.json').read_text())['data'][0]['files']
          if f['filename'] == '/work/source/io/PlyReader.cpp'
          and f['summary']['lines']['covered'] > 0]
native_lines = sum(f['summary']['lines']['covered'] for f in native)
if native_lines == 0:
    raise SystemExit('no PDAL PlyReader source lines covered')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': wrapper_lines,
           'underlying_source_files': len(native), 'underlying_source_lines_covered': native_lines,
           'abi_check': json.loads(Path('/work/abi-check.json').read_text()),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files + native}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k != 'abi_check'}))
PYRUN
