# smol-toml — TOML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.9.1`
- **License:** BSD-3-Clause
- **Parser family:** smol-toml (own hand-written TOML parser)
- **Local input API:** `parse(text, { integersAsBigInt: true }) on local bytes decoded as strict UTF-8 text; the typed tree walks the returned TomlTable (BigInt integers, Number floats, TomlDate date-times)`
- **Documentation:** [API reference](<https://github.com/squirrelchat/smol-toml/blob/v1.9.1/README.md#usage>)
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

The README (tag v1.9.1) documents parse(toml, options) and the integersAsBigInt option ("parse integers as BigInt") and TomlDate with isDate()/isTime()/isLocal(). With integersAsBigInt: true every TOML integer is a BigInt and every float a Number, so integer 1000 and float 1e3 stay distinct; without the option both come back as the Number 1000. The adapter decodes the bytes with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}), calls parse once and builds the typed tree from the returned values: BigInt -> integer, Number -> float (shortest round-trip digits written positionally), TomlDate isDate() -> date-local, isTime() -> time-local, isLocal() -> datetime-local, otherwise datetime as the UTC instant of Date.prototype.toISOString with the zero fraction trimmed. TomlDate keeps millisecond precision only; the controls need at most two fractional digits. Both controls match the expected typed trees exactly (data/javascript/toml/smol-toml-tree-verification.json). Only valid controls were run.

## Run this target

```sh
python3 parsarium.py build toml javascript smol_toml
python3 parsarium.py run toml javascript smol_toml controls/toml/service-config.toml
```
