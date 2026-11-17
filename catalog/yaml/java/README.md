# YAML / Java — pilot

**Status:** pilot_three_verified_bounded_search; incomplete. 3 verified third-party paths, 0 verified standard APIs, 3 verified Docker harnesses.

Three verified Java YAML paths: SnakeYAML 2.7 (YAML 1.1 SafeConstructor), SnakeYAML Engine 3.2 (YAML 1.2, CoreSchema configured) and circe-yaml 0.16.1 (Scala 2.13 wrapper: SnakeYAML 2.2 compose plus its own node-to-Json conversion). circe-yaml 0.16.1 is a clearly labelled wrapper in the SnakeYAML family: its own 72 Scala lines are identical on both controls, and the control differential (113 lines) is in the SnakeYAML 2.2 scanner, parser and reader it calls; its Json numbers carry no int/float tag, so the harness types an exact-Long number as int (the controls hold no integral-valued floats). jackson-dataformat-yaml 2.23.0, the top lead by deps.dev summed dependents (32,860), returns aliases as anchor-name strings through YAMLMapper.readTree and stays a lead. yamlbeans and eo-yaml (134 and 89) are not yet run. The bounded Maven Central search (query yaml, first 100 of 855 hits) and the named leads are recorded; deps.dev summed directDependentCount counts package adoption, not YAML-specific use, and Scala cross-builds are counted per artifact. The two controls cover a schema-neutral YAML 1.2 subset only, not tags, merge keys, multi-document streams, complex keys or YAML 1.1-only scalars. Coverage and AFL++ feedback are parser source lines under JaCoCo.

[Ranking and search limits](../../../data/java/yaml/ranking.md) · [Standard API inventory](../../../data/java/yaml/standard.json)

## Third-party parsers

- [snakeyaml](snakeyaml/README.md) — verified Docker harness
- [snakeyaml-engine](snakeyaml-engine/README.md) — verified Docker harness
- [circe-yaml](circe-yaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
