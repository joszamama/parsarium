# Java × YAML: pilot ranking

Six control-verified third-party paths. The ceiling is ten; the cell is not padded. Every lead ranked above the sixth path was run on the controls or read at its pinned source and failed or was excluded; the evidence is in [leads.json](leads.json).

## Primary within-cell adoption metric

deps.dev `directDependentCount` summed over every Maven release, captured 2026-11-17 ([snapshot](registry-snapshot.json)), the metric of the Java JSON cell. Package adoption, not YAML-specific use. Scala cross-builds are separate Maven artifacts; the pinned artifact's own count is used and the others are not summed.

| Rank | Package | Release | Metric | Control feedback difference | Parser family |
| ---: | --- | --- | ---: | --- | --- |
| 1 | [snakeyaml](https://javadoc.io/static/org.yaml/snakeyaml/2.7/org/yaml/snakeyaml/Yaml.html) | 2.7 | 10,859 | 119 lines / 118 tuples | SnakeYAML |
| 2 | [snakeyaml-engine](https://javadoc.io/static/org.snakeyaml/snakeyaml-engine/3.2/org.snakeyaml.engine/org/snakeyaml/engine/v2/api/Load.html) | 3.2 | 493 | 124 lines / 122 tuples | SnakeYAML Engine |
| 3 | [circe-yaml](https://github.com/circe/circe-yaml/blob/v0.16.1/README.md) | 0.16.1 | 127 | 113 lines / 111 tuples (wrapper 0, SnakeYAML 113) | SnakeYAML via circe-yaml (wrapper) |
| 4 | [zio-json-yaml](https://github.com/zio/zio-json/blob/v1.1.2/docs/yaml.md) | 1.1.2 | 63 | 120 lines / 116 tuples (wrapper 0, SnakeYAML 120) | SnakeYAML via zio-json-yaml (wrapper) |
| 5 | [kjson-yaml](https://github.com/pwall567/kjson-yaml/blob/3.15/README.md) | 3.15 | 29 | 59 lines / 59 tuples | kjson-yaml |
| 6 | [snakeyaml-engine-kmp](https://github.com/krzema12/snakeyaml-engine-kmp/blob/v5.0.0/README.md) | 5.0.0 | 27 | 112 lines / 105 tuples | SnakeYAML Engine KMP (Kotlin port) |

All paths load the documents into ordered trees; aliases resolve to the anchored node. circe-yaml and zio-json-yaml are wrappers over SnakeYAML 2.2 and 2.7 from separate projects: their own lines show no control differential, and their feedback rows split wrapper and SnakeYAML lines. AFL++ feedback: [afl-feedback.json](afl-feedback.json).

## Leads

| Lead | Status | Metric | Parser family |
| --- | --- | ---: | --- |
| com.fasterxml.jackson.dataformat:jackson-dataformat-yaml | fails_control | 32,860 | SnakeYAML (Engine in 3.x) via Jackson |
| org.yaml:snakeyaml | selected | 10,859 | SnakeYAML |
| tools.jackson.dataformat:jackson-dataformat-yaml | fails_control | 5,346 | SnakeYAML Engine via Jackson 3 |
| cn.hutool:hutool-setting | excluded | 871 | SnakeYAML via hutool YamlUtil (optional dependency) |
| org.snakeyaml:snakeyaml-engine | selected | 493 | SnakeYAML Engine |
| com.charleskorn.kaml:kaml-jvm | fails_control | 480 | SnakeYAML Engine KMP via kaml (kotlinx.serialization format) |
| io.vertx:vertx-config-yaml | fails_control | 480 | SnakeYAML via Vert.x config YamlProcessor |
| org.apache.camel:camel-yaml-io | excluded | 178 | Camel route model YAML writer |
| io.circe:circe-yaml_2.12 | excluded | 170 | SnakeYAML via circe-yaml (Scala 2.12 cross-build) |
| com.esotericsoftware.yamlbeans:yamlbeans | fails_control | 134 | YamlBeans |
| io.circe:circe-yaml_2.13 | selected | 127 | SnakeYAML via circe-yaml (Scala wrapper) |
| systems.manifold:manifold-yaml | fails_control | 123 | SnakeYAML Engine 1.0 via manifold-yaml-rt |
| com.sksamuel.hoplite:hoplite-yaml | fails_control | 97 | SnakeYAML events via hoplite YamlParser |
| io.circe:circe-yaml_3 | excluded | 94 | SnakeYAML via circe-yaml (Scala 3 cross-build) |
| com.amihaiemil.web:eo-yaml | fails_control | 89 | eo-yaml |
| dev.zio:zio-json-yaml_2.13 | selected | 63 | SnakeYAML via zio-json-yaml (Scala wrapper) |
| net.mamoe.yamlkt:yamlkt-jvm | fails_control | 56 | yamlkt (own Kotlin parser) |
| com.charleskorn.kaml:kaml | excluded | 56 | SnakeYAML Engine KMP via kaml (KMP root module) |
| org.spongepowered:configurate-yaml | fails_control | 48 | SnakeYAML (bundled) via Configurate |
| net.pwall.yaml:yaml-simple | fails_control | 36 | kjson-yaml predecessor (own Kotlin parser) |
| org.jyaml:jyaml | fails_control | 31 | JYaml |
| io.kjson:kjson-yaml | selected | 29 | kjson-yaml (own Kotlin parser) |
| org.virtuslab:scala-yaml_3 | fails_control | 28 | scala-yaml (own Scala 3 parser) |
| it.krzeminski:snakeyaml-engine-kmp-jvm | selected | 27 | SnakeYAML Engine KMP (Kotlin port of SnakeYAML Engine) |
| org.wso2.orbit.org.yaml:snakeyaml | excluded | 27 | SnakeYAML (OSGi repackaging) |
| com.electronwill.night-config:yaml | fails_control | 21 | SnakeYAML 1.33 via NightConfig |
| net.jcazevedo:moultingyaml_2.12 | unresolved | 12 | SnakeYAML via moultingyaml (Scala) |
| it.krzeminski:snakeyaml-engine-kmp | excluded | 8 | SnakeYAML Engine KMP (KMP root module) |
| org.virtuslab:scala-yaml_2.13 | excluded | 6 | scala-yaml (Scala 2.13 cross-build) |
| io.circe:circe-yaml-v12_2.13 | unresolved | 6 | SnakeYAML Engine via circe-yaml-v12 (Scala wrapper) |
| dev.dejvokep:boosted-yaml | unresolved | 4 | SnakeYAML Engine via boosted-yaml (configuration library) |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
