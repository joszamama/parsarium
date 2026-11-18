# toml_edit — TOML / Rust

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.25.19+spec-1.1.0`
- **Upstream:** [source repository](<https://github.com/toml-rs/toml>) · [crates.io](<https://crates.io/crates/toml_edit>)
- **License:** MIT OR Apache-2.0
- **Parser family:** toml_parser (toml-rs): toml_parser 1.1.5 lexes and emits parse events; toml_edit assembles its own format-preserving Document/Item/Value tree from those events. Shared with the selected toml path; not an independent lexer or parser.
- **Local input API:** `str::parse::<toml_edit::DocumentMut>() -> Result<DocumentMut, TomlError>; DocumentMut derefs to Table of Item::{None, Value, Table, ArrayOfTables}; Value::{String, Integer, Float, Boolean, Datetime (Formatted<toml_datetime::Datetime>), Array, InlineTable}`
- **Documentation:** [API reference](<https://docs.rs/toml_edit/0.25.19+spec-1.1.0/toml_edit/struct.DocumentMut.html>)
- **Valid control:** [`controls/toml/service-config.toml`](../../../../controls/toml/service-config.toml)
- **Catalog evidence:** [parser record](../../../../data/rust/toml/parsers.json) · [control result](../../../../projects/toml/rust/toml_edit/verification.json)

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
python3 parsarium.py build toml rust toml_edit
python3 parsarium.py run toml rust toml_edit controls/toml/service-config.toml
```
