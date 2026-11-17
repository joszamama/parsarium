"""Map executed pyquery lines and libxml2 parser.c regions to AFL++ features."""

import glob
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import trace

NATIVE_PREFIX = '/work/libxml2/parser.c'


def case(source: str, output: str) -> None:
    from harness import fuzz_one_input
    prefix = os.environ['PARSARIUM_SUBJECT_PREFIX']
    tracer = trace.Trace(count=True, trace=False)
    tracer.runfunc(fuzz_one_input, Path(source).read_bytes())
    lines = {f'{Path(filename).resolve()}:{line}'
             for (filename, line), hits in tracer.results().counts.items()
             if hits > 0 and str(Path(filename).resolve()).startswith(prefix)}
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
            raise SystemExit('no pyquery source lines executed')
        subprocess.run(['llvm-profdata', 'merge', str(root / 'case.profraw'),
                        '-o', str(root / 'case.profdata')], check=True,
                       stdout=subprocess.DEVNULL)
        result = subprocess.run(['llvm-cov', 'export', modules[0],
                                 f'-instr-profile={root / "case.profdata"}'],
                                check=True, capture_output=True, text=True)
    native = set()
    # parser.c:8700-8720 is the address-sensitive attribute hash lookup excluded
    # by the lxml overlay; its line path varied across identical valid replays.
    for file in json.loads(result.stdout)['data'][0]['files']:
        if not file['filename'].startswith(NATIVE_PREFIX):
            continue
        for line, column, count, has_count, region_start, *_ in file['segments']:
            if has_count and region_start and count > 0 and not 8700 <= line <= 8720:
                native.add(f'{file["filename"]}:{line}')
    if not native:
        raise SystemExit('no native parser source regions covered')
    Path(sys.argv[2]).write_text('\n'.join(sorted(features | native)) + '\n')


if __name__ == '__main__':
    main()
