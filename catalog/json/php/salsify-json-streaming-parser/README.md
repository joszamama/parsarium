# salsify/json-streaming-parser — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v8.3.1`
- **License:** MIT
- **Parser family:** salsify JsonStreamingParser character state machine (SAX-style listener)
- **Local input API:** `new JsonStreamingParser\Parser(resource $stream, ListenerInterface $listener) then parse() over a php://memory stream holding local JSON text; harness listener builds stdClass/list values from startObject/startArray/key/value events`
- **Documentation:** [API reference](<https://github.com/salsify/jsonstreamingparser/blob/c0cfac990eb4e917c71b0ad0146546f0a4da0c2f/README.md>)
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
python3 parsarium.py build json php salsify_json_streaming_parser
python3 parsarium.py run json php salsify_json_streaming_parser controls/json/nested-object.json
```
