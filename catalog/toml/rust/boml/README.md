# boml — TOML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.0.1`
- **License:** MIT OR Apache-2.0
- **Parser family:** boml (brightshard, codeberg.org): own dependency-free scanner and parser; independent of toml_parser, toml, toml_edit and taplo (no dependency on them).
- **Local input API:** `boml::parse(&str) -> Result<boml::Toml, Error>; Toml derefs to TomlTable of TomlValue::{String, Integer (i64), Float (f64), Boolean, OffsetDateTime, DateTime, Date, Time, Array, Table}`
- **Documentation:** [API reference](<https://docs.rs/boml/2.0.1/boml/fn.parse.html>)
- **Valid control:** [`controls/toml/service-config.toml`](../../../../controls/toml/service-config.toml)
- **Catalog evidence:** [parser record](../../../../data/rust/toml/parsers.json) · [control result](../../../../projects/toml/rust/boml/verification.json)

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

## Run this target

```sh
python3 parsarium.py build toml rust boml
python3 parsarium.py run toml rust boml controls/toml/service-config.toml
```
