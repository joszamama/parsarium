# msgspec — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.22.0`
- **License:** BSD-3-Clause
- **Parser family:** msgspec hand-written C JSON decoder (src/msgspec/_core.c)
- **Local input API:** `msgspec.json.decode(local JSON bytes) with the default type=Any`
- **Documentation:** [API reference](<https://msgspec.dev/api.html#msgspec.json.decode>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/python/json/parsers.json) · [control result](../../../../data/python/json/verification.json)

## Observed control result

```json
{
  "value": [
    "object",
    [
      [
        "name",
        [
          "string",
          "parsarium"
        ]
      ],
      [
        "version",
        [
          "int",
          1
        ]
      ],
      [
        "ratio",
        [
          "float",
          "-2.5"
        ]
      ],
      [
        "enabled",
        [
          "bool",
          true
        ]
      ],
      [
        "missing",
        [
          "null"
        ]
      ],
      [
        "tags",
        [
          "array",
          [
            [
              "string",
              "json"
            ],
            [
              "string",
              "go"
            ],
            [
              "string",
              "rfc8259"
            ]
          ]
        ]
      ],
      [
        "nested",
        [
          "object",
          [
            [
              "level",
              [
                "int",
                2
              ]
            ],
            [
              "items",
              [
                "array",
                [
                  [
                    "object",
                    [
                      [
                        "id",
                        [
                          "int",
                          1
                        ]
                      ],
                      [
                        "ok",
                        [
                          "bool",
                          false
                        ]
                      ]
                    ]
                  ],
                  [
                    "object",
                    [
                      [
                        "id",
                        [
                          "int",
                          2
                        ]
                      ],
                      [
                        "text",
                        [
                          "string",
                          "café \"quoted\""
                        ]
                      ]
                    ]
                  ]
                ]
              ]
            ],
            [
              "empty",
              [
                "object",
                []
              ]
            ],
            [
              "list",
              [
                "array",
                []
              ]
            ]
          ]
        ]
      ]
    ]
  ]
}
```

## Run this target

```sh
python3 parsarium.py build json python msgspec
python3 parsarium.py run json python msgspec controls/json/nested-object.json
```
