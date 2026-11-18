# @streamparser/json — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.0.26`
- **Upstream:** [source repository](<https://github.com/juanjoDiaz/streamparser-json>) · [npm](<https://www.npmjs.com/package/@streamparser/json>)
- **License:** MIT
- **Parser family:** @streamparser/json TypeScript tokenizer and token parser
- **Local input API:** `new JSONParser({keepStack:true}).write(local Uint8Array); onValue root; end()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@streamparser/json?activeTab=readme>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/javascript/json/parsers.json) · [control result](../../../../data/javascript/json/verification.json)

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

## Run this target

```sh
python3 parsarium.py build json javascript streamparser_json
python3 parsarium.py run json javascript streamparser_json controls/json/nested-object.json
```
