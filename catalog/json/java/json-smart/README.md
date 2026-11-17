# json-smart — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.6.1`
- **License:** Apache-2.0
- **Parser family:** json-smart own JSONParser byte/stream parser
- **Local input API:** `new net.minidev.json.parser.JSONParser(JSONParser.MODE_RFC4627).parse(Files.readAllBytes(local Path))`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/net/minidev/json-smart/2.6.1/json-smart-2.6.1-sources.jar>)
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
python3 parsarium.py build json java json_smart
python3 parsarium.py run json java json_smart controls/json/nested-object.json
```
