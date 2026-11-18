# petalbranch/toml — TOML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `v1.2.0`
- **Upstream:** [source repository](<https://github.com/PetalBranch/toml>) · [Packagist](<https://packagist.org/packages/petalbranch/toml>)
- **License:** Apache-2.0
- **Parser family:** petalbranch/toml Lexer, LazyTokenStream, Parser and node tree
- **Local input API:** `Petalbranch\Toml\Parser\Parser::parseToNode(string $toml): TableNodeInterface, constructed as new Parser(new Lexer()) (documented in the README 'Lossless Round-Trip' section; Parser::parse() and Toml::parse() return this tree's getValue()); walked through TableNode/InlineTableNode::getEntries() (Entry {key, value}), ArrayNode::getElements() and ValueNode::getType() (TomlType STRING, INTEGER, FLOAT, BOOLEAN, OFFSET_DATETIME, LOCAL_DATETIME, LOCAL_DATE, LOCAL_TIME) with getValue(). Toml::parse(string) and Toml::parseFile(path) are cross-checked against the tree's getValue()`
- **Documentation:** [API reference](<https://github.com/PetalBranch/toml/blob/d8553b064a73ed78e835d5372b2cde66b88837a2/README-EN.md>)
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
python3 parsarium.py build toml php petalbranch_toml
python3 parsarium.py run toml php petalbranch_toml controls/toml/service-config.toml
```
