# lossless-json — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `4.3.3`
- **Upstream:** [source repository](<https://github.com/josdejong/lossless-json>) · [npm](<https://www.npmjs.com/package/lossless-json>)
- **License:** MIT
- **Parser family:** lossless-json own recursive-descent JSON value parser
- **Local input API:** `parse(text) from the pinned ESM export after strict UTF-8 TextDecoder of local bytes; returns LosslessNumber objects for every JSON numeric token`
- **Documentation:** [API reference](<https://github.com/josdejong/lossless-json/blob/v4.3.3/README.md>)
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
                  "type": "LosslessNumber",
                  "raw": "1"
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
                  "type": "LosslessNumber",
                  "raw": "2"
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
          "type": "LosslessNumber",
          "raw": "2"
        },
        "list": {
          "type": "array",
          "items": []
        }
      }
    },
    "ratio": {
      "type": "LosslessNumber",
      "raw": "-0.25e1"
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
      "type": "LosslessNumber",
      "raw": "1"
    }
  }
}
```

## Verification scope

Docker valid controls match independent Python JSON parsing with exact numeric lexemes: every JSON number is a LosslessNumber with raw source spelling. V8 covers 252 own lib/esm/parse.js lines; parser-source AFL++ ranges are stable over three fresh runs per control and differ by 8 features/8 tuples. No shared parser engine, malformed-input, or campaign claim. Selected as the tenth within-cell path with its independent numeric-lexeme-preserving parser family.

## Run this target

```sh
python3 parsarium.py build json javascript lossless_json
python3 parsarium.py run json javascript lossless_json controls/json/nested-object.json
```
