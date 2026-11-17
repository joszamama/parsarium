#!/bin/sh
set -eu
mkdir -p /coverage
profiles=$(mktemp -d /tmp/parsarium-llvm.XXXXXX)
# JaCoCo for the F3D Java binding classes; LLVM source coverage for the JNI
# binding, F3D's static native PLY plugin and VTK's vtkPLYReader/vtkPLY, all
# linked into the source-built libf3d-java.so.
LLVM_PROFILE_FILE="$profiles/native-%p-%m.profraw" \
  java -javaagent:/work/jacocoagent.jar=destfile=/coverage/jacoco.exec,append=false,includes=* \
  -cp '/work/classes:/work/lib/*' GenericHarness /input/control > /coverage/observed.raw
java -jar /work/jacococli.jar report /coverage/jacoco.exec \
  --classfiles /work/lib/f3d.jar --sourcefiles /work/parser-source --xml /coverage/jacoco.xml --quiet
llvm-profdata merge "$profiles"/*.profraw -o "$profiles/native.profdata"
llvm-cov export /work/native/libf3d-java.so -instr-profile="$profiles/native.profdata" \
  /work/vtk/source/IO/PLY /work/f3d/source/plugins/native /work/f3d/build/f3d/plugins/native \
  /work/f3d/source/java > /coverage/native-llvm.json
rm -rf "$profiles"
python3 - <<'PYRUN'
import json
from pathlib import Path
import xml.etree.ElementTree as ET
expected = {"files": 1, "actors": 1, "points": 3, "cells": 1}
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
binding_lines = sum(f['summary']['lines']['covered'] for f in files)
native = [f for f in json.loads(Path('/coverage/native-llvm.json').read_text())['data'][0]['files']
          if f['summary']['lines']['covered'] > 0]
def lines(prefix, suffix=''):
    return sum(f['summary']['lines']['covered'] for f in native
               if f['filename'].startswith(prefix) and f['filename'].endswith(suffix))
vtk = [f for f in native if f['filename'].startswith('/work/vtk/source/IO/PLY/vtkPLY')]
vtk_lines = lines('/work/vtk/source/IO/PLY/vtkPLY')
parser = lines('/work/vtk/source/IO/PLY/', '/vtkPLY.cxx')
vtk_reader = lines('/work/vtk/source/IO/PLY/', '/vtkPLYReader.cxx')
plugin_reader = lines('/work/f3d/source/plugins/native/', '/vtkF3DPLYReader.cxx')
plugin_entry = lines('/work/f3d/build/f3d/plugins/native/', '/reader_PLYReader.h')
jni = lines('/work/f3d/source/java/')
if min(binding_lines, vtk_lines, parser, vtk_reader, plugin_reader, plugin_entry, jni) <= 0:
    raise SystemExit('missing Java binding, JNI, F3D PLY plugin or VTK vtkPLYReader/vtkPLY lines')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files), 'parser_source_lines_covered': binding_lines,
           'underlying_source_files': len(vtk), 'underlying_source_lines_covered': vtk_lines,
           'underlying_format_specific_source_lines_covered': parser,
           'underlying_reader_lines_covered': vtk_reader,
           'native_plugin_reader_lines_covered': plugin_reader,
           'native_plugin_entry_lines_covered': plugin_entry,
           'jni_binding_lines_covered': jni,
           'coverage': '/coverage/coverage.json'}
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
Path('/coverage/coverage.json').write_text(json.dumps({'data': [{'files': files + native}]}, indent=2) + '\n')
Path('/coverage/summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
PYRUN
