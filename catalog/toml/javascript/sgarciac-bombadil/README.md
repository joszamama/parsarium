# @sgarciac/bombadil — TOML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.3.0`
- **License:** Artistic-2.0
- **Parser family:** bombadil (sgarciac; own chevrotain TOML 0.5.0 lexer and grammar)
- **Local input API:** `new TomlReader().readToml(text, true) on local bytes decoded as strict UTF-8 text; result holds tables { type: 'table', content }, arrays and typed primitives { type, image, value } (README 'Full typing information'); errors holds lexer, parser and table-loading errors`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@sgarciac/bombadil/v/2.3.0>)
- **Valid control:** [`controls/toml/service-config.toml`](../../../../controls/toml/service-config.toml)
- **Catalog evidence:** [parser record](../../../../data/javascript/toml/parsers.json) · [control result](../../../../data/javascript/toml/verification.json)

## Observed control result

```json
{
  "database": {
    "limits": {
      "max": {
        "type": "integer",
        "value": "10"
      },
      "min": {
        "type": "integer",
        "value": "-2"
      }
    },
    "ports": [
      {
        "type": "integer",
        "value": "8000"
      },
      {
        "type": "integer",
        "value": "8001"
      },
      {
        "type": "integer",
        "value": "8002"
      }
    ],
    "ratio": {
      "type": "float",
      "value": "3.25"
    }
  },
  "enabled": {
    "type": "bool",
    "value": "true"
  },
  "owner": {
    "name": {
      "type": "string",
      "value": "Zoë"
    },
    "since": {
      "type": "datetime",
      "value": "1979-05-27T07:32:00Z"
    }
  },
  "products": [
    {
      "name": {
        "type": "string",
        "value": "Hammer"
      },
      "sku": {
        "type": "integer",
        "value": "738594937"
      }
    },
    {
      "color": {
        "type": "string",
        "value": "gray"
      },
      "name": {
        "type": "string",
        "value": "Nail"
      },
      "points": [
        {
          "x": {
            "type": "integer",
            "value": "1"
          },
          "y": {
            "type": "integer",
            "value": "2"
          }
        },
        {
          "x": {
            "type": "integer",
            "value": "3"
          },
          "y": {
            "type": "integer",
            "value": "4"
          }
        }
      ]
    }
  ],
  "retries": {
    "type": "integer",
    "value": "3"
  },
  "servers": {
    "alpha": {
      "ip": {
        "type": "string",
        "value": "10.0.0.1"
      },
      "tags": [
        {
          "type": "string",
          "value": "edge"
        },
        {
          "type": "string",
          "value": "eu"
        }
      ]
    },
    "beta": {
      "enabled": {
        "type": "bool",
        "value": "false"
      },
      "ip": {
        "type": "string",
        "value": "10.0.0.2"
      }
    }
  },
  "title": {
    "type": "string",
    "value": "Parsarium \"service\" control"
  }
}
```

## Verification scope

The 2.3.0 README documents new bombadil.TomlReader, readToml(input) with result and errors, and the 'Full typing information' mode readToml(input, true), in which tables and primitives are objects with a type (table, atomicString, atomicInteger, atomicFloat, atomicBoolean, offsetDateTime, localDateTime, localDate, localTime), the toml image and the JavaScript value; without the flag integers and floats are both Numbers. The adapter decodes the bytes with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}), calls readToml once with the flag, requires an empty errors list and walks the result using only type and value: Dates through Date.prototype.toISOString (local kinds are stored at UTC±00:00), integers only within the exact Number range, floats as shortest round-trip digits written positionally. The image strings are never read and the text is never re-parsed. bombadil targets TOML 0.5.0; both controls are inside the subset it shares with TOML 1.0.0. Found by a targeted lookup of npm search hits without a lead decision (also listed in the toml-lang wiki). Both controls match the expected typed trees exactly (data/javascript/toml/sgarciac-bombadil-tree-verification.json). Only valid controls were run.

## Run this target

```sh
python3 parsarium.py build toml javascript sgarciac_bombadil
python3 parsarium.py run toml javascript sgarciac_bombadil controls/toml/service-config.toml
```
