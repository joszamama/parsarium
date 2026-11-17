"""ryaml 0.5.1: serde_yaml 0.9.34 over unsafe-libyaml 0.2.11 (Rust) through the PyO3 _ryaml extension, over local YAML bytes; reports the typed YAML tree."""

import hashlib
import io
import json

import ryaml

# ryaml.loads(str) runs serde_yaml::from_str into a serde_yaml::Value (unsafe-libyaml
# scanner/parser, serde_yaml loader with alias expansion and YAML 1.2 core-schema scalar
# resolution) and converts it with pythonize; ryaml.load(fp) reads a local file object
# and decodes bytes as UTF-8 before the same loads. The binding has no bytes API, so the
# bytes mode decodes strict UTF-8 first.


def load(data, mode='bytes'):
    if mode == 'bytes':
        return ryaml.loads(data.decode('utf-8'))
    if mode == 'str':
        return ryaml.loads(data.decode('utf-8'))
    if mode == 'stream':
        return ryaml.load(io.BytesIO(data))
    raise ValueError(mode)


ERRORS = (ryaml.InvalidYamlError, UnicodeError, ValueError, TypeError, RecursionError, OverflowError)


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
