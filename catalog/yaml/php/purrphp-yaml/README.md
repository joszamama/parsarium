# purrphp/yaml — YAML / PHP

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parser family:** PurrPHP Yaml own line reader, block Parser.php, InlineParser.php flow/scalar parser and CoreSchema resolver
- **Local input API:** `Purr\Yaml\YamlStreamSingle::fromString(string) over local bytes; the documented node model (MappingNode entries, SequenceNode items, AliasNode targets) is walked in source order and each scalar is typed by the package's Schema\CoreSchema::resolve`
- **Documentation:** [API reference](<https://github.com/PurrPHP/yaml/blob/c069a72e06e5a11a725b50226122f1eb26eb64fe/README.md>)
- **Valid control:** [`controls/yaml/catalog.yaml`](../../../../controls/yaml/catalog.yaml)
- **Catalog evidence:** [parser record](../../../../data/php/yaml/parsers.json) · [control result](../../../../data/php/yaml/verification.json)

## Observed control result

```json
{
  "root": "map",
  "nodes": {
    "bool": 2,
    "float": 2,
    "int": 7,
    "map": 7,
    "null": 1,
    "seq": 2,
    "str": 13
  },
  "max_depth": 3,
  "tree": [
    "map",
    [
      [
        "kind",
        [
          "str",
          "catalog"
        ]
      ],
      [
        "version",
        [
          "int",
          "2"
        ]
      ],
      [
        "ratio",
        [
          "float",
          "0.25"
        ]
      ],
      [
        "offset",
        [
          "int",
          "-17"
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
        "retired",
        [
          "bool",
          false
        ]
      ],
      [
        "missing",
        [
          "null"
        ]
      ],
      [
        "title",
        [
          "str",
          "Café \"quoted\"\tend"
        ]
      ],
      [
        "single",
        [
          "str",
          "it's here"
        ]
      ],
      [
        "tags",
        [
          "seq",
          [
            [
              "str",
              "alpha"
            ],
            [
              "str",
              "beta"
            ],
            [
              "str",
              "gamma delta"
            ]
          ]
        ]
      ],
      [
        "point",
        [
          "map",
          [
            [
              "lat",
              [
                "int",
                "1"
              ]
            ],
            [
              "lon",
              [
                "float",
                "-2.5"
              ]
            ]
          ]
        ]
      ],
      [
        "items",
        [
          "seq",
          [
            [
              "map",
              [
                [
                  "id",
                  [
                    "int",
                    "7"
                  ]
                ],
                [
                  "name",
                  [
                    "str",
                    "first item"
                  ]
                ],
                [
                  "note",
                  [
                    "str",
                    "line one\nline two\n"
                  ]
                ]
              ]
            ],
            [
              "map",
              [
                [
                  "id",
                  [
                    "int",
                    "8"
                  ]
                ],
                [
                  "name",
                  [
                    "str",
                    "Zürich"
                  ]
                ],
                [
                  "note",
                  [
                    "str",
                    "folded text\n"
                  ]
                ]
              ]
            ]
          ]
        ]
      ],
      [
        "defaults",
        [
          "map",
          [
            [
              "retries",
              [
                "int",
                "3"
              ]
            ],
            [
              "label",
              [
                "str",
                "base"
              ]
            ]
          ]
        ]
      ],
      [
        "service",
        [
          "map",
          [
            [
              "settings",
              [
                "map",
                [
                  [
                    "retries",
                    [
                      "int",
                      "3"
                    ]
                  ],
                  [
                    "label",
                    [
                      "str",
                      "base"
                    ]
                  ]
                ]
              ]
            ],
            [
              "label",
              [
                "str",
                "edge"
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
python3 parsarium.py build yaml php purrphp_yaml
python3 parsarium.py run yaml php purrphp_yaml controls/yaml/catalog.yaml
```
