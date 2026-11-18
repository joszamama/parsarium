# hjson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.1.0`
- **Upstream:** [source repository](<https://github.com/hjson/hjson-py>) · [PyPI](<https://pypi.org/project/hjson/>)
- **License:** MIT OR AFL-2.1
- **Parser family:** hjson-py pure-Python Hjson decoder (hjson/decoder.py), based on simplejson (simplejson-derived lineage)
- **Local input API:** `hjson.loads(local JSON bytes); hjson.loads(decoded str) and hjson.load(BytesIO(local bytes)) give the same exact tree on both controls`
- **Documentation:** [API reference](<https://pypi.org/project/hjson/3.1.0/>)
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
python3 parsarium.py build json python hjson
python3 parsarium.py run json python hjson controls/json/structure.json
```
