# laminas/laminas-json — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.8.0`
- **License:** BSD-3-Clause
- **Parser family:** Laminas Json Decoder pure-PHP parser (Zend JSON lineage)
- **Local input API:** `Set Laminas\Json\Json::$useBuiltinEncoderDecoder = true, then Json::decode(string $input) over local JSON text; forces package Decoder instead of ext/json`
- **Documentation:** [API reference](<https://docs.laminas.dev/laminas-json/advanced/#internal-encoderdecoder>)
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
