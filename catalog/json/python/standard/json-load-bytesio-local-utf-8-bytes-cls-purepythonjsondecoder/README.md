# json.load(BytesIO(local UTF-8 bytes), cls=PurePythonJSONDecoder) — JSON / Python

**Pilot / incomplete format cell.**

- **Runtime:** CPython 3.14.4 standard library pure-Python JSON decoder
- **Parser family:** See standard API inventory
- **Official documentation:** [reference](https://docs.python.org/3.14/library/json.html)
- **Valid control:** [`controls/json/structure.json`](../../../../../controls/json/structure.json)
- **Inventory:** [standard API record](../../../../../data/python/json/standard.json) · [saved result](../../../../../projects/json/python/stdlib_json/verification.json)

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
python3 parsarium.py build json python stdlib_json
python3 parsarium.py run json python stdlib_json controls/json/structure.json
```
