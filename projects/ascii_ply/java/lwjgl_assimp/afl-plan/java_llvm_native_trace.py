"""Draft AFL++ trace for LWJGL Assimp: native PLY importer regions, optionally plus wrapper lines.

Not wired into fuzzing/afl-bridge yet; see ../AFL_PLAN.md. Features carry a "native:" or
"java:" prefix so the two provenance groups never share a feature string.
"""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

NATIVE_LIBRARY = '/work/native/libassimp.so'
NATIVE_PREFIX = '/work/source/code/AssetLib/Ply/'


def native_features(profiles: Path) -> set[str]:
    raws = sorted(profiles.glob('*.profraw'))
    if not raws:
        return set()
    profdata = profiles / 'case.profdata'
    subprocess.run(['llvm-profdata', 'merge', *map(str, raws), '-o', str(profdata)],
                   check=True, stdout=subprocess.DEVNULL)
    export = subprocess.run(['llvm-cov', 'export', NATIVE_LIBRARY,
                             f'-instr-profile={profdata}', NATIVE_PREFIX],
                            check=True, capture_output=True, text=True)
    features = set()
    for file in json.loads(export.stdout)['data'][0]['files']:
        filename = file['filename']
        if not filename.startswith(NATIVE_PREFIX):
            continue
        for line, column, count, has_count, region_start, *_ in file['segments']:
            if has_count and region_start and count > 0:
                features.add(f'native:{filename}:{line}:{column}')
        for branch in file.get('branches', []):
            line, column = branch[0], branch[1]
            if branch[4] > 0:
                features.add(f'native:{filename}:{line}:{column}:true')
            if branch[5] > 0:
                features.add(f'native:{filename}:{line}:{column}:false')
    return features


def java_features(execution: Path, work: Path) -> set[str]:
    report = work / 'wrapper.xml'
    subprocess.run(['java', '-jar', '/work/jacococli.jar', 'report', str(execution),
                    '--classfiles', '/work/lib/lwjgl-assimp-3.4.3.jar',
                    '--sourcefiles', '/work/parser-source', '--xml', str(report), '--quiet'],
                   check=True, capture_output=True, text=True, timeout=30)
    features = set()
    for package in ET.parse(report).getroot().findall('package'):
        for source in package.findall('sourcefile'):
            for line in source.findall('line'):
                if int(line.attrib['ci']) > 0:
                    features.add(f"java:{package.attrib['name']}/{source.attrib['name']}:{line.attrib['nr']}")
    return features


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(2)
    scope = os.environ.get('PARSARIUM_FEEDBACK_SCOPE', 'native')
    if scope not in {'native', 'dual'}:
        raise SystemExit(f'unknown feedback scope: {scope}')
    with tempfile.TemporaryDirectory(prefix='parsarium-lwjgl-assimp-') as temporary:
        work = Path(temporary)
        execution = work / 'jacoco.exec'
        command = ['java']
        if scope == 'dual':
            command.append(f'-javaagent:/work/jacocoagent.jar=destfile={execution},append=false,includes=*')
        command += ['-cp', '/work/afl-java-classes:/work/classes:/work/lib/*', 'JavaCase', sys.argv[1]]
        environment = {**os.environ, 'PARSARIUM_TARGET_CLASS': 'GenericHarness',
                       'PARSARIUM_LWJGL_NATIVE_DIR': '/work/native',
                       'LLVM_PROFILE_FILE': str(work / 'case-%p-%m.profraw')}
        result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=30)
        # A native fault kills the JVM before the profile runtime writes; record what exists.
        features = native_features(work)
        if scope == 'dual' and execution.exists():
            features |= java_features(execution, work)
        Path(sys.argv[2]).write_text(''.join(f'{feature}\n' for feature in sorted(features)))
        if result.returncode:
            sys.stderr.write(result.stdout[-1000:] + result.stderr[-1000:])
            raise SystemExit(1)


if __name__ == '__main__':
    main()
