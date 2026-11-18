# jackson-databind — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.23.0`
- **Upstream:** [source repository](<https://github.com/FasterXML/jackson-databind>) · [Maven Central](<https://central.sonatype.com/artifact/com.fasterxml.jackson.core/jackson-databind>)
- **License:** Apache-2.0
- **Parser family:** Jackson (jackson-core streaming parser + databind untyped mapping)
- **Local input API:** `ObjectMapper(JsonFactory with CANONICALIZE_FIELD_NAMES disabled).readValue(File, Object.class)`
- **Documentation:** [API reference](<https://javadoc.io/static/com.fasterxml.jackson.core/jackson-databind/2.23.0/com/fasterxml/jackson/databind/ObjectMapper.html>)
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
python3 parsarium.py build json java jackson_databind
python3 parsarium.py run json java jackson_databind controls/json/nested-object.json
```
