# @decimalturn/toml-patch — TOML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `3.3.3`
- **License:** MIT
- **Parser family:** toml-patch (Tim Hall's format-preserving TOML parser, maintained fork by DecimalTurn)
- **Local input API:** `parse(text, { integersAsBigInt: true }) on local bytes decoded as strict UTF-8 text; returns plain objects with BigInt integers, Number floats and the exported OffsetDateTime/LocalDateTime/LocalDate/LocalTime Date subclasses`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@decimalturn/toml-patch/v/3.3.3>)
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

The package type declarations (dist/toml-patch.d.ts in the 3.3.3 tarball) document parse(value, options?) with ParseOptions.integersAsBigInt (true returns every integer as bigint; the default 'asNeeded' returns safe integers as Numbers, which would make integer 1000 and float 1e3 indistinguishable) and the exported Date subclasses LocalDate, LocalTime, LocalDateTime and OffsetDateTime. The adapter decodes the bytes with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}), calls parse once with integersAsBigInt true, and walks the result: date kinds from the exported classes, their fields through Date.prototype.toISOString (millisecond precision; local kinds are stored in the Date's UTC fields, the offset date-time Date is the instant), floats as shortest round-trip digits written positionally. It never re-parses the text. The published bundle is minified into 83 long lines, so its line counts understate the code reached. Both controls match the expected typed trees exactly (data/javascript/toml/decimalturn-toml-patch-tree-verification.json). Only valid controls were run.

## Run this target

```sh
python3 parsarium.py build toml javascript decimalturn_toml_patch
python3 parsarium.py run toml javascript decimalturn_toml_patch controls/toml/service-config.toml
```
