# simdjson — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `5.0.4`
- **Upstream:** [source repository](<https://github.com/simdjson/simdjson>) · [Debian](<https://tracker.debian.org/pkg/simdjson>)
- **License:** Apache-2.0 OR MIT
- **Parser family:** simdjson ARM64 DOM parser
- **Local input API:** `simdjson::dom::parser::parse(const char *buf, size_t len) -> simdjson::dom::element`
- **Documentation:** [API reference](<https://github.com/simdjson/simdjson/blob/v5.0.4/doc/dom.md>)
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
python3 parsarium.py build json cpp simdjson
python3 parsarium.py run json cpp simdjson controls/json/nested-object.json
```
