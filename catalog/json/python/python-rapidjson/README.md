# python-rapidjson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.26`
- **License:** MIT
- **Parser family:** Tencent RapidJSON C++ SAX Reader (vendored v1.1.0-763-g24b5e7a8) / python-rapidjson PyHandler wrapper
- **Local input API:** `rapidjson.load(io.BytesIO(local JSON bytes)); rapidjson.loads(bytes) and rapidjson.loads(decoded str) give the same exact tree on both controls`
- **Documentation:** [API reference](<https://python-rapidjson.readthedocs.io/en/latest/load.html>)
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
