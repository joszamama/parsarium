# bfj — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `9.1.4`
- **Upstream:** [source repository](<https://gitlab.com/philbooth/bfj>) · [npm](<https://www.npmjs.com/package/bfj>)
- **License:** MIT
- **Parser family:** bfj asynchronous JSON walker
- **Local input API:** `bfj.parse(Readable.from([local Buffer]), {ndjson:false}) returns a Promise after consuming a complete JSON stream`
- **Documentation:** [API reference](<https://www.npmjs.com/package/bfj?activeTab=readme>)
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
python3 parsarium.py build json javascript bfj
python3 parsarium.py run json javascript bfj controls/json/nested-object.json
```
