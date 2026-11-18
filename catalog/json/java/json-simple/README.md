# json-simple — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.1.1`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/com.googlecode.json-simple/json-simple>)
- **License:** Apache-2.0
- **Parser family:** json-simple JSONParser with generated JFlex Yylex lexer
- **Local input API:** `new org.json.simple.parser.JSONParser().parse(InputStreamReader(FileInputStream, UTF_8))`
- **Documentation:** [API reference](<https://javadoc.io/static/com.googlecode.json-simple/json-simple/1.1.1/org/json/simple/parser/JSONParser.html>)
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
python3 parsarium.py build json java json_simple
python3 parsarium.py run json java json_simple controls/json/nested-object.json
```
