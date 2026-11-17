"""srsly.yaml_loads over local YAML text: srsly's CustomYaml wraps ruamel.yaml YAML(typ='safe', pure=True); reports the typed YAML tree."""

import hashlib
import io
import json

import srsly
import srsly._yaml_api
import ruamel.yaml.parser

# srsly.yaml_loads(data) builds srsly._yaml_api.CustomYaml(), a ruamel.yaml YAML
# subclass whose defaults are typ='safe', pure=True: the pure-Python ruamel.yaml
# Reader/Scanner/Parser/Composer, SafeConstructor and YAML 1.2 VersionedResolver.
assert srsly._yaml_api.CustomYaml().Parser is ruamel.yaml.parser.Parser


def load(data, mode='bytes'):
    # The documented input is str or a file-like object; srsly passes the value
    # unchanged to ruamel.yaml's YAML.load, which also takes bytes.
    if mode == 'bytes':
        return srsly.yaml_loads(data)
    if mode == 'str':
        return srsly.yaml_loads(data.decode('utf-8'))
    if mode == 'stream':
        return srsly.yaml_loads(io.BytesIO(data))
    raise ValueError(mode)


from ruamel.yaml.error import YAMLError, MarkedYAMLError  # noqa: E402

ERRORS = (YAMLError, MarkedYAMLError, UnicodeError, ValueError, TypeError, AttributeError,
          KeyError, IndexError, AssertionError, RecursionError, OverflowError)


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


def parse_yaml(data: bytes, mode: str = 'str'):
    if not data or len(data) > (1 << 20):
        raise ValueError('input outside harness limit')
    return summarize(tagged(load(data, mode)))


def fuzz_one_input(data: bytes):
    try:
        parse_yaml(data)
    except ERRORS:
        pass
