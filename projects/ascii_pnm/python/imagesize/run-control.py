"""Verify the valid control and record parser-source line coverage."""
import json
from pathlib import Path
import trace
from harness import parse_pnm

config = json.loads(Path('/work/target.json').read_text())
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(parse_pnm, Path('/input/control').read_bytes())
if observed != config['expected_output']:
    raise SystemExit(f"control mismatch: {observed}")
prefix = config['coverage_subject_prefix']
covered = {}
for (filename, line), count in tracer.results().counts.items():
    if count > 0 and str(Path(filename).resolve()).startswith(prefix):
        covered.setdefault(str(Path(filename).resolve()), set()).add(line)
if not covered:
    raise SystemExit('no parser package source lines covered')
files = [{'filename': filename,
          'summary': {'lines': {'covered': len(lines)}},
          'executed_lines': sorted(lines)}
         for filename, lines in sorted(covered.items())]
output = Path('/coverage')
output.mkdir(exist_ok=True)
(output / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')
(output / 'coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(files),
           'parser_source_lines_covered': sum(len(lines) for lines in covered.values()),
           'coverage': '/coverage/coverage.json'}
(output / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
