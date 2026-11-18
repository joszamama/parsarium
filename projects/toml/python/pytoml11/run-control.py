"""Replay the service-config TOML control through pytoml11.loads and check the hand-written typed tree."""
import json
from pathlib import Path

from harness import parse_toml

observed = parse_toml(Path("/input/control").read_bytes())
expected = json.loads(Path("/work/expected/service-config.expected.json").read_text(encoding="utf-8"))
if observed != expected:
    raise SystemExit(f"control mismatch: {json.dumps(observed, ensure_ascii=False, sort_keys=True)}")
Path("/coverage/observed.json").write_text(
    json.dumps(observed, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
