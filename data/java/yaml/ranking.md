# Java × YAML: pilot ranking

Three control-verified third-party paths. The ceiling is ten; the cell is not padded. The top lead by the metric, jackson-dataformat-yaml, fails the alias part of the control through `YAMLMapper.readTree` and stays a lead.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)), the metric of the Java JSON cell. Package adoption, not YAML-specific use. Scala cross-builds are separate Maven artifacts; the pinned artifact's own count is used and the others are not summed.

| Rank | Package | Release | Metric | Control feedback difference | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [snakeyaml](https://javadoc.io/static/org.yaml/snakeyaml/2.7/org/yaml/snakeyaml/Yaml.html) | 2.7 | 10,859 | 119 lines / 118 tuples | SnakeYAML |
| 2 | [snakeyaml-engine](https://javadoc.io/static/org.snakeyaml/snakeyaml-engine/3.2/org.snakeyaml.engine/org/snakeyaml/engine/v2/api/Load.html) | 3.2 | 493 | 124 lines / 122 tuples | SnakeYAML Engine |
| 3 | [circe-yaml](https://github.com/circe/circe-yaml/blob/v0.16.1/README.md) | 0.16.1 | 127 | 113 lines / 111 tuples (wrapper 0, SnakeYAML 113) | SnakeYAML via circe-yaml (wrapper) |

All paths load the documents into ordered trees; aliases resolve to the anchored node. circe-yaml is a wrapper over SnakeYAML 2.2: its own lines show no control differential, and its feedback row splits wrapper and SnakeYAML lines. AFL++ feedback: [afl-feedback.json](afl-feedback.json).

## Leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| com.fasterxml.jackson.dataformat:jackson-dataformat-yaml | fails_control | 32,860 | SnakeYAML (Engine in 3.x) via Jackson |
| org.yaml:snakeyaml | selected | 10,859 | SnakeYAML |
| org.snakeyaml:snakeyaml-engine | selected | 493 | SnakeYAML Engine |
| com.esotericsoftware.yamlbeans:yamlbeans | unresolved | 134 | YamlBeans |
| io.circe:circe-yaml_2.13 | selected | 127 | SnakeYAML via circe-yaml (Scala wrapper) |
| com.amihaiemil.web:eo-yaml | unresolved | 89 | eo-yaml |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
