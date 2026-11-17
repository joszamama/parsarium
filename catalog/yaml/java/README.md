# YAML / Java — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

One verified Java YAML path: SnakeYAML 2.7 (YAML 1.1 SafeConstructor). SnakeYAML Engine 3.2 (493) is the next lead. jackson-dataformat-yaml 2.23.0, the top lead by deps.dev summed dependents (32,860), parses every scalar and collection of both controls but returns aliases as anchor-name strings through YAMLMapper.readTree, so it fails the alias part of the control and stays a lead in the SnakeYAML family. yamlbeans and eo-yaml (134 and 89) are not yet run. The bounded Maven Central search (query yaml, first 100 of 855 hits) and five named leads are recorded; deps.dev summed directDependentCount counts package adoption, not YAML-specific use. The two controls cover a schema-neutral YAML 1.2 subset only, not tags, merge keys, multi-document streams, complex keys or YAML 1.1-only scalars. Coverage and AFL++ feedback are SnakeYAML source lines under JaCoCo; the control differences are in the scanner, parser and constructors.

[Ranking and search limits](../../../data/java/yaml/ranking.md) · [Standard API inventory](../../../data/java/yaml/standard.json)

## Third-party parsers

- [snakeyaml](snakeyaml/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
