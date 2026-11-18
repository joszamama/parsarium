# moshi — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.15.2`
- **Upstream:** [source repository](<https://github.com/square/moshi>) · [Maven Central](<https://central.sonatype.com/artifact/com.squareup.moshi/moshi>)
- **License:** Apache-2.0
- **Parser family:** Moshi JsonReader/JsonUtf8Reader own tokenizer; Okio I/O dependency
- **Local input API:** `JsonReader.of(Okio.buffer(Okio.source(local File))).readJsonValue(); peek() verifies END_DOCUMENT`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/com/squareup/moshi/moshi/1.15.2/moshi-1.15.2-sources.jar>)
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
python3 parsarium.py build json java moshi
python3 parsarium.py run json java moshi controls/json/nested-object.json
```
