# Python × YAML: pilot ranking

One control-verified third-party path. The ceiling is ten; this pilot does not pad the selection. A path is an API route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

PyPI Stats `last_month` downloads excluding known mirrors, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell.

| Rank | Package | Release | Last-month downloads | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) | 6.0.3 | 1,227,712,536 | yaml.load(local YAML bytes, Loader=yaml.SafeLoader), the pure-Python safe loader | PyYAML pure-Python loader (yaml/scanner.py, parser.py, composer.py, SafeConstructor, YAML 1.1 Resolver); not the libyaml CSafeLoader route |

Both controls must equal the hand-written typed trees in [check_controls.py](../../../controls/yaml/check_controls.py); see [verification.json](verification.json).

## Remaining leads (unverified)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| PyYAML CSafeLoader (libyaml) | unresolved | n/a | libyaml through PyYAML's _yaml C extension |
| ruamel.yaml | unresolved | 177,667,165 | ruamel.yaml (PyYAML-derived, YAML 1.2) |
| strictyaml | shared_family | 29,369,654 | ruamel.yaml via strictyaml |
| oyaml | shared_family | 2,622,495 | PyYAML |
| rapidyaml | unresolved | 224,758 | rapidyaml (ryml) |
| yamlcore | shared_family | 92,413 | PyYAML with YAML 1.2 core resolver |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
