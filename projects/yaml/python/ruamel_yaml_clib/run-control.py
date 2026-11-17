"""Replay the valid YAML control through ruamel.yaml YAML(typ='safe') with the ruamel.yaml.clib CParser and check the typed tree."""
import json
from pathlib import Path

from harness import parse_yaml

observed = parse_yaml(Path('/input/control').read_bytes())
expected = json.loads(Path('/work/expected.json').read_text(encoding='utf-8'))
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n')
