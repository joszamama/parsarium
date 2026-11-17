# snakeyaml — YAML / Java

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.7`
- **License:** Apache-2.0
- **Parser family:** SnakeYAML (own reader, scanner, parser, composer and YAML 1.1 resolver)
- **Local input API:** `new Yaml(new SafeConstructor(new LoaderOptions())).load(InputStream) over Files.newInputStream(Path)`
- **Documentation:** [API reference](<https://javadoc.io/static/org.yaml/snakeyaml/2.7/org/yaml/snakeyaml/Yaml.html>)
- **Valid control:** [`controls/yaml/catalog.yaml`](../../../../controls/yaml/catalog.yaml)
- **Catalog evidence:** [parser record](../../../../data/java/yaml/parsers.json) · [control result](../../../../data/java/yaml/verification.json)

## Observed control result

```json
{
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
python3 parsarium.py build yaml java snakeyaml
python3 parsarium.py run yaml java snakeyaml controls/yaml/catalog.yaml
```
