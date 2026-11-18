# @effected/toml — TOML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.20.0`
- **Upstream:** [source repository](<https://github.com/spencerbeggs/effected>) · [npm](<https://www.npmjs.com/package/@effected/toml>)
- **License:** MIT
- **Parser family:** @effected/toml (spencerbeggs; own hand-written scanner, lossless syntax-tree parser and semantic analysis)
- **Local input API:** `TomlVisitor.visit(text) on local bytes decoded as strict UTF-8 text, collected with Effect.runSync(Stream.runCollect(...)); returns TableStart/ArrayTableStart events with resolved table paths and KeyValue events with resolved key paths and typed value nodes (TomlString, TomlInteger, TomlFloat, TomlBoolean, TomlDateTimeLiteral, TomlArray, TomlInlineTable)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@effected/toml/v/0.20.0>)
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

The 0.20.0 README and type declarations (index.d.ts) document TomlVisitor.visit(text): a Stream of TomlVisitorEvent in document order, with TableStart (path), ArrayTableStart (path and 0-based index), KeyValue (path including the final key, and the parsed TomlKeyValue node) and Comment events, failing with TomlParseError on lex, parse or semantic violations. The value-level Toml.parse is not used because it returns safe integers as plain Numbers. The adapter decodes the bytes with TextDecoder('utf-8', {fatal: true, ignoreBOM: true}), collects the events once with Effect.runSync(Stream.runCollect(...)) and assembles the tree: tables from the resolved paths (an array of tables resolves to the element its latest ArrayTableStart opened), scalars from the typed nodes, inline tables from their entries' decoded key paths, date-times formatted from the TomlOffsetDateTime/TomlLocalDateTime/TomlLocalDate/TomlLocalTime fields (offset date-times shifted by offsetMinutes to the UTC instant, nanosecond field kept). It never re-parses the text. Found by a targeted lookup of npm search hits without a lead decision. Both controls match the expected typed trees exactly (data/javascript/toml/effected-toml-tree-verification.json). Only valid controls were run.

## Run this target

```sh
python3 parsarium.py build toml javascript effected_toml
python3 parsarium.py run toml javascript effected_toml controls/toml/service-config.toml
```
