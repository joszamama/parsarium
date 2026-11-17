# json-bigint — JSON / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parser family:** Crockford JSON.js recursive-descent parser adapted by json-bigint
- **Local input API:** `JSONbig.parse(text) after decoding a local Buffer with strict UTF-8 TextDecoder; exact type-tagged tree of returned values`
- **Documentation:** [API reference](<https://github.com/sidorares/json-bigint/blob/390482a8b6b460f98c61c3b65915dbd91fc8e7b2/README.md>)
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

The documented parse(text) API receives one strict UTF-8 decoded local control. The two pinned controls contain only Number-safe numeric literals and the adapter emits exact type-tagged trees. lib/parse.js itself parses JSON syntax and rejects trailing text. Its source chooses BigNumber for finite numeric tokens whose strings exceed 15 characters by default; this source branch is not exercised by the two controls, and no large-integer behavior is claimed from a control run.

## Run this target

```sh
python3 parsarium.py build json javascript json_bigint
python3 parsarium.py run json javascript json_bigint controls/json/nested-object.json
```
