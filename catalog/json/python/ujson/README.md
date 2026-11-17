# ujson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `6.1.0`
- **License:** BSD-3-Clause AND TCL
- **Parser family:** UltraJSON C decoder (ujson decode.c) / vendored double-conversion 3.2.0 C++ string-to-double
- **Local input API:** `ujson.loads(local JSON bytes); ujson.loads(decoded str) gives the same exact tree on both controls`
- **Documentation:** [API reference](<https://github.com/ultrajson/ultrajson/blob/6.1.0/README.md#usage>)
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
python3 parsarium.py build json python ujson
python3 parsarium.py run json python ujson controls/json/structure.json
```
