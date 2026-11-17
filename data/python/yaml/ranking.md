# Python × YAML: pilot ranking

No third-party path is verified yet; this cell records the bounded search and the leads in primary-metric order. The ceiling is ten.

## Primary within-cell adoption metric

PyPI Stats `last_month` downloads excluding known mirrors, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell.

## Leads (unverified)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| PyYAML | unresolved | 1,227,712,536 | PyYAML pure Python (CLoader is the libyaml family) |
| ruamel.yaml | unresolved | 177,667,165 | ruamel.yaml (PyYAML-derived, YAML 1.2) |
| strictyaml | shared_family | 29,369,654 | ruamel.yaml via strictyaml |
| oyaml | shared_family | 2,622,495 | PyYAML |
| rapidyaml | unresolved | 224,758 | rapidyaml (ryml) |
| yamlcore | shared_family | 92,413 | PyYAML with YAML 1.2 core resolver |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
