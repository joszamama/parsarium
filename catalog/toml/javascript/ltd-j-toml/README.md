# @ltd/j-toml — TOML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.38.0`
- **License:** LGPL-3.0
- **Parser family:** j-toml (LongTengDao; own line-iterator TOML parser)
- **Local input API:** `TOML.parse[1.0](text, { joiner: '\n', bigint: true }) on local bytes decoded as strict UTF-8 text; returns nested tables with BigInt integers, Number floats and OffsetDateTime/LocalDateTime/LocalDate/LocalTime objects`
- **Documentation:** [API reference](<https://github.com/LongTengDao/j-toml/blob/e946ce04db3d72ce59653c4e3daad86681f1de37/README.md>)
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

The README in the 1.38.0 tarball documents TOML.parse(source[, options]) with options.joiner (the string that joins multi-line string lines; required when a document has multi-line strings) and options.bigint (true returns every integer as BigInt), and TOML.parse[1.0] to fix the specification version. With bigint: true, integers are BigInts and floats Numbers, so integer 1000 and float 1e3 stay distinct; offset date-times, local date-times, local dates and local times come back as distinct exported classes. The adapter decodes the bytes with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}), calls TOML.parse[1.0] once with joiner '\n' and bigint true, and walks the result: offset date-times through the documented getUTC* getters (millisecond precision), local kinds through their toISOString, floats as shortest round-trip digits written positionally. Tables are instances of j-toml's internal null-prototype Table class. It never re-parses the text. Both controls match the expected typed trees exactly (data/javascript/toml/ltd-j-toml-tree-verification.json). Only valid controls were run.

## Run this target

```sh
python3 parsarium.py build toml javascript ltd_j_toml
python3 parsarium.py run toml javascript ltd_j_toml controls/toml/service-config.toml
```
