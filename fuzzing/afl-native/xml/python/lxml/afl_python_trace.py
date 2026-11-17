"""Map executed libxml2 parser source lines to AFL++ features."""

import glob
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == '--case':
        from harness import fuzz_one_input
        fuzz_one_input(Path(sys.argv[2]).read_bytes())
        return
    if len(sys.argv) != 3:
        raise SystemExit(2)
    modules = glob.glob(os.environ['PARSARIUM_LLVM_MODULE_GLOB'])
    if len(modules) != 1:
        raise SystemExit(f'expected one native module, found {modules}')
    with tempfile.TemporaryDirectory(prefix='parsarium-llvm-') as temporary:
        root = Path(temporary)
        environment = {**os.environ, 'LLVM_PROFILE_FILE': str(root / 'case.profraw')}
        subprocess.run([sys.executable, __file__, '--case', sys.argv[1]],
                       env=environment, check=True, stdout=subprocess.DEVNULL)
        subprocess.run(['llvm-profdata', 'merge', str(root / 'case.profraw'),
                        '-o', str(root / 'case.profdata')], check=True,
                       stdout=subprocess.DEVNULL)
        result = subprocess.run(['llvm-cov', 'export', modules[0],
                                 f'-instr-profile={root / "case.profdata"}'],
                                check=True, capture_output=True, text=True)
    coverage = json.loads(result.stdout)
    prefix = os.environ['PARSARIUM_SUBJECT_PREFIX']
    # parser.c:8700-8720 is an address-sensitive attribute hash lookup;
    # its line path varied across identical valid-control replays.
    features = set()
    for file in coverage['data'][0]['files']:
        filename = file['filename']
        if not filename.startswith(prefix):
            continue
        for line, column, count, has_count, region_start, *_ in file['segments']:
            if has_count and region_start and count > 0 and not 8700 <= line <= 8720:
                features.add(f'{filename}:{line}')
    if not features:
        raise SystemExit('no native parser source regions covered')
    Path(sys.argv[2]).write_text('\n'.join(sorted(features)) + '\n')


if __name__ == '__main__':
    main()
