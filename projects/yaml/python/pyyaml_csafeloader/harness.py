"""PyYAML yaml.CSafeLoader: libyaml 0.2.5 (scanner/parser through PyYAML's _yaml C extension) with SafeConstructor and the YAML 1.1 Resolver, over local YAML bytes; reports the typed YAML tree."""

import hashlib
import io
import json

import yaml
from yaml import _yaml

# The libyaml route: _yaml.CParser drives libyaml's yaml_parser_parse (reader.c,
# scanner.c, parser.c) and composes nodes in the C extension; only SafeConstructor
# and the Resolver stay in Python. The pure-Python yaml.SafeLoader is a separate path.
LOADER = yaml.CSafeLoader
assert yaml.__with_libyaml__ and issubclass(LOADER, _yaml.CParser)
assert _yaml.get_version_string() == '0.2.5'


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
