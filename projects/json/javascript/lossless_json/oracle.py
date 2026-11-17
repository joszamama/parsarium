"""Independent Python JSON oracle that retains each numeric source lexeme."""

import json
import sys


class NumberToken(str):
    """A JSON number spelling, kept distinct from a decoded JSON string."""


def summarize(data: bytes) -> dict:
    value = json.loads(data.decode("utf-8"), parse_int=NumberToken,
                       parse_float=NumberToken,
                       parse_constant=lambda token: (_ for _ in ()).throw(
                           ValueError(f"non-JSON numeric constant: {token}")))

    def tag(item):
        if isinstance(item, NumberToken):
            return {"type": "LosslessNumber", "raw": str(item)}
        if item is None:
            return {"type": "null"}
        if isinstance(item, bool):
            return {"type": "boolean", "value": item}
        if isinstance(item, str):
            return {"type": "string", "value": item}
        if isinstance(item, list):
            return {"type": "array", "items": [tag(child) for child in item]}
        if isinstance(item, dict):
            return {"type": "object", "members": {
                key: tag(item[key]) for key in sorted(item)}}
        raise TypeError(f"unexpected decoded type {type(item)}")

    return tag(value)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, "rb") as source:
            print(json.dumps(summarize(source.read()), ensure_ascii=False, sort_keys=True))
