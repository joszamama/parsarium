# jsoncons — JSON / C++

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.10.0`
- **Upstream:** [source repository](<https://github.com/danielaparker/jsoncons>) · [Debian](<https://tracker.debian.org/pkg/jsoncons>)
- **License:** BSL-1.0
- **Parser family:** jsoncons own basic_json_parser
- **Local input API:** `jsoncons::ojson::parse(const char*, std::size_t) on local bytes, yielding an insertion-ordered basic_json tree with integer and double kinds`
- **Documentation:** [API reference](<https://github.com/danielaparker/jsoncons/blob/v1.10.0/doc/ref/corelib/json/parse.md>)
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
python3 parsarium.py build json cpp jsoncons
python3 parsarium.py run json cpp jsoncons controls/json/nested-object.json
```
