"""Replay the nested-object control through jiter.from_json(bytes) and check the summary."""
import json
from pathlib import Path
from harness import parse_json

observed = parse_json(Path('/input/control').read_bytes())
# Written from the control text, not from parser output.
expected = {
    'root_type': 'object', 'root_length': 7,
    'top_level_keys': ['name', 'version', 'ratio', 'enabled', 'missing', 'tags', 'nested'],
    'kind_counts': {'object': 5, 'array': 3, 'string': 5, 'int': 4, 'float': 1, 'bool': 2, 'null': 1},
    'object_members': 15, 'max_container_depth': 4,
    'scalar_leaves': [['/name', 'string', 'parsarium'], ['/version', 'int', 1],
                      ['/ratio', 'float', '-2.5'], ['/enabled', 'bool', True],
                      ['/missing', 'null', None], ['/tags/0', 'string', 'json'],
                      ['/tags/1', 'string', 'go'], ['/tags/2', 'string', 'rfc8259'],
                      ['/nested/level', 'int', 2], ['/nested/items/0/id', 'int', 1],
                      ['/nested/items/0/ok', 'bool', False], ['/nested/items/1/id', 'int', 2],
                      ['/nested/items/1/text', 'string', 'café "quoted"']],
    'empty_containers': [['/nested/empty', 'object'], ['/nested/list', 'array']],
}
if observed != expected:
    raise SystemExit(f'control mismatch: {observed}')
Path('/coverage/observed.json').write_text(json.dumps(observed, indent=2, ensure_ascii=False) + '\n')
