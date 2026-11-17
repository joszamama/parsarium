# fastjson — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.2.83`
- **License:** Apache-2.0
- **Parser family:** fastjson 1.x DefaultJSONParser and JSONLexer
- **Local input API:** `JSON.parse(Files.readAllBytes(local Path))`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/alibaba/fastjson/1.2.83/fastjson-1.2.83-sources.jar>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/java/json/parsers.json) · [control result](../../../../data/java/json/verification.json)

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
python3 parsarium.py build json java fastjson1
python3 parsarium.py run json java fastjson1 controls/json/nested-object.json
```
