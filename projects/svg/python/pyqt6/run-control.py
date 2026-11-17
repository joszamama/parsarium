"""Replay a valid control and export instrumented QtSvg source coverage."""

import json
import os
from pathlib import Path
import subprocess
import sys

from harness import parse_svg

CONFIG = json.loads(Path('/work/target.json').read_text())
OUT = Path('/coverage')


def child():
    observed = parse_svg(Path('/input/control').read_bytes())
    if observed != CONFIG['expected_output']:
        raise SystemExit(f'control mismatch: {observed!r}')
    OUT.mkdir(exist_ok=True)
    (OUT / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')


def parent():
    OUT.mkdir(exist_ok=True)
    env = {**os.environ, 'LLVM_PROFILE_FILE': str(OUT / 'control.profraw')}
    subprocess.run([sys.executable, '/work/run-control.py', '--child'], env=env, check=True)
    subprocess.run(['llvm-profdata', 'merge', str(OUT / 'control.profraw'), '-o', str(OUT / 'control.profdata')], check=True)
    result = subprocess.run(['llvm-cov', 'export', CONFIG['native_module'], f'-instr-profile={OUT / "control.profdata"}'], capture_output=True, text=True, check=True)
    files = [f for f in json.loads(result.stdout)['data'][0]['files'] if f['filename'].startswith(CONFIG['native_subject_prefix'])]
    if not any(f['filename'].endswith(CONFIG['format_specific_suffix']) and f['summary']['lines']['covered'] > 0 for f in files):
        raise SystemExit('no QtSvg qsvghandler.cpp source lines covered')
    observed = json.loads((OUT / 'observed.json').read_text())
    (OUT / 'coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
    summary = {'control_pass': True, 'output': observed,
               'parser_source_files': len(files),
               'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in files),
               'coverage': '/coverage/coverage.json'}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    child() if '--child' in sys.argv else parent()
