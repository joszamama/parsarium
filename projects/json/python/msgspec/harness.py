"""msgspec.json.decode over local JSON bytes with the default Any type."""

import msgspec


def describe(value):
    """Type-tagged tree of the decoded value, keeping key order and number kinds."""
    kind = type(value)
    if kind is dict:
        return ['object', [[key, describe(item)] for key, item in value.items()]]
    if kind is list:
        return ['array', [describe(item) for item in value]]
    if kind is str:
        return ['string', value]
    if kind is bool:
        return ['bool', value]
    if kind is int:
        return ['int', value]
    if kind is float:
        return ['float', repr(value)]
    if value is None:
        return ['null']
    raise TypeError(f'unexpected decoded type {kind.__name__}')


def parse_json(data: bytes):
    if not data or len(data) > (1 << 20):
        raise ValueError('input outside harness limit')
    return {'value': describe(msgspec.json.decode(data))}


def fuzz_one_input(data: bytes):
    try:
        parse_json(data)
    except (msgspec.DecodeError, ValueError, UnicodeError, OverflowError, RecursionError):
        pass
