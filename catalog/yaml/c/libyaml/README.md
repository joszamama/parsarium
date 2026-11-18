# libyaml — YAML / C

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.2.5`
- **Upstream:** [source repository](<https://github.com/yaml/libyaml>) · [Debian](<https://tracker.debian.org/pkg/libyaml>)
- **License:** MIT
- **Parser family:** libyaml (reader.c/scanner.c/parser.c/loader.c)
- **Local input API:** `yaml_parser_initialize; yaml_parser_set_input_string(yaml_parser_t *parser, const unsigned char *input, size_t size); yaml_parser_load(yaml_parser_t *parser, yaml_document_t *document)`
- **Documentation:** [API reference](<https://github.com/yaml/libyaml/blob/0.2.5/include/yaml.h>)
- **Valid control:** [`controls/yaml/catalog.yaml`](../../../../controls/yaml/catalog.yaml)
- **Catalog evidence:** [parser record](../../../../data/c/yaml/parsers.json) · [control result](../../../../data/c/yaml/verification.json)

## Observed control result

```json
{
  "max_depth": 3,
  "nodes": {
    "bool": 2,
    "float": 2,
    "int": 7,
    "map": 7,
    "null": 1,
    "seq": 2,
    "str": 13
  },
  "root": "map",
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
  ],
  "tree_sha256": "031d7bf7daeecfb14b6c5da4b93235a39776cd31b1121e350b78bd42bbcef62b"
}
```

## Run this target

```sh
python3 parsarium.py build yaml c libyaml
python3 parsarium.py run yaml c libyaml controls/yaml/catalog.yaml
```
