# tomllib.load(local binary file) — TOML / Python

**Pilot / incomplete format cell.**

- **Runtime:** CPython 3.13.1 standard library tomllib
- **Parser family:** tomli (tomllib is a vendored copy of tomli)
- **Official documentation:** [reference](https://docs.python.org/3.13/library/tomllib.html)
- **Valid control:** [`controls/toml/service-config.toml`](../../../../../controls/toml/service-config.toml)
- **Inventory:** [standard API record](../../../../../data/python/toml/standard.json) · [saved result](../../../../../data/python/toml/stdlib-tomllib-control.json)

## Observed control result

```json
{
  "title": {
    "type": "string",
    "value": "Parsarium \"service\" control"
  },
  "enabled": {
    "type": "bool",
    "value": "true"
  },
  "retries": {
    "type": "integer",
    "value": "3"
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
  "database": {
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
    },
    "limits": {
      "max": {
        "type": "integer",
        "value": "10"
      },
      "min": {
        "type": "integer",
        "value": "-2"
      }
    }
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
      "ip": {
        "type": "string",
        "value": "10.0.0.2"
      },
      "enabled": {
        "type": "bool",
        "value": "false"
      }
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
      "name": {
        "type": "string",
        "value": "Nail"
      },
      "color": {
        "type": "string",
        "value": "gray"
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
  ]
}
```
