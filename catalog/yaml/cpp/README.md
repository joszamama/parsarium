# YAML / C++ — pilot

**Status:** pilot_one_verified_bounded_search; incomplete. 1 verified third-party paths, 0 verified standard APIs, 1 verified Docker harnesses.

1 verified C++ YAML path. The bounded Debian source-name search ('yaml', 90 hits in the pinned sourcemax snapshot) found yaml-cpp and rapidyaml; unresolved leads: rapidyaml, fkyaml (fkYAML is not packaged in Debian and has no primary value). yaml-cpp keeps plain scalars untyped, so its harness types plain scalars with YAML 1.2 core-schema patterns and converts them with Node::as<T>; this is adapter-side typing. Package installations are not YAML-specific use. Two schema-neutral valid controls do not establish tags, merge keys, multi-document streams, YAML 1.1-only scalars, complex keys or malformed-input behavior.

[Ranking and search limits](../../../data/cpp/yaml/ranking.md) · [Standard API inventory](../../../data/cpp/yaml/standard.json)

## Third-party parsers

- [yaml-cpp](yaml-cpp/README.md) — verified Docker harness

## Standard and runtime APIs

None verified in this pilot cell yet.
