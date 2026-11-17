"""Standalone jiter package: jiter.from_json over local JSON bytes (Jiter Rust parser)."""

import jiter

KINDS = ('object', 'array', 'string', 'int', 'float', 'bool', 'null')


def kind_of(value) -> str:
    # bool before int: bool is an int subclass.
    if isinstance(value, bool):
        return 'bool'
    if value is None:
        return 'null'
    for kind, types in (('int', int), ('float', float), ('string', str), ('array', list), ('object', dict)):
        if isinstance(value, types):
            return kind
    raise TypeError(type(value).__name__)


def pointer(path: str, token) -> str:
    return f"{path}/{str(token).replace('~', '~0').replace('/', '~1')}"


def summarize(value) -> dict:
    """Decoded tree as type counts, document-order scalar leaves and empty containers."""
    counts = dict.fromkeys(KINDS, 0)
    leaves, empty = [], []
    state = {'members': 0, 'depth': 0}

    def walk(node, path: str, depth: int) -> None:
        kind = kind_of(node)
        counts[kind] += 1
        if kind in ('object', 'array'):
            state['depth'] = max(state['depth'], depth + 1)
            pairs = list(node.items()) if kind == 'object' else list(enumerate(node))
            state['members'] += len(pairs) if kind == 'object' else 0
            if not pairs:
                empty.append([path, kind])
            for token, child in pairs:
                walk(child, pointer(path, token), depth + 1)
        else:
            leaves.append([path, kind, repr(node) if kind == 'float' else node])

    walk(value, '', 0)
    result = {'root_type': kind_of(value)}
    if isinstance(value, (dict, list)):
        result['root_length'] = len(value)
    if isinstance(value, dict):
        result['top_level_keys'] = list(value)
    result.update({'kind_counts': counts, 'object_members': state['members'],
                   'max_container_depth': state['depth'], 'scalar_leaves': leaves,
                   'empty_containers': empty})
    return result


def parse_json(data: bytes):
    if not data or len(data) > (1 << 20):
        raise ValueError('input outside harness limit')
    return summarize(jiter.from_json(data))


def fuzz_one_input(data: bytes):
    try:
        parse_json(data)
    except (ValueError, UnicodeError, OverflowError, RecursionError):
        pass
