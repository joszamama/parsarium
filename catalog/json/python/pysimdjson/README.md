# pysimdjson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `8.0.0`
- **License:** MIT
- **Parser family:** simdjson 5.1.1 C++ DOM parser (vendored amalgamation, arm64 NEON kernel on linux/arm64) / pysimdjson Cython binding
- **Local input API:** `simdjson.Parser().parse(local JSON bytes, recursive=True); Parser().load(local path, recursive=True) gives the same exact tree on both controls`
- **Documentation:** [API reference](<https://github.com/TkTech/pysimdjson/blob/98a6f9a84bfc0620cf8b5c450d22b8eeae313bfd/docs/native.rst>)
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
python3 parsarium.py build json python pysimdjson
python3 parsarium.py run json python pysimdjson controls/json/structure.json
```
