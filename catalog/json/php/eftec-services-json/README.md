# eftec/services_json — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.5`
- **License:** BSD-2-Clause
- **Parser family:** PEAR Services_JSON decoder (eftec port)
- **Local input API:** `static eftec\ServicesJson\Services_JSON::decode(string $str) with default flags over local bytes; returns stdClass objects, PHP lists and scalars that the harness type-tags with members in returned order`
- **Documentation:** [API reference](<https://github.com/EFTEC/Services_JSON/blob/4f2892bc19a3e4967d34a20cd1d3430392ffa15c/README.md#decode>)
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
python3 parsarium.py build json php eftec_services_json
python3 parsarium.py run json php eftec_services_json controls/json/nested-object.json
```
