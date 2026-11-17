# ijson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.6.0`
- **License:** BSD-3-Clause AND ISC
- **Parser family:** ijson yajl2_c C extension / yajl 2.1.1 (rtobar fork) C parser
- **Local input API:** `ijson.items(BytesIO(local JSON bytes), '') on the default yajl2_c backend`
- **Documentation:** [API reference](<https://github.com/ICRAR/ijson/blob/v3.6.0/README.rst>)
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
python3 parsarium.py build json python ijson
python3 parsarium.py run json python ijson controls/json/structure.json
```
