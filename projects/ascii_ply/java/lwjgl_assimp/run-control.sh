#!/bin/sh
set -eu
mkdir -p /coverage
profiles=$(mktemp -d /tmp/parsarium-llvm.XXXXXX)
# 1. Published natives-linux-arm64 libraries, no instrumentation: the selected artifact itself.
PARSARIUM_LWJGL_NATIVE_DIR=/work/native-stock \
  java -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/stock.raw
# 2. Same Java classes over the source-built Assimp: JaCoCo for the LWJGL wrapper,
#    LLVM source coverage for the native PLY importer.
PARSARIUM_LWJGL_NATIVE_DIR=/work/native LLVM_PROFILE_FILE="$profiles/native-%p-%m.profraw" \
  java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=* \
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/lwjgl-assimp-3.4.3.jar --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
llvm-profdata merge "$profiles"/*.profraw -o "$profiles/native.profdata"
llvm-cov export /work/native/libassimp.so -instr-profile="$profiles/native.profdata" \
  /work/source/code/AssetLib/Ply > /coverage/native-llvm.json
rm -rf "$profiles"
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
expected = {"vertices": 3, "faces": 1, "indices": [0, 1, 2]}
stock = json.loads(Path('/coverage/stock.raw').read_text().strip().splitlines()[-1])
if stock != expected:
    raise SystemExit(f'stock native control mismatch: {stock}')
observed = json.loads(Path('/coverage/observed.raw').read_text().strip().splitlines()[-1])
if observed != expected:
    raise SystemExit(f'instrumented native control mismatch: {observed}')
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
    raise SystemExit('no LWJGL wrapper source lines covered')
native = [f for f in json.loads(Path('/coverage/native-llvm.json').read_text())['data'][0]['files']
          if f['filename'].startswith('/work/source/code/AssetLib/Ply/')
          and f['summary']['lines']['covered'] > 0]
native_lines = sum(f['summary']['lines']['covered'] for f in native)
if native_lines == 0:
    raise SystemExit('no native Assimp PLY source lines covered')
summary = {'control_pass': True, 'stock_native_control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': wrapper_lines,
           'underlying_source_files': len(native), 'underlying_source_lines_covered': native_lines,
           'abi_check': json.loads(Path('/work/abi-check.json').read_text()),
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files + native}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k != 'abi_check'}))
PYRUN
