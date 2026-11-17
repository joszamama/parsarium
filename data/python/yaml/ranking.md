# Python × YAML: pilot ranking

Three control-verified third-party paths. The ceiling is ten; this pilot does not pad the selection. A path is an API route, not necessarily an independent parser engine.

## Primary within-cell adoption metric

PyPI Stats `last_month` downloads excluding known mirrors, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell. PyYAML CSafeLoader is a route of the PyYAML package and carries the same package value (PyPI does not split by loader); it is listed after the pure SafeLoader path, which was selected first.

| Rank | Package | Release | Last-month downloads | Parsed scope | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) | 6.0.3 | 1,227,712,536 | yaml.load(local YAML bytes, Loader=yaml.SafeLoader), the pure-Python safe loader | PyYAML pure-Python loader (yaml/scanner.py, parser.py, composer.py, SafeConstructor, YAML 1.1 Resolver); not the libyaml CSafeLoader route |
| 2 | [PyYAML CSafeLoader (libyaml)](https://pyyaml.org/wiki/PyYAMLDocumentation) | 6.0.3 | 1,227,712,536 | yaml.load(local YAML bytes, Loader=yaml.CSafeLoader) | libyaml 0.2.5 through PyYAML's _yaml C extension (CParser), with PyYAML's Python SafeConstructor and YAML 1.1 Resolver; not the pure-Python SafeLoader route |
| 3 | [ruamel.yaml](https://yaml.dev/doc/ruamel.yaml/basicuse/) | 0.19.1 | 177,667,165 | ruamel.yaml.YAML(typ='safe', pure=True).load(local YAML bytes) | ruamel.yaml pure-Python loader (PyYAML-derived Reader/Scanner/Parser/Composer, SafeConstructor, YAML 1.2 VersionedResolver); not the ruamel.yaml.clib(z) C route |

Both controls must equal the hand-written typed trees in [check_controls.py](../../../controls/yaml/check_controls.py); see [verification.json](verification.json).

## Remaining leads

| Lead | Status | Metric | Parser family | Decision |
| --- | --- | ---: | --- | --- |
| strictyaml | shared_family | 29,369,654 | ruamel.yaml via strictyaml | Unverified wrapper/fork lead sharing a parser family named in the note; it needs its own pinned control run before selection. |
| oyaml | shared_family | 2,622,495 | PyYAML | Unverified wrapper/fork lead sharing a parser family named in the note; it needs its own pinned control run before selection. |
| rapidyaml | unresolved | 224,758 | rapidyaml (ryml) | Unverified lead: no pinned release, control run or harness yet. |
| yamlcore | shared_family | 92,413 | PyYAML with YAML 1.2 core resolver | Unverified wrapper/fork lead sharing a parser family named in the note; it needs its own pinned control run before selection. |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
