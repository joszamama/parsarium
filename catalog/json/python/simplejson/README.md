# simplejson — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.3.0`
- **Upstream:** [source repository](<https://github.com/simplejson/simplejson>) · [PyPI](<https://pypi.org/project/simplejson/>)
- **License:** MIT OR AFL-2.1
- **Parser family:** simplejson pure-Python JSON decoder
- **Local input API:** `simplejson.load(BytesIO(local UTF-8 JSON bytes), allow_nan=False)`
- **Documentation:** [API reference](<https://simplejson.readthedocs.io/en/latest/>)
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
python3 parsarium.py build json python simplejson
python3 parsarium.py run json python simplejson controls/json/structure.json
```
