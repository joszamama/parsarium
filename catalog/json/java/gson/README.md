# gson — JSON / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.15.0`
- **License:** Apache-2.0
- **Parser family:** Gson (com.google.gson.stream.JsonReader + ObjectTypeAdapter untyped mapping)
- **Local input API:** `new Gson().fromJson(Reader, Object.class) over InputStreamReader(FileInputStream, UTF_8)`
- **Documentation:** [API reference](<https://javadoc.io/doc/com.google.code.gson/gson/2.15.0/com.google.gson/com/google/gson/Gson.html>)
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
python3 parsarium.py build json java gson
python3 parsarium.py run json java gson controls/json/nested-object.json
```
