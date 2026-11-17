"""Replay a valid control and export instrumented libxml2 source coverage."""

import json
import os
from pathlib import Path
import subprocess
import sys

from harness import parse_xml

CONFIG = json.loads(Path('/work/target.json').read_text())
OUT = Path('/coverage')


def child():
    observed = parse_xml(Path('/input/control').read_bytes())
    expected_key = 'differential_expected_output' if '--differential' in sys.argv else 'expected_output'
    if observed != CONFIG[expected_key]:
        raise SystemExit(f'control mismatch: {observed!r}')
    OUT.mkdir(exist_ok=True)
    (OUT / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')


def parent():
    OUT.mkdir(exist_ok=True)
    env = {**os.environ, 'LLVM_PROFILE_FILE': str(OUT / 'control.profraw')}
    child_args = [sys.executable, '/work/run-control.py', '--child']
    if '--differential' in sys.argv:
        child_args.append('--differential')
    subprocess.run(child_args, env=env, check=True)
    subprocess.run(['llvm-profdata', 'merge', str(OUT / 'control.profraw'), '-o', str(OUT / 'control.profdata')], check=True)
    result = subprocess.run(['llvm-cov', 'export', CONFIG['native_module'], f'-instr-profile={OUT / "control.profdata"}'], capture_output=True, text=True, check=True)
    files = [f for f in json.loads(result.stdout)['data'][0]['files'] if f['filename'].startswith(CONFIG['native_subject_prefix'])]
    if not any(f['filename'].endswith('/parser.c') and f['summary']['lines']['covered'] > 0 for f in files):
        raise SystemExit('no libxml2 parser.c source lines covered')
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
