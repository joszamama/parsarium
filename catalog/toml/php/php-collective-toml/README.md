# php-collective/toml — TOML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.1.5`
- **Upstream:** [source repository](<https://github.com/php-collective/toml>) · [Packagist](<https://packagist.org/packages/php-collective/toml>)
- **License:** MIT
- **Parser family:** php-collective/toml Lexer, Parser, AST and Normalizer
- **Local input API:** `PhpCollective\Toml\Toml::tryParse(string $input): ParseResult (documented 'Parse without exceptions and keep diagnostics + partial AST'; same Parser and Normalizer as Toml::decode), rejected unless isValid(); getDocument() is walked through Document->items (KeyValue, Table {key->parts, isArrayTable, items}) and typed value nodes StringValue, IntegerValue, FloatValue, BoolValue, OffsetDateTime {DateTimeImmutable}, LocalDateTime, LocalDate, LocalTime {string}, ArrayValue and InlineTable; the walk's getValue() results must equal getValue() of the ParseResult. Toml::decode(string) and Toml::decodeFile(path) are cross-checked for the same array`
- **Documentation:** [API reference](<https://github.com/php-collective/toml/blob/51810282d85d6333c60c866019c0e6548e26e483/README.md>)
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
python3 parsarium.py build toml php php_collective_toml
python3 parsarium.py run toml php php_collective_toml controls/toml/service-config.toml
```
