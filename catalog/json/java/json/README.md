# json — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `20260814`
- **License:** Public Domain
- **Parser family:** org.json JSONTokener with JSONObject/JSONArray builders
- **Local input API:** `new JSONTokener(InputStreamReader(FileInputStream, UTF_8), new JSONParserConfiguration().withStrictMode()).nextValue(); nextClean() checks end of local document`
- **Documentation:** [API reference](<https://repo.maven.apache.org/maven2/org/json/json/20260814/json-20260814-sources.jar>)
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
python3 parsarium.py build json java orgjson
python3 parsarium.py run json java orgjson controls/json/nested-object.json
```
