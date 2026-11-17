# boundwize/jsonrecast — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.37`
- **License:** MIT
- **Parser family:** boundwize/jsonrecast Lexer and recursive-descent JsonParser (formatting-preserving AST)
- **Local input API:** `Boundwize\JsonRecast\JsonRecast::parse(string $source) over local bytes returns a JsonDocument AST; harness walks ObjectNode items, ArrayNode items, StringNode/BooleanNode values, NullNode and NumberNode::toIntOrFloat() into a type-tagged tree with members in source order`
- **Documentation:** [API reference](<https://github.com/boundwize/jsonrecast/blob/d37e0d808cd5c0a8f6e5d6f36ea363202950e399/README.md>)
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
