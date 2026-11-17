# taoJSON — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.0-beta.14`
- **License:** MIT
- **Parser family:** taoJSON own JSON grammar on the PEGTL engine
- **Local input API:** `tao::json::from_string(const char*, std::size_t, source) on local bytes, yielding a tao::json::value with signed, unsigned and double number kinds; objects are std::map with sorted keys`
- **Documentation:** [API reference](<https://github.com/taocpp/json/blob/1.0.0-beta.14/doc/Batteries-Included.md>)
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
python3 parsarium.py build json cpp tao-json
python3 parsarium.py run json cpp tao-json controls/json/nested-object.json
```
