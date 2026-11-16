"""Verify the valid control and record parser-source line coverage."""
import json
from pathlib import Path
import trace
from harness import parse_data

config = json.loads(Path('/work/target.json').read_text())
tracer = trace.Trace(count=True, trace=False)
observed = tracer.runfunc(parse_data, Path('/input/control').read_bytes())
if observed != config['expected_output']:
    raise SystemExit(f"control mismatch: {observed}")
prefix = config['coverage_subject_prefix']
underlying_prefix = config['underlying_coverage_subject_prefix']
covered = {}
underlying_covered = {}
for (filename, line), count in tracer.results().counts.items():
    if count <= 0:
        continue
    source = str(Path(filename).resolve())
    if source.startswith(prefix):
        covered.setdefault(source, set()).add(line)
    if source.startswith(underlying_prefix):
        underlying_covered.setdefault(source, set()).add(line)
if not covered or not underlying_covered:
    raise SystemExit('SimpleAudio or underlying wave parser source not covered')
files = [{'filename': filename,
          'summary': {'lines': {'covered': len(lines)}},
          'executed_lines': sorted(lines)}
         for filename, lines in sorted({**covered, **underlying_covered}.items())]
output = Path('/coverage')
output.mkdir(exist_ok=True)
(output / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')
(output / 'coverage.json').write_text(json.dumps({'data': [{'files': files}]}, indent=2) + '\n')
summary = {'control_pass': True, 'output': observed,
           'parser_source_files': len(covered),
           'parser_source_lines_covered': sum(len(lines) for lines in covered.values()),
           'underlying_source_files': len(underlying_covered),
           'underlying_source_lines_covered': sum(len(lines) for lines in underlying_covered.values()),
           'coverage': '/coverage/coverage.json'}
(output / 'summary.json').write_text(json.dumps(summary) + '\n')
print(json.dumps(summary))
