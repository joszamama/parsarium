# dirtyjson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.8`
- **License:** MIT OR AFL-2.1
- **Parser family:** dirtyjson pure-Python lenient decoder (dirtyjson/loader.py), a rewritten simplejson loader (simplejson-derived lineage)
- **Local input API:** `dirtyjson.loads(local JSON bytes); dirtyjson.loads(decoded str) and dirtyjson.load(BytesIO(local bytes)) give the same exact tree on both controls`
- **Documentation:** [API reference](<https://pypi.org/project/dirtyjson/1.0.8/>)
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
python3 parsarium.py build json python dirtyjson
python3 parsarium.py run json python dirtyjson controls/json/structure.json
```
