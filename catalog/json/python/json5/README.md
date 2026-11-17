# json5 — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.17.3`
- **License:** Apache-2.0
- **Parser family:** json5 pure-Python PEG parser (glop-generated json5/parser.py) with AST conversion in json5/lib.py
- **Local input API:** `json5.loads(local JSON bytes); json5.loads(decoded str) and json5.load(BytesIO(local bytes)) give the same exact tree on both controls`
- **Documentation:** [API reference](<https://github.com/dpranke/pyjson5/blob/v0.17.3/README.md>)
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
python3 parsarium.py build json python json5
python3 parsarium.py run json python json5 controls/json/structure.json
```
