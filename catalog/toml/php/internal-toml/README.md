# internal/toml — TOML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.1.3`
- **License:** BSD-3-Clause
- **Parser family:** internal/toml (php-internal/toml) Lexer, recursive-descent Parser and AST
- **Local input API:** `Internal\Toml\Toml::parse(string $toml): Document (documented 'Working with AST'), walked through Document->nodes (Entry, Table, TableArray with Key->segments) and typed value nodes StringValue, IntegerValue, FloatValue, BooleanValue, DateTimeValue {value: DateTimeImmutable, type: DateTimeType::OffsetDatetime|LocalDatetime|LocalDate}, LocalTimeValue {value: string}, ArrayValue and InlineTableValue; the walk's PHP values must equal Document::toArray(). Toml::parseToArray(string) is cross-checked against Document::toArray()`
- **Documentation:** [API reference](<https://github.com/php-internal/toml/blob/b0e077794a179b0a39a4fba84185762a4425c472/README.md>)
- **Valid control:** [`controls/toml/service-config.toml`](../../../../controls/toml/service-config.toml)
- **Catalog evidence:** [parser record](../../../../data/php/toml/parsers.json) · [control result](../../../../data/php/toml/verification.json)

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
python3 parsarium.py build toml php internal_toml
python3 parsarium.py run toml php internal_toml controls/toml/service-config.toml
```
