"""Replay the first valid JSON control through orjson.loads(local bytes)."""
import json
from pathlib import Path
from harness import parse_json

observed = parse_json(Path('/input/control').read_bytes())
expected = {"root_type": "object", "top_level_keys": ["items", "kind"],
            "item_count": 2, "first_id": 7, "first_label": "a\nb",
            "first_ok": True, "first_value_is_null": True, "second_label": "π"}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n')
