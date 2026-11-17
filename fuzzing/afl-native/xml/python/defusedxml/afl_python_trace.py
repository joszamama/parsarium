"""Map executed defusedxml/ElementTree-driver lines and Expat regions to AFL++ features.

Only the defusedxml.ElementTree.parse call is traced: defusedxml's parser
factory and guard handlers, CPython's ElementTree.py XMLParser callbacks and
the Expat tokenizer. Harness lines and the post-parse summary are not features.
"""

import glob
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import trace

DRIVER_PREFIX = '/usr/lib/python3.14/xml/etree/'
NATIVE_PREFIX = '/work/expat/lib/'


def case(source: str, output: str) -> None:
    from harness import PARSE_ERRORS, parse_tree

    def parse() -> None:
        try:
            parse_tree(Path(source).read_bytes())
        except PARSE_ERRORS:
            pass

    prefixes = (os.environ['PARSARIUM_SUBJECT_PREFIX'], DRIVER_PREFIX)
    tracer = trace.Trace(count=True, trace=False)
    tracer.runfunc(parse)
    lines = {f'{Path(filename).resolve()}:{line}'
             for (filename, line), hits in tracer.results().counts.items()
             if hits > 0 and str(Path(filename).resolve()).startswith(prefixes)}
    Path(output).write_text('\n'.join(sorted(lines)) + '\n')


def main() -> None:
    if len(sys.argv) == 4 and sys.argv[1] == '--case':
        case(sys.argv[2], sys.argv[3])
        return
    if len(sys.argv) != 3:
        raise SystemExit(2)
    modules = glob.glob(os.environ['PARSARIUM_LLVM_MODULE_GLOB'])
    if len(modules) != 1:
        raise SystemExit(f'expected one native module, found {modules}')
    with tempfile.TemporaryDirectory(prefix='parsarium-llvm-') as temporary:
        root = Path(temporary)
        environment = {**os.environ, 'LLVM_PROFILE_FILE': str(root / 'case.profraw')}
        subprocess.run([sys.executable, __file__, '--case', sys.argv[1], str(root / 'python.txt')],
                       env=environment, check=True, stdout=subprocess.DEVNULL)
        features = set((root / 'python.txt').read_text().splitlines()) - {''}
        if not features:
            raise SystemExit('no defusedxml/ElementTree driver source lines executed')
        subprocess.run(['llvm-profdata', 'merge', str(root / 'case.profraw'),
                        '-o', str(root / 'case.profdata')], check=True,
                       stdout=subprocess.DEVNULL)
        result = subprocess.run(['llvm-cov', 'export', modules[0],
                                 f'-instr-profile={root / "case.profdata"}'],
                                check=True, capture_output=True, text=True)
    native = set()
    for file in json.loads(result.stdout)['data'][0]['files']:
        filename = file['filename']
        if not filename.startswith(NATIVE_PREFIX):
            continue
        for line, column, count, has_count, region_start, *_ in file['segments']:
            if has_count and region_start and count > 0:
                native.add(f'{filename}:{line}:{column}')
        for branch in file.get('branches', []):
            line, column, *_ = branch
            if branch[4] > 0:
                native.add(f'{filename}:{line}:{column}:true')
            if branch[5] > 0:
                native.add(f'{filename}:{line}:{column}:false')
    if not native:
        raise SystemExit('no Expat source regions covered')
    Path(sys.argv[2]).write_text('\n'.join(sorted(features | native)) + '\n')


if __name__ == '__main__':
    main()
