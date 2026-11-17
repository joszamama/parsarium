"""yaml-rs 0.1.6: granit-parser events and yaml-rs's own Rust loader through the PyO3 _yaml_rs extension, over local YAML bytes; reports the typed YAML tree."""

import hashlib
import io
import json

import yaml_rs

assert yaml_rs.__version__ == '0.1.6'

# yaml_rs.load(bytes | binary file) and yaml_rs.loads(str) decode the input, run the
# granit-parser event parser (saphyr-parser lineage) and build Python values with
# yaml-rs's own Rust loader (src/load/loads.rs: aliases, YAML 1.2 core-schema scalar
# resolution in scalar.rs). parse_datetime stays at its default; the controls hold no
# timestamps. yaml_rs.load(str) would treat the string as a file path, so str input
# goes through loads.


def load(data, mode='bytes'):
    if mode == 'bytes':
        return yaml_rs.load(data)
    if mode == 'str':
        return yaml_rs.loads(data.decode('utf-8'))
    if mode == 'stream':
        return yaml_rs.load(io.BytesIO(data))
    raise ValueError(mode)


ERRORS = (yaml_rs.YAMLDecodeError, UnicodeError, ValueError, TypeError, RecursionError, OverflowError)


def tagged(value):
    """Typed tree shared by every YAML harness; bool before int (bool is an int subclass)."""
    if isinstance(value, bool):
        return ['bool', value]
    if value is None:
        return ['null']
    if isinstance(value, int):
        return ['int', str(value)]
    if isinstance(value, float):
        return ['float', repr(value)]
    if isinstance(value, str):
        return ['str', value]
    if isinstance(value, list):
        return ['seq', [tagged(item) for item in value]]
    if isinstance(value, dict):
        for key in value:
            if not isinstance(key, str):
                raise TypeError('non-string mapping key')
        return ['map', [[key, tagged(item)] for key, item in value.items()]]
    raise TypeError(type(value).__name__)


def summarize(tree):
    counts = {}

    def visit(node, depth):
        counts[node[0]] = counts.get(node[0], 0) + 1
        if node[0] == 'map':
            return max([depth] + [visit(value, depth + 1) for _, value in node[1]])
        if node[0] == 'seq':
            return max([depth] + [visit(value, depth + 1) for value in node[1]])
        return depth - 1

    depth = visit(tree, 1)
    text = json.dumps(tree, ensure_ascii=False, separators=(',', ':')).encode()
    return {'root': tree[0], 'nodes': dict(sorted(counts.items())), 'max_depth': depth,
            'tree_sha256': hashlib.sha256(text).hexdigest(), 'tree': tree}


def parse_yaml(data: bytes, mode: str = 'bytes'):
    if not data or len(data) > (1 << 20):
        raise ValueError('input outside harness limit')
    return summarize(tagged(load(data, mode)))


def fuzz_one_input(data: bytes):
    try:
        parse_yaml(data)
    except ERRORS:
        pass
