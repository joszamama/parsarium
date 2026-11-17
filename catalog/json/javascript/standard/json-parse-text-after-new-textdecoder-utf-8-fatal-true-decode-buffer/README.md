# JSON.parse(text) after new TextDecoder('utf-8', {fatal: true}).decode(Buffer) — JSON / JavaScript

**Pilot / incomplete format cell.**

- **Runtime:** Node.js 26.10.0
- **Parser family:** V8 native JSON.parse (JsonParser)
- **Official documentation:** [reference](https://tc39.es/ecma262/#sec-json.parse)
- **Valid control:** [`controls/json/nested-object.json`](../../../../../controls/json/nested-object.json)
- **Inventory:** [standard API record](../../../../../data/javascript/json/standard.json) · [saved result](../../../../../data/javascript/json/standard-receipt.json)

## Observed control result

```json
{
  "arrays": 3,
  "booleans": 2,
  "max_depth": 4,
  "nulls": 1,
  "numbers": [
    -2.5,
    1,
    1,
    2,
    2
  ],
  "objects": 5,
  "root": "object",
  "strings": [
    "café \"quoted\"",
    "go",
    "json",
    "parsarium",
    "rfc8259"
  ],
  "top_level_keys": [
    "enabled",
    "missing",
    "name",
    "nested",
    "ratio",
    "tags",
    "version"
  ]
}
```

**Docker control:** [pinned project](../../../../../projects/json/javascript/stdlib_json_parse/README.md). V8 JSON parser function entries were observed; source lines and AFL++ feedback are unavailable.
