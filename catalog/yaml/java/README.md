# YAML / Java — pilot

**Status:** pilot_five_verified_bounded_search; incomplete. 5 verified third-party paths, 0 verified standard APIs, 5 verified Docker harnesses.

Five verified Java YAML paths: SnakeYAML 2.7 (YAML 1.1 SafeConstructor), SnakeYAML Engine 3.2 (YAML 1.2, CoreSchema configured), circe-yaml 0.16.1 (Scala 2.13 wrapper over SnakeYAML 2.2), kjson-yaml 3.15 (own Kotlin parser) and SnakeYAML Engine KMP 5.0.0 (Kotlin port of Engine). circe-yaml 0.16.1 is a clearly labelled wrapper in the SnakeYAML family: its own 72 Scala lines are identical on both controls, and the control differential (113 lines) is in the SnakeYAML 2.2 scanner, parser and reader it calls; its Json numbers carry no int/float tag, so the harness types an exact-Long number as int (the controls hold no integral-valued floats). kjson-yaml 3.15 is an independent Kotlin parser (derived from the same author's yaml-simple) that types scalars itself into kjson-core values. SnakeYAML Engine KMP 5.0.0 is a Kotlin translation of SnakeYAML Engine (same family, separate code); its default LoadSettings already use CoreSchema. Round 2 ran or source-read every higher-ranked lead and none qualified: jackson-dataformat-yaml 2.x (32,860) and Jackson 3 (5,346) return aliases as anchor names (Jackson 3 also reads ~ as a string); kaml (480) forbids aliases by default and its YamlScalar keeps no type or style; vertx-config-yaml (480) and night-config yaml reject a sequence root; yamlbeans (134) and hoplite-yaml (97) return untyped strings; manifold-yaml (123) reads ~ as a string; eo-yaml, yamlkt, JYaml, yaml-simple and scala-yaml fail parsing, aliases or escapes; configurate-yaml drops nulls. hutool-setting (871) is an optional-dependency SnakeYAML delegation, camel-yaml-io a writer, the WSO2 Orbit snakeyaml a byte-identical repackaging, and the circe-yaml Scala 2.12 and 3 cross-builds are the selected source. Below SnakeYAML Engine KMP (27), positive leads remain unrun (circe-yaml-v12 6, moultingyaml 12, boosted-yaml 4 and other first-100 hits), so five slots stay open rather than padded. The bounded Maven Central search (query yaml, first 100 of 855 hits) and the named leads are recorded; round-2 targeted leads outside the first 100 hits are listed in the snapshot; deps.dev summed directDependentCount counts package adoption, not YAML-specific use, and Scala cross-builds are counted per artifact. The two controls cover a schema-neutral YAML 1.2 subset only, not tags, merge keys, multi-document streams, complex keys or YAML 1.1-only scalars. Coverage and AFL++ feedback are parser source lines under JaCoCo.

[Ranking and search limits](../../../data/java/yaml/ranking.md) · [Standard API inventory](../../../data/java/yaml/standard.json)

## Third-party parsers

- [snakeyaml](snakeyaml/README.md) — verified Docker harness
- [snakeyaml-engine](snakeyaml-engine/README.md) — verified Docker harness
- [circe-yaml](circe-yaml/README.md) — verified Docker harness
- [zio-json-yaml](zio-json-yaml/README.md) — verified API path
- [kjson-yaml](kjson-yaml/README.md) — verified Docker harness
- [snakeyaml-engine-kmp](snakeyaml-engine-kmp/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
