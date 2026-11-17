# laktak/hjson — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v2.3.1`
- **License:** MIT
- **Parser family:** hjson-php HJSONParser (port of hjson-js) recursive character parser
- **Local input API:** `new HJSON\HJSONParser() then parse(string $text) with default options over local UTF-8 bytes; returns stdClass objects, PHP lists and scalars that the harness type-tags with members in returned order`
- **Documentation:** [API reference](<https://github.com/hjson/hjson-php/blob/97c5cf2c0779cb6099976e9387e752f879beb106/README.md#hjsonparser-parsetext-options>)
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
