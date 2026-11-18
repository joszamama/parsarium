# klkvsk/json-decode-stream — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.0.3`
- **Upstream:** [source repository](<https://github.com/klkvsk/json-decode-stream>) · [Packagist](<https://packagist.org/packages/klkvsk/json-decode-stream>)
- **License:** MIT
- **Parser family:** klkvsk json-decode-stream Tokenizer, event Parser and Collector
- **Local input API:** `JsonDecodeStream\Parser::fromString(string) then items() with no selector over local bytes, yielding each complete top-level document (objects as stdClass); harness requires exactly one document and type-tags it. Parser::fromFile(string $path) and Parser::fromStream(resource) are cross-checked for the same tree`
- **Documentation:** [API reference](<https://github.com/klkvsk/json-decode-stream/blob/831b5310b42b51705a2d6ae5353bba7aaa302358/README.md>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/php/json/parsers.json) · [control result](../../../../data/php/json/verification.json)

## Observed control result

```json
{
  "type": "object",
  "members": {
    "name": {
      "type": "string",
      "value": "parsarium"
    },
    "version": {
      "type": "number",
      "value": 1
    },
    "ratio": {
      "type": "number",
      "value": -2.5
    },
    "enabled": {
      "type": "boolean",
      "value": true
    },
    "missing": {
      "type": "null"
    },
    "tags": {
      "type": "array",
      "items": [
        {
          "type": "string",
          "value": "json"
        },
        {
          "type": "string",
          "value": "go"
        },
        {
          "type": "string",
          "value": "rfc8259"
        }
      ]
    },
    "nested": {
      "type": "object",
      "members": {
        "level": {
          "type": "number",
          "value": 2
        },
        "items": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "members": {
                "id": {
                  "type": "number",
                  "value": 1
                },
                "ok": {
                  "type": "boolean",
                  "value": false
                }
              }
            },
            {
              "type": "object",
              "members": {
                "id": {
                  "type": "number",
                  "value": 2
                },
                "text": {
                  "type": "string",
                  "value": "café \"quoted\""
                }
              }
            }
          ]
        },
        "empty": {
          "type": "object",
          "members": {}
        },
        "list": {
          "type": "array",
          "items": []
        }
      }
    }
  }
}
```

## Run this target

```sh
python3 parsarium.py build json php klkvsk_json_decode_stream
python3 parsarium.py run json php klkvsk_json_decode_stream controls/json/nested-object.json
```
