# pcrov/jsonreader — JSON / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.4`
- **Upstream:** [source repository](<https://github.com/pcrov/JsonReader>) · [Packagist](<https://packagist.org/packages/pcrov/jsonreader>)
- **License:** MIT
- **Parser family:** pcrov JsonReader Lexer and JsonParser pull state machine
- **Local input API:** `new pcrov\JsonReader\JsonReader() then json(string $json) over local bytes, pulled with read()/type()/name()/value()/depth(); harness builds a type-tagged tree from OBJECT/ARRAY/scalar nodes. open(string $uri) on the local control file and stream(resource) are cross-checked for the same tree`
- **Documentation:** [API reference](<https://github.com/pcrov/JsonReader/wiki/JsonReader-API/6a5d9e3d004cde30dbcb9acd3ad69d80fb33aec6>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/php/json/parsers.json) · [control result](../../../../data/php/json/verification.json)

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

## Run this target

```sh
python3 parsarium.py build json php pcrov_jsonreader
python3 parsarium.py run json php pcrov_jsonreader controls/json/nested-object.json
```
