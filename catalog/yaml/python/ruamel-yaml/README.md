# ruamel.yaml — YAML / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.19.1`
- **Upstream:** [source repository](<https://sourceforge.net/projects/ruamel-yaml/>) · [PyPI](<https://pypi.org/project/ruamel.yaml/>)
- **License:** MIT
- **Parser family:** ruamel.yaml pure-Python loader (PyYAML-derived Reader/Scanner/Parser/Composer, SafeConstructor, YAML 1.2 VersionedResolver); not the ruamel.yaml.clib(z) C route
- **Local input API:** `ruamel.yaml.YAML(typ='safe', pure=True).load(local YAML bytes); the decoded str and a local binary stream give the same tree`
- **Documentation:** [API reference](<https://yaml.dev/doc/ruamel.yaml/basicuse/>)
- **Valid control:** [`controls/yaml/catalog.yaml`](../../../../controls/yaml/catalog.yaml)
- **Catalog evidence:** [parser record](../../../../data/python/yaml/parsers.json) · [control result](../../../../data/python/yaml/verification.json)

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
  "tree_sha256": "031d7bf7daeecfb14b6c5da4b93235a39776cd31b1121e350b78bd42bbcef62b",
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
python3 parsarium.py build yaml python ruamel_yaml
python3 parsarium.py run yaml python ruamel_yaml controls/yaml/catalog.yaml
```
