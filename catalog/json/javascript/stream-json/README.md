# stream-json — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.9.0`
- **License:** BSD-3-Clause
- **Parser family:** stream-json charCodeAt/regex streaming tokenizer
- **Local input API:** `chain([Readable.from([Buffer]), parser()]) with Assembler.connectTo(pipeline, {onDone})`
- **Documentation:** [API reference](<https://github.com/uhop/stream-json/wiki/Parser>)
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
python3 parsarium.py build json javascript stream_json
python3 parsarium.py run json javascript stream_json controls/json/nested-object.json
```
