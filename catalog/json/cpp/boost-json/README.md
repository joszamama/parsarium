# Boost.JSON — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.92.0`
- **License:** BSL-1.0
- **Parser family:** Boost.JSON basic_parser
- **Local input API:** `boost::json::parse(string_view s, boost::system::error_code& ec, storage_ptr sp = {}, parse_options const& opt = {}) over locally supplied bytes; default options accept only standard JSON`
- **Documentation:** [API reference](<https://www.boost.org/doc/libs/1_92_0/libs/json/doc/html/ref/parse.html>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/cpp/json/parsers.json) · [control result](../../../../data/cpp/json/verification.json)
- **Adoption:** no primary rank; the Debian source `boost1.83` covers all of Boost. Separately labeled fallback: 1,749 `libboost-json-dev` installations.

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
python3 parsarium.py build json cpp boost-json
python3 parsarium.py run json cpp boost-json controls/json/nested-object.json
```
