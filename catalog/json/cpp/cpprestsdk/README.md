# cpprestsdk — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.10.19`
- **License:** MIT
- **Parser family:** cpprestsdk own web::json JSON_Parser
- **Local input API:** `web::json::value::parse(const utility::string_t&) on local bytes (utility::string_t is std::string on Linux), after the documented global web::json::keep_object_element_order(true); yields a web::json::value whose numbers report integer (is_int64/is_integral) or double kinds and whose objects keep source member order`
- **Documentation:** [API reference](<https://github.com/microsoft/cpprestsdk/blob/v2.10.19/Release/include/cpprest/json.h>)
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
python3 parsarium.py build json cpp cpprestsdk
python3 parsarium.py run json cpp cpprestsdk controls/json/nested-object.json
```
