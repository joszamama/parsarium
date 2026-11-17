# jsonc-parser — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.3.1`
- **License:** MIT
- **Parser family:** Microsoft jsonc-parser scanner and event/tree parser
- **Local input API:** `parseTree(text, errors, {disallowComments:true, allowTrailingComma:false, allowEmptyContent:false}) after strict UTF-8 decoding of local Buffer; zero errors required; exact type-tagged AST projection`
- **Documentation:** [API reference](<https://github.com/microsoft/node-jsonc-parser/blob/v3.3.1/README.md#parser>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/javascript/json/parsers.json) · [control result](../../../../data/javascript/json/verification.json)

## Observed control result

```json
{
  "type": "object",
  "members": {
    "enabled": {
      "type": "boolean",
      "value": true
    },
    "missing": {
      "type": "null"
    },
    "name": {
      "type": "string",
      "value": "parsarium"
    },
    "nested": {
      "type": "object",
      "members": {
        "empty": {
          "type": "object",
          "members": {}
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
        "level": {
          "type": "number",
          "value": 2
        },
        "list": {
          "type": "array",
          "items": []
        }
      }
    },
    "ratio": {
      "type": "number",
      "value": -2.5
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
    "version": {
      "type": "number",
      "value": 1
    }
  }
}
```

## Verification scope

The documented parseTree API returns a hierarchical AST and reports syntax errors separately because the parser is fault tolerant. The adapter uses strict JSON options, rejects nonzero errors, then maps node types and primitive values. Both valid pinned controls yield exact type-tagged trees matching an independent Python json oracle. The controls have no comments, trailing commas, duplicate keys or unsafe numbers, so they do not establish broader acceptance/rejection behavior.

## Run this target

```sh
python3 parsarium.py build json javascript jsonc_parser
python3 parsarium.py run json javascript jsonc_parser controls/json/nested-object.json
```
