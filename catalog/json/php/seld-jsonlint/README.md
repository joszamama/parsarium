# seld/jsonlint — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.12.2`
- **Upstream:** [source repository](<https://github.com/Seldaek/jsonlint>) · [Packagist](<https://packagist.org/packages/seld/jsonlint>)
- **License:** MIT
- **Parser family:** seld/jsonlint Lexer and LR table parser
- **Local input API:** `Seld\JsonLint\JsonParser::parse(string $input, int $flags = 0) over local bytes; default flags decode objects to stdClass`
- **Documentation:** [API reference](<https://github.com/Seldaek/jsonlint/blob/4882a0459c88772e4afa3a73ee81b7824490aa9c/README.md>)
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
python3 parsarium.py build json php seld_jsonlint
python3 parsarium.py run json php seld_jsonlint controls/json/nested-object.json
```
