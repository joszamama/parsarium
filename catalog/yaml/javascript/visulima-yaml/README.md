# @visulima/yaml — YAML / JavaScript

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `2.0.0`
- **Upstream:** [source repository](<https://github.com/visulima/visulima>) · [npm](<https://www.npmjs.com/package/@visulima/yaml>)
- **License:** MIT
- **Parser family:** @visulima/yaml own scanner, parser and composer
- **Local input API:** `parse(text) with default options (YAML 1.2, core schema, strict) after strict UTF-8 decoding of a local Buffer; a YAMLError rejects the input; the returned value is mapped to the Parsarium typed YAML tree`
- **Documentation:** [API reference](<https://github.com/visulima/visulima/blob/%40visulima/yaml%402.0.0/packages/data-manipulation/yaml/README.md>)
- **Valid control:** [`controls/yaml/catalog.yaml`](../../../../controls/yaml/catalog.yaml)
- **Catalog evidence:** [parser record](../../../../data/javascript/yaml/parsers.json) · [control result](../../../../data/javascript/yaml/verification.json)

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

## Verification scope

Both valid schema-neutral YAML 1.2 controls give exact typed trees equal to the hand-written expected trees in controls/yaml/check_controls.py (cross-checked there with Ruby Psych/libyaml). The controls avoid integral-valued floats and integer-like keys, so the JavaScript number and key-order limits cannot change the result. They do not test tags, merge keys, multi-document streams, YAML 1.1-only scalars or malformed input.

## Run this target

```sh
python3 parsarium.py build yaml javascript visulima_yaml
python3 parsarium.py run yaml javascript visulima_yaml controls/yaml/catalog.yaml
```
