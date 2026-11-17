"""Parse one complete local JSON byte stream with simplejson."""

from io import BytesIO

import simplejson


def parse_json(data: bytes):
    if len(data) > (1 << 20):
        return None
    value = simplejson.load(BytesIO(data), allow_nan=False)
    if not isinstance(value, dict):
        return {"root_type": type(value).__name__}
    result = {"root_type": "object", "top_level_keys": sorted(value)}
    items = value.get("items")
    if isinstance(items, list):
        result["item_count"] = len(items)
        if items and isinstance(items[0], dict):
            first = items[0]
            result["first_id"] = first.get("id")
            result["first_label"] = first.get("label")
            result["first_ok"] = first.get("ok")
            result["first_value_is_null"] = first.get("value") is None
        if len(items) > 1 and isinstance(items[1], dict):
            result["second_label"] = items[1].get("label")
    return result


def fuzz_one_input(data: bytes):
    try:
        parse_json(data)
    except (simplejson.JSONDecodeError, UnicodeDecodeError, OverflowError):
        pass
