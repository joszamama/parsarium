# toml-eslint-parser — TOML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.3`
- **License:** MIT
- **Parser family:** toml-eslint-parser (own code-point tokenizer and syntax-tree parser)
- **Local input API:** `parseTOML(text, { tomlVersion: '1.0.0' }) on local bytes decoded as strict UTF-8 text; the typed tree walks the returned TOML syntax tree (TOMLTable resolvedKey, TOMLKeyValue keys via getStaticTOMLValue, TOMLValue kind and value)`
- **Documentation:** [API reference](<https://github.com/ota-meshi/toml-eslint-parser/blob/6008e35499342f1116262162d16dbcab0c84760c/README.md#usage-for-directly>)
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

The README at gitHead 6008e35499342f1116262162d16dbcab0c84760c (the 1.0.3 tarball's gitHead) documents direct use: parseTOML(code) returns the AST and getStaticTOMLValue(ast) its static value, and parserOptions.tomlVersion selects 1.0.0 or 1.1.0 (default 1.1.0). getStaticTOMLValue alone returns plain Numbers and Dates, so integer 1000 and float 1e3 or a local date and an offset date-time cannot be told apart from it; the AST keeps them apart. The adapter decodes the bytes with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}), calls parseTOML once with tomlVersion '1.0.0', and assembles the typed tree from the returned nodes: table paths from each TOMLTable's resolvedKey (array-of-tables entries carry numeric indices), key paths from getStaticTOMLValue(key), integers from the node's BigInt, floats from its Number (shortest round-trip digits written positionally), date-time kinds from the node kind with the Date's UTC fields (local kinds are stored as if UTC; the offset date-time Date is the instant). It never re-parses the text and does not read the raw datetime lexeme. Dates keep millisecond precision only; the controls need at most two fractional digits. Both controls match the expected typed trees exactly (data/javascript/toml/toml-eslint-parser-tree-verification.json). Only valid controls were run.

## Run this target

```sh
python3 parsarium.py build toml javascript toml_eslint_parser
python3 parsarium.py run toml javascript toml_eslint_parser controls/toml/service-config.toml
```
