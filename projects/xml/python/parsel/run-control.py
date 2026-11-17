"""Replay a valid control; check it against the expat oracle; export Parsel lines plus libxml2 parser.c coverage."""

import json
import os
from pathlib import Path
import subprocess
import sys
import trace

CONFIG = json.loads(Path('/work/target.json').read_text())
OUT = Path('/coverage')


def child():
    from lxml import etree
    from parsel import Selector
    from parsel.selector import SafeXMLParser, _ctgroup
    from harness import parse_xml
    from oracle import summarize

    probe = Selector(body=b'<r/>', type='xml')
    if (probe.type != 'xml' or not isinstance(probe.root, etree._Element)
            or _ctgroup['xml']['_parser'] is not SafeXMLParser):
        raise SystemExit('Selector(body=..., type="xml") is not SafeXMLParser over lxml.etree')
    data = Path('/input/control').read_bytes()
    tracer = trace.Trace(count=True, trace=False)
    observed = tracer.runfunc(parse_xml, data)
    expected_key = 'differential_expected_output' if '--differential' in sys.argv else 'expected_output'
    if observed != CONFIG[expected_key]:
        raise SystemExit(f'control mismatch: {observed!r}')
    if summarize(data) != observed:
        raise SystemExit(f'expat oracle disagrees: {summarize(data)!r}')
    covered = {}
    for (filename, line), hits in tracer.results().counts.items():
        source = str(Path(filename).resolve())
        if hits > 0 and source.startswith(CONFIG['trace_subject_prefix']):
            covered.setdefault(source, set()).add(line)
    files = [{'filename': source, 'summary': {'lines': {'covered': len(lines)}},
              'executed_lines': sorted(lines)}
             for source, lines in sorted(covered.items())]
    if not any(f['filename'].endswith(CONFIG['trace_selector_suffix']) for f in files):
        raise SystemExit('no parsel/selector.py lines covered')
    OUT.mkdir(exist_ok=True)
    (OUT / 'observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n')
    (OUT / 'python-files.json').write_text(json.dumps(files, indent=2) + '\n')


def parent():
    OUT.mkdir(exist_ok=True)
    env = {**os.environ, 'LLVM_PROFILE_FILE': str(OUT / 'control.profraw')}
    child_args = [sys.executable, '/work/run-control.py', '--child']
    if '--differential' in sys.argv:
        child_args.append('--differential')
    subprocess.run(child_args, env=env, check=True)
    subprocess.run(['llvm-profdata', 'merge', str(OUT / 'control.profraw'), '-o', str(OUT / 'control.profdata')], check=True)
    result = subprocess.run(['llvm-cov', 'export', CONFIG['native_module'], f'-instr-profile={OUT / "control.profdata"}'],
                            capture_output=True, text=True, check=True)
    native = [f for f in json.loads(result.stdout)['data'][0]['files'] if f['filename'].startswith(CONFIG['native_subject_prefix'])]
    if not any(f['filename'].endswith('/parser.c') and f['summary']['lines']['covered'] > 0 for f in native):
        raise SystemExit('no libxml2 parser.c source lines covered')
    python_files = json.loads((OUT / 'python-files.json').read_text())
    observed = json.loads((OUT / 'observed.json').read_text())
    (OUT / 'coverage.json').write_text(json.dumps({'data': [{'files': python_files + native}]}, indent=2) + '\n')
    summary = {'control_pass': True, 'output': observed,
               'parser_source_files': len(python_files),
               'parser_source_lines_covered': sum(f['summary']['lines']['covered'] for f in python_files),
               'underlying_source_files': len(native),
               'underlying_source_lines_covered': sum(f['summary']['lines']['covered'] for f in native),
               'coverage': '/coverage/coverage.json'}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    child() if '--child' in sys.argv else parent()
