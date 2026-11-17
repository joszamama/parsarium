# halaxa/json-machine — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.2.6`
- **License:** Apache-2.0
- **Parser family:** JSON Machine Lexer/Parser plus PHP ext/json member decoder
- **Local input API:** `JsonMachine\Items::fromString(string $input, array $options) over local JSON text; iteration yields top-level members; ExtJsonDecoder decodes each value`
- **Documentation:** [API reference](<https://github.com/halaxa/json-machine/blob/8bf0b0ff6ff60ab480778eaa5ad7d505b442c2d4/README.md>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/php/json/parsers.json) · [control result](../../../../data/php/json/verification.json)

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
python3 parsarium.py build json php halaxa_json_machine
python3 parsarium.py run json php halaxa_json_machine controls/json/nested-object.json
```
