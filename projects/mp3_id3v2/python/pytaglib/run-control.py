"""Replay the valid mp3_id3v2 through the installed pytaglib extension."""
import json
from pathlib import Path
from harness import parse_data

expected = json.loads(Path('/work/target.json').read_text())['expected_output']
observed = parse_data(Path('/input/control').read_bytes())
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
output = Path('/coverage')
(output / 'observed.json').write_text(json.dumps(observed, indent=2) + '\n')
(output / 'coverage.json').write_text(json.dumps({'data': [{'files': []}]}) + '\n')
(output / 'summary.json').write_text(json.dumps({
    'control_pass': True, 'output': observed,
    'parser_source_files': 0, 'parser_source_lines_covered': 0,
    'coverage': '/coverage/coverage.json'}) + '\n')
