# jiter — JSON / Python

**Pilot / incomplete format cell.** This path is verified on its stated control; the format-wide search is still in progress.

- **Pinned release:** `0.19.0`
- **Upstream:** [source repository](<https://github.com/pydantic/jiter>) · [PyPI](<https://pypi.org/project/jiter/>)
- **License:** MIT
- **Parser family:** Jiter 0.19.0 Rust parser (PythonParser over jiter::parse::Parser) / lexical-parse-float 1.0.6
- **Local input API:** `jiter.from_json(local JSON bytes) with documented defaults (cache_mode='all', partial_mode=False, allow_inf_nan=True, float_mode='float')`
- **Documentation:** [API reference](<https://github.com/pydantic/jiter/blob/v0.19.0/crates/jiter-python/README.md>)
- **Valid control:** [`controls/json/nested-object.json`](../../../../controls/json/nested-object.json)
- **Catalog evidence:** [parser record](../../../../data/python/json/parsers.json) · [control result](../../../../data/python/json/verification.json)

## Observed control result

```json
{
  "root_type": "object",
  "root_length": 7,
  "top_level_keys": [
    "name",
    "version",
    "ratio",
    "enabled",
    "missing",
    "tags",
    "nested"
  ],
  "kind_counts": {
    "object": 5,
    "array": 3,
    "string": 5,
    "int": 4,
    "float": 1,
    "bool": 2,
    "null": 1
  },
  "object_members": 15,
  "max_container_depth": 4,
  "scalar_leaves": [
    [
      "/name",
      "string",
      "parsarium"
    ],
    [
      "/version",
      "int",
      1
    ],
    [
      "/ratio",
      "float",
      "-2.5"
    ],
    [
      "/enabled",
      "bool",
      true
    ],
    [
      "/missing",
      "null",
      null
    ],
    [
      "/tags/0",
      "string",
      "json"
    ],
    [
      "/tags/1",
      "string",
      "go"
    ],
    [
      "/tags/2",
      "string",
      "rfc8259"
    ],
    [
      "/nested/level",
      "int",
      2
    ],
    [
      "/nested/items/0/id",
      "int",
      1
    ],
    [
      "/nested/items/0/ok",
      "bool",
      false
    ],
    [
      "/nested/items/1/id",
      "int",
      2
    ],
    [
      "/nested/items/1/text",
      "string",
      "café \"quoted\""
    ]
  ],
  "empty_containers": [
    [
      "/nested/empty",
      "object"
    ],
    [
      "/nested/list",
      "array"
    ]
  ]
}
```

## Run this target

```sh
python3 parsarium.py build json python jiter
python3 parsarium.py run json python jiter controls/json/nested-object.json
```
