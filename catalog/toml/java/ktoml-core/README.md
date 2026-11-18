# ktoml-core — TOML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.7.1`
- **Upstream:** [source repository](<https://github.com/orchestr7/ktoml>) · [Maven Central](<https://central.sonatype.com/artifact/com.akuleshov7/ktoml-core-jvm>)
- **License:** MIT
- **Parser family:** ktoml (orchestr7/akuleshov7 Kotlin multiplatform; own line-oriented TomlParser and value parsers in ktoml-core)
- **Local input API:** `TomlParser(TomlInputConfig()).parseString(String) -> TomlFile node tree (documented in the README 'Parser to AST' section and the TomlParser.parseString KDoc); from Java the Kotlin value-class method is the public static TomlParser.parseString-impl(TomlInputConfig, String), called by reflection; parse errors throw TomlDecodingException`
- **Documentation:** [API reference](<https://github.com/orchestr7/ktoml/blob/267f5dfc4b7caa667d687dce136f86cbb2f6e2ec/README.md#parser-to-ast>)
- **Valid control:** [`controls/toml/service-config.toml`](../../../../controls/toml/service-config.toml)
- **Catalog evidence:** [parser record](../../../../data/java/toml/parsers.json) · [control result](../../../../data/java/toml/verification.json)

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
python3 parsarium.py build toml java ktoml_core
python3 parsarium.py run toml java ktoml_core controls/toml/service-config.toml
```
