# Java × YAML: pilot ranking

One control-verified third-party path. The ceiling is ten; the cell is not padded. The top lead by the metric, jackson-dataformat-yaml, fails the alias part of the control through `YAMLMapper.readTree` and stays a lead.

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)), the metric of the Java JSON cell. Package adoption, not YAML-specific use.

| Rank | Package | Release | Metric | Control feedback difference | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [snakeyaml](https://javadoc.io/static/org.yaml/snakeyaml/2.7/org/yaml/snakeyaml/Yaml.html) | 2.7 | 10,859 | 119 lines / 118 tuples | SnakeYAML |

The path loads the documents into Java collections; aliases resolve to the anchored object. AFL++ feedback: [afl-feedback.json](afl-feedback.json).

## Leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| com.fasterxml.jackson.dataformat:jackson-dataformat-yaml | fails_control | 32,860 | SnakeYAML (Engine in 3.x) via Jackson |
| org.yaml:snakeyaml | selected | 10,859 | SnakeYAML |
| org.snakeyaml:snakeyaml-engine | unresolved | 493 | SnakeYAML Engine |
| com.esotericsoftware.yamlbeans:yamlbeans | unresolved | 134 | YamlBeans |
| com.amihaiemil.web:eo-yaml | unresolved | 89 | eo-yaml |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
