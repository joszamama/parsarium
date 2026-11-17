# jsoncpp — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.9.8`
- **License:** MIT OR LicenseRef-Public-Domain
- **Parser family:** JsonCpp OurReader
- **Local input API:** `Json::CharReaderBuilder::newCharReader()->parse(const char* begin, const char* end, Json::Value*, std::string*) with CharReaderBuilder::strictMode`
- **Documentation:** [API reference](<https://github.com/open-source-parsers/jsoncpp/blob/1.9.8/include/json/reader.h>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/cpp/json/parsers.json) · [control result](../../../../data/cpp/json/verification.json)

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
python3 parsarium.py build json cpp jsoncpp
python3 parsarium.py run json cpp jsoncpp controls/json/nested-object.json
```
