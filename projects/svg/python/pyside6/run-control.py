"""Check the valid SVG control without claiming native QtSvg line coverage."""
import json
from pathlib import Path
from harness import parse_data

config = json.loads(Path('/work/target.json').read_text())
observed = parse_data(Path('/input/control').read_bytes())
if observed != config['expected_output']:
    raise SystemExit(f'control mismatch: {observed}')
output = Path('/coverage')
output.mkdir(exist_ok=True)
(output / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')
summary = {'control_pass': True, 'output': observed,
           'parser_source_lines_covered': None,
           'parser_feedback_available': False}
(output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary))
