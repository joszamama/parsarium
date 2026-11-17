# orjson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.13.0`
- **License:** MPL-2.0 AND (Apache-2.0 OR MIT)
- **Parser family:** orjson Rust deserializer backed by vendored yyjson 0.12.0 C parser
- **Local input API:** `orjson.loads(local UTF-8 bytes)`
- **Documentation:** [API reference](<https://github.com/ijl/orjson/blob/3.13.0/README.md#deserialize>)
- **Valid control:** [`controls/json/structure.json`](../../../../controls/json/structure.json)
- **Catalog evidence:** [parser record](../../../../data/python/json/parsers.json) · [control result](../../../../data/python/json/verification.json)

## Observed control result

```json
{
  "root_type": "object",
  "top_level_keys": [
    "items",
    "kind"
  ],
  "item_count": 2,
  "first_id": 7,
  "first_label": "a\nb",
  "first_ok": true,
  "first_value_is_null": true,
  "second_label": "π"
}
```

## Run this target

```sh
python3 parsarium.py build json python orjson
python3 parsarium.py run json python orjson controls/json/structure.json
```
