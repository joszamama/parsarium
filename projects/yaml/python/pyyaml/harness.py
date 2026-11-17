"""PyYAML pure-Python SafeLoader (yaml/reader.py, scanner.py, parser.py, composer.py, SafeConstructor, resolver.py) over local YAML bytes; reports the typed YAML tree."""

import hashlib
import io
import json

import yaml

# The pure-Python loader: Reader, Scanner, Parser, Composer, SafeConstructor and
# Resolver from yaml/*.py. yaml.CSafeLoader (libyaml through the _yaml C
# extension) is a separate path and is never used here.
LOADER = yaml.SafeLoader
assert LOADER.__module__ == 'yaml.loader' and not issubclass(LOADER, yaml.CSafeLoader if hasattr(yaml, 'CSafeLoader') else ())


def load(data, mode='bytes'):
    if mode == 'bytes':
        source = data
    elif mode == 'str':
        source = data.decode('utf-8')
    elif mode == 'stream':
        source = io.BytesIO(data)
    else:
        raise ValueError(mode)
    return yaml.load(source, Loader=LOADER)


ERRORS = (yaml.YAMLError, UnicodeError, ValueError, TypeError, RecursionError, OverflowError)


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
