"""Replay the valid PLY control through the pinned OpenMesh Python binding."""
import json
from pathlib import Path
from harness import parse_data

config = json.loads(Path('/work/target.json').read_text())
observed = parse_data(Path('/input/control').read_bytes())
if observed != config['expected_output']:
    raise SystemExit(f"control mismatch: {observed}")
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2) + '\n')
print(json.dumps({'control_pass': True, 'output': observed}))
