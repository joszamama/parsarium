"""json5 (dpranke/pyjson5) pure-Python parser over local JSON bytes through json5.loads."""

import json5


def parse_json(data: bytes):
    if not data or len(data) > (1 << 20):
        raise ValueError('input outside harness limit')
    value = json5.loads(data)
    if isinstance(value, dict):
        result = {'root_type': 'object', 'top_level_keys': sorted(value)}
        items = value.get('items')
        if isinstance(items, list):
            result['item_count'] = len(items)
            if items and isinstance(items[0], dict):
                first = items[0]
                result['first_id'] = first.get('id')
                result['first_label'] = first.get('label')
                result['first_ok'] = first.get('ok')
                result['first_value_is_null'] = first.get('value') is None
            if len(items) > 1 and isinstance(items[1], dict):
                result['second_label'] = items[1].get('label')
        return result
    if isinstance(value, list):
        return {'root_type': 'array', 'item_count': len(value),
                'nested_arrays': sum(isinstance(x, list) for x in value),
                'nested_objects': sum(isinstance(x, dict) for x in value)}
    return {'root_type': type(value).__name__}


def fuzz_one_input(data: bytes):
    try:
        parse_json(data)
    except (ValueError, UnicodeError, OverflowError, RecursionError):
        pass
