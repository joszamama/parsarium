"""rapidyaml (ryml) 0.15.2 Python binding: the C++ rapidyaml parse engine through the SWIG _ryml extension, over local YAML bytes; reports the typed YAML tree."""

import hashlib
import io
import json
import math
import re

import ryml

assert ryml.__version__ == '0.15.2'

# ryml.parse_in_arena copies the buffer into the tree's arena and runs the C++ parse
# engine (parse_engine.def.hpp) with the tree event handler; Tree.resolve() expands
# aliases into copies of the anchored nodes. The tree keeps every scalar as text plus
# style flags (plain, single/double quoted, literal, folded) and marks plain nulls
# (val_is_null). ryml has no YAML 1.2 core-schema typing of its own, so this adapter
# types unquoted, non-null scalars with the YAML 1.2 core-schema patterns (the same
# patterns as the C++ rapidyaml harness) and converts them with Python int/float.
# The controls avoid every scalar whose type differs between YAML 1.1 and 1.2 core.
BOOL = re.compile(r'true|True|TRUE|false|False|FALSE')
INT = re.compile(r'[-+]?[0-9]+')
FLOAT = re.compile(r'[-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)?')


class RymlRejected(ValueError):
    pass


def text(view) -> str:
    return bytes(view).decode('utf-8')


def scalar(tree, node):
    if not tree.has_val(node) or tree.has_val_tag(node):
        raise RymlRejected('tagged or valueless scalar')
    value = text(tree.val(node))
    if tree.is_val_quoted(node):  # single/double quoted, literal or folded
        return ['str', value]
    if tree.val_is_null(node):
        return ['null']
    if BOOL.fullmatch(value):
        return ['bool', value[0] in 'tT']
    if INT.fullmatch(value):
        return ['int', str(int(value))]
    if FLOAT.fullmatch(value):
        number = float(value)
        if not math.isfinite(number):
            raise RymlRejected('non-finite float')
        return ['float', repr(number)]
    return ['str', value]


def typed(tree, node, depth=0):
    if depth > 64:
        raise RymlRejected('nesting limit')
    if tree.is_map(node) or tree.is_seq(node):
        if tree.has_val_tag(node):
            raise RymlRejected('tagged collection')
        is_map = tree.is_map(node)
        items = []
        for child in ryml.children(tree, node):
            if is_map:
                if tree.has_key_tag(child):
                    raise RymlRejected('tagged key')
                items.append([text(tree.key(child)), typed(tree, child, depth + 1)])
            else:
                items.append(typed(tree, child, depth + 1))
        return ['map' if is_map else 'seq', items]
    return scalar(tree, node)


def load(data, mode='bytes'):
    if mode == 'bytes':
        source = data
    elif mode == 'str':
        source = data.decode('utf-8')
    elif mode == 'stream':
        source = io.BytesIO(data).read()
    else:
        raise ValueError(mode)
    # Documented API (rapidyaml-python README): tree = ryml.parse_in_arena(buf) for
    # bytes, bytearray or str; then Tree.resolve() for anchors and aliases.
    tree = ryml.parse_in_arena(source)
    tree.resolve()
    root = tree.root_id()
    if tree.is_stream(root):
        if tree.num_children(root) != 1:
            raise RymlRejected('not exactly one document')
        root = tree.first_child(root)
    return typed(tree, root)


ERRORS = (RymlRejected, RuntimeError, UnicodeError, ValueError, TypeError, RecursionError, OverflowError)


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
    text_ = json.dumps(tree, ensure_ascii=False, separators=(',', ':')).encode()
    return {'root': tree[0], 'nodes': dict(sorted(counts.items())), 'max_depth': depth,
            'tree_sha256': hashlib.sha256(text_).hexdigest(), 'tree': tree}


def parse_yaml(data: bytes, mode: str = 'bytes'):
    if not data or len(data) > (1 << 20):
        raise ValueError('input outside harness limit')
    return summarize(load(data, mode))


def fuzz_one_input(data: bytes):
    try:
        parse_yaml(data)
    except ERRORS:
        pass
