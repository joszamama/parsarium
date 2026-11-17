"""Exercise CPython json.load with its pinned pure-Python scanner."""

from io import BytesIO
import json
import json.decoder
import json.scanner


class PurePythonJSONDecoder(json.JSONDecoder):
    """Select CPython's parser source instead of its built-in _json accelerator."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parse_string = json.decoder.py_scanstring
        self.scan_once = json.scanner.py_make_scanner(self)


def reject_nonfinite(value):
    raise ValueError(f"non-RFC-8259 numeric token: {value}")


def parse_json(data: bytes):
    if len(data) > (1 << 20):
        return None
    value = json.load(BytesIO(data), cls=PurePythonJSONDecoder,
                      parse_constant=reject_nonfinite)
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
    except (json.JSONDecodeError, UnicodeError, ValueError, RecursionError, OverflowError):
        pass
