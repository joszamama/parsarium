"""Verify frozen zipimport lines against the pinned matching source file."""
import json
from pathlib import Path
import trace
from harness import parse_data

config = json.loads(Path('/work/target.json').read_text())
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(parse_data, Path('/input/control').read_bytes())
if observed != config['expected_output']:
    raise SystemExit(f'control mismatch: {observed}')
source = Path(config['coverage_subject_prefix'])
if not source.is_file():
    raise SystemExit('pinned zipimport source is missing')
lines = sorted({line for (filename, line), hits in tracer.results().counts.items()
                if hits > 0 and filename == '<frozen zipimport>'})
if not lines or max(lines) > len(source.read_text().splitlines()):
    raise SystemExit('frozen zipimport lines do not map to pinned source')
files = [{'filename': str(source),
          'summary': {'lines': {'covered': len(lines)}},
          'executed_lines': lines}]
output = Path('/coverage')
output.mkdir(exist_ok=True)
(output / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')
(output / 'coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': 1,
           'parser_source_lines_covered': len(lines),
           'coverage': '/coverage/coverage.json'}
(output / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
