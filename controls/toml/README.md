# TOML controls

Two hand-written TOML 1.0.0 documents (UTF-8, LF) and their expected typed trees.
The tree rules and the scope of each control are in the
[TOML cell protocol](../../catalog/toml/PROTOCOL.md).

| Control | Bytes | Expected tree | Role |
| --- | ---: | --- | --- |
| [`service-config.toml`](service-config.toml) | 517 | [`service-config.expected.json`](service-config.expected.json) | Primary control: tables, nested tables, inline tables, array of tables |
| [`typed-scalars.toml`](typed-scalars.toml) | 616 | [`typed-scalars.expected.json`](typed-scalars.expected.json) | Second control for AFL++ feedback: every scalar type, string forms, dotted keys |

```sh
python3 controls/toml/check_controls.py
```

The checker pins both hashes and compares Python's standard-library `tomllib` result with the
hand-written trees. `tomllib` is a vendored `tomli`, so for the Python `tomli` path the hand-written
trees are the independent check.
