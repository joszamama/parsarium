# Java × YAML: pilot ranking

No third-party path is verified yet; this cell records the bounded search and the leads in primary-metric order. The ceiling is ten.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)). Values are package adoption, not YAML-specific use, and are compared only within this cell.

## Leads (unverified)

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| com.fasterxml.jackson.dataformat:jackson-dataformat-yaml | shared_family | 32,860 | SnakeYAML (Engine in 3.x) via Jackson |
| org.yaml:snakeyaml | unresolved | 10,859 | SnakeYAML |
| org.snakeyaml:snakeyaml-engine | unresolved | 493 | SnakeYAML Engine |
| com.esotericsoftware.yamlbeans:yamlbeans | unresolved | 134 | YamlBeans |
| com.amihaiemil.web:eo-yaml | unresolved | 89 | eo-yaml |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
