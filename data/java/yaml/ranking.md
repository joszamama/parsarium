# Java × YAML: pilot ranking

Six control-verified third-party paths. The ceiling is ten; the cell is not padded. Every lead ranked above the sixth path was run on the controls or read at its pinned source and failed or was excluded, and every positive-metric lead below it was decided the same way, so four slots stay open; the evidence is in [leads.json](leads.json).

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
| org.springframework:spring-beans | excluded | 59,801 | SnakeYAML via Spring YamlProcessor (bean-factory utility, optional dependency) |
| com.fasterxml.jackson.dataformat:jackson-dataformat-yaml | fails_control | 32,860 | SnakeYAML (Engine in 3.x) via Jackson |
| org.yaml:snakeyaml | selected | 10,859 | SnakeYAML |
| tools.jackson.dataformat:jackson-dataformat-yaml | fails_control | 5,346 | SnakeYAML Engine via Jackson 3 |
| org.apache.groovy:groovy-yaml | fails_control | 4,090 | SnakeYAML via Jackson YAMLFactory via Groovy YamlSlurper (wrapper) |
| org.apache.commons:commons-configuration2 | fails_control | 3,072 | SnakeYAML via Commons Configuration YAMLConfiguration (configuration library) |
| org.openrewrite:rewrite-yaml | fails_control | 2,501 | SnakeYAML events via OpenRewrite YamlParser (lossless source tree) |
| org.noear:solon-config-yaml | excluded | 1,582 | SnakeYAML via Solon PropertiesYaml (configuration loader) |
| org.noear:solon.config.yaml | excluded | 1,549 | empty compatibility artifact for org.noear:solon-config-yaml |
| io.helidon.config:helidon-config-yaml | excluded | 910 | SnakeYAML via Helidon YamlConfigParser (configuration loader) |
| cn.hutool:hutool-setting | excluded | 871 | SnakeYAML via hutool YamlUtil (optional dependency) |
| org.http4k:http4k-format-jackson-yaml | excluded | 804 | SnakeYAML via Jackson YAMLFactory via http4k (message-format lens) |
| org.snakeyaml:snakeyaml-engine | selected | 493 | SnakeYAML Engine |
| com.charleskorn.kaml:kaml-jvm | fails_control | 480 | SnakeYAML Engine KMP via kaml (kotlinx.serialization format) |
| io.vertx:vertx-config-yaml | fails_control | 480 | SnakeYAML via Vert.x config YamlProcessor |
| org.apache.camel:camel-snakeyaml | excluded | 426 | SnakeYAML via Camel SnakeYAMLDataFormat (integration data format) |
| no.nav.common:yaml | excluded | 275 | SnakeYAML via Jackson YAMLFactory (NAV common utility) |
| io.smallrye.config:smallrye-config-source-yaml | excluded | 249 | SnakeYAML via SmallRye Config YamlConfigSource (configuration source) |
| org.apache.camel:camel-yaml-io | excluded | 178 | Camel route model YAML writer |
| org.citrusframework:citrus-yaml | excluded | 171 | SnakeYAML via Citrus YAML test DSL |
| io.circe:circe-yaml_2.12 | excluded | 170 | SnakeYAML via circe-yaml (Scala 2.12 cross-build) |
| com.esotericsoftware.yamlbeans:yamlbeans | fails_control | 134 | YamlBeans |
| io.circe:circe-yaml_2.13 | selected | 127 | SnakeYAML via circe-yaml (Scala wrapper) |
| systems.manifold:manifold-yaml | fails_control | 123 | SnakeYAML Engine 1.0 via manifold-yaml-rt |
| com.sksamuel.hoplite:hoplite-yaml | fails_control | 97 | SnakeYAML events via hoplite YamlParser |
| io.circe:circe-yaml_3 | excluded | 94 | SnakeYAML via circe-yaml (Scala 3 cross-build) |
| com.amihaiemil.web:eo-yaml | fails_control | 89 | eo-yaml |
| com.networknt:yaml-rule | excluded | 78 | SnakeYAML via Jackson YAMLMapper (rule-engine mapping) |
| io.avaje:avaje-config | excluded | 75 | avaje-config YamlLoaderSimple / YamlLoaderSnake (configuration loader) |
| io.jenkins.plugins:snakeyaml-api | excluded | 74 | SnakeYAML (Jenkins library-plugin repackaging) |
| io.ktor:ktor-server-config-yaml-jvm | excluded | 72 | kaml via Ktor YamlConfig (server configuration) |
| org.http4k:http4k-format-moshi-yaml | excluded | 66 | SnakeYAML via Moshi via http4k (message-format lens) |
| dev.zio:zio-json-yaml_2.13 | selected | 63 | SnakeYAML via zio-json-yaml (Scala wrapper) |
| net.mamoe.yamlkt:yamlkt-jvm | fails_control | 56 | yamlkt (own Kotlin parser) |
| com.charleskorn.kaml:kaml | excluded | 56 | SnakeYAML Engine KMP via kaml (KMP root module) |
| org.codehaus.groovy:groovy-yaml | excluded | 49 | SnakeYAML via Jackson YAMLFactory via Groovy YamlSlurper (Groovy 3 coordinate) |
| org.spongepowered:configurate-yaml | fails_control | 48 | SnakeYAML (bundled) via Configurate |
| io.maryk:maryk-yaml-jvm | fails_control | 45 | maryk-yaml (own Kotlin token reader) |
| io.maryk:maryk-yaml | excluded | 45 | maryk-yaml (KMP root module) |
| io.takari.polyglot:polyglot-yaml | excluded | 38 | SnakeYAML via Maven Polyglot (POM model mapping) |
| dev.zio:zio-config-yaml_3 | excluded | 38 | SnakeYAML Engine via ZIO Config YamlConfigProvider (configuration loader) |
| net.pwall.yaml:yaml-simple | fails_control | 36 | kjson-yaml predecessor (own Kotlin parser) |
| org.jyaml:jyaml | fails_control | 31 | JYaml |
| io.kjson:kjson-yaml | selected | 29 | kjson-yaml (own Kotlin parser) |
| org.virtuslab:scala-yaml_3 | fails_control | 28 | scala-yaml (own Scala 3 parser) |
| it.krzeminski:snakeyaml-engine-kmp-jvm | selected | 27 | SnakeYAML Engine KMP (Kotlin port of SnakeYAML Engine) |
| org.wso2.orbit.org.yaml:snakeyaml | excluded | 27 | SnakeYAML (OSGi repackaging) |
| com.electronwill.night-config:yaml | fails_control | 21 | SnakeYAML 1.33 via NightConfig |
| dev.zio:zio-config-yaml_2.13 | excluded | 18 | SnakeYAML Engine via ZIO Config (Scala 2.13 cross-build) |
| com.uchuhimo:konf-yaml | fails_control | 18 | SnakeYAML via konf YamlProvider (configuration library) |
| com.github.sbaudoin:yamllint | excluded | 17 | SnakeYAML tokens via yamllint (linter) |
| dev.zio:zio-json-yaml_2.12 | excluded | 16 | SnakeYAML via zio-json-yaml (Scala 2.12 cross-build) |
| dev.zio:zio-json-yaml_3 | excluded | 14 | SnakeYAML via zio-json-yaml (Scala 3 cross-build) |
| org.bspfsystems:yamlconfiguration | fails_control | 13 | SnakeYAML via Bukkit-style YamlConfiguration (configuration library) |
| net.jcazevedo:moultingyaml_2.12 | fails_control | 12 | SnakeYAML via moultingyaml (Scala) |
| org.jruby.extras:jvyamlb | fails_control | 11 | JvYAML (PyYAML-derived Java port; byte-oriented JRuby variant) |
| com.github.pureconfig:pureconfig-yaml_2.13 | fails_control | 10 | SnakeYAML via PureConfig YamlConfigSource (configuration library) |
| net.pwall.yaml:yaml-base | excluded | 9 | yaml-simple node classes |
| dev.hnaderi:yaml4s-snake_2.13 | fails_control | 9 | SnakeYAML Engine via yaml4s-snake (Scala wrapper; converter shared with circe-yaml-v12) |
| dev.hnaderi:yaml4s-snake_3 | excluded | 9 | SnakeYAML Engine via yaml4s-snake (Scala 3 cross-build) |
| it.krzeminski:snakeyaml-engine-kmp | excluded | 8 | SnakeYAML Engine KMP (KMP root module) |
| net.jcazevedo:moultingyaml_2.11 | excluded | 8 | SnakeYAML via moultingyaml (Scala 2.11 cross-build) |
| dev.hnaderi:yaml4s-snake_2.12 | excluded | 8 | SnakeYAML Engine via yaml4s-snake (Scala 2.12 cross-build) |
| io.github.yaml-path:yaml-path | excluded | 7 | SnakeYAML via Jackson YAMLMapper (path query layer) |
| org.virtuslab:scala-yaml_2.13 | excluded | 6 | scala-yaml (Scala 2.13 cross-build) |
| io.circe:circe-yaml-v12_2.13 | fails_control | 6 | SnakeYAML Engine via circe-yaml-v12 (Scala wrapper; same project as circe-yaml) |
| net.java.dev:jvyaml | fails_control | 6 | JvYAML (PyYAML-derived Java port) |
| dev.dejvokep:boosted-yaml | fails_control | 4 | SnakeYAML Engine (relocated copy) via boosted-yaml (configuration library) |
| io.circe:circe-yaml-v12_3 | excluded | 4 | SnakeYAML Engine via circe-yaml-v12 (Scala 3 cross-build) |
| io.basc.framework:yaml | excluded | 4 | SnakeYAML via basc YamlProcessor (properties loader) |
| io.sourceforge.github.components:yaml-snakeyaml | excluded | 4 | empty SnakeYAML dependency artifact |
| org.treblereel.gwt.yaml:eo-yaml | excluded | 4 | eo-yaml (GWT fork) |
| org.jruby:yecht | fails_control | 4 | Syck (Java port of the C Syck parser, YAML 1.0) |
| io.maryk:yaml-jvm | excluded | 3 | maryk-yaml predecessor coordinate |
| io.maryk:yaml | excluded | 3 | maryk-yaml predecessor coordinate (KMP root) |
| net.jcazevedo:moultingyaml_2.13 | excluded | 3 | SnakeYAML via moultingyaml (Scala 2.13 cross-build) |
| ninja.leaping.configurate:configurate-yaml | excluded | 3 | SnakeYAML via Configurate (predecessor coordinate) |
| io.circe:circe-yaml-v12_2.12 | excluded | 2 | SnakeYAML Engine via circe-yaml-v12 (Scala 2.12 cross-build) |
| com.github.siroshun09.configapi:yaml | excluded | 2 | SnakeYAML via ConfigAPI YamlConfiguration (configuration library) |
| com.github.autermann:yaml | fails_control | 2 | SnakeYAML via autermann YamlNode tree |
| org.embulk:embulk-util-snakeyaml | excluded | 2 | SnakeYAML tag resolver helper for Embulk |
| io.ktor:ktor-server-config-yaml | excluded | 1 | kaml via Ktor YamlConfig (KMP root module) |
| io.circe:circe-yaml-scalayaml_3 | excluded | 1 | scala-yaml via circe-yaml-scalayaml (Scala wrapper) |
| org.asux:yaml | excluded | 1 | ASUX YAML command-line processor |
| org.elypia.yaml4deltaspike:yaml4deltaspike | excluded | 1 | SnakeYAML via DeltaSpike YamlConfigSource (configuration source) |
| com.github.mhshams:dahgan-core | excluded | 1 | dahgan (Kotlin port of the YAML 1.2 reference parser, tokenizer module) |
| com.dnanexus:dxyaml | fails_control | 1 | SnakeYAML Engine via dxYaml (moultingyaml-derived Scala wrapper) |

Standard and runtime APIs: none documented ([standard.json](standard.json)).
